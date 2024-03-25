import os
import subprocess
import argparse
from sys import argv

def main():
    if(len(sys.argv) != 2):
        print("Usage: syslogd {command}")
    option = sys.argv[1]
    
    if(option.lower() in ('-h', '--help')):
        print("""
        Syslogd, controller for the syslogT trojan.
        
        Commands:
        
        -h, --help   | displays this message and exits.
        
        -s, --status | displays current module status.
        
        """)
    

main()