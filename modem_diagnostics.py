#!/usr/bin/env python3

import sys
import signal
import argparse
# Fails on Windows unless X-server is used
# If this line is commented, though, the script runs fine + W is not used anywhere
# from tkinter import W
from modem_interface import * 
import re

# setup handler for control-c to exit cleanly
def ctrl_handler(signum, frame):
    print("Ctrl-c was pressed.")
    atm.close()
    if log_file:
        log_file.write("\nCtrl-c was pressed.\n")
        log_file.close()
    sys.exit(0)

# Main
def main():
    # SERIAL_PORT = "/dev/ttyACM0"  # Raspberry Pi 2
    # BAUD = 115200
    SERIAL_PORT = None
    BAUD = None

    # get inputs
    parser=argparse.ArgumentParser()
    parser.add_argument('--port', default='', type=str, help='Serial port to use')
    parser.add_argument('--baud', default=115200, type=int, help='Baud rate to use')
    args=parser.parse_args()

    if args.baud:
        BAUD = args.baud

    if args.port:
        SERIAL_PORT = args.port
    else:
        sp = serial_ports()
        print('Select port:')
        for (i,s) in enumerate(sp):
            print('{} {}'.format(i,s))
        ind = int(input('> '))
        SERIAL_PORT = sp[ind]

    # Diagnostic Commands
    #atCommands = ['ATE0','ATI','AT+CGMI','AT+CGMM','AT+GMM','AT+CMEE=2', 'AT+CREG=2', 'AT+CGREG=2', 'AT+CEREG=3', 'AT+CGEREP=2,1', 'AT+CPIN?','AT+CCID','AT+CRSM=176,28539,0,0,12','AT+CFUN?','AT+CSQ','AT+CESQ','AT+CREG?','AT+CGREG?','AT+CEREG?','AT+CGDCONT?','AT+CGACT?','AT+COPS?','AT+COPS=?']
    atCommands = ['ATE0','ATI','AT+CGMI','AT+CGMM','AT+GMM','AT+CMEE=2', 'AT+CREG=2', 'AT+CGREG=2', 'AT+CEREG=3', 'AT+CGEREP=2,1', 'AT+CPIN?','AT+CCID','AT+CRSM=176,28539,0,0,12','AT+CFUN?','AT+CSQ','AT+CESQ','AT+CREG?','AT+CGREG?','AT+CEREG?','AT+CGDCONT?','AT+CGACT?','AT+COPS?']

    # Create and open modem interface
    atm = ATManager(print_debug=True)

    # Save to file
    file_name = 'ModemDiagnostics.txt'
    log_file = open(file_name, 'w')

    signal.signal(signal.SIGINT, ctrl_handler)

    print('\n---------------\nConnecting to modem ...')
    while True:
        try:
            atm.open(SERIAL_PORT, BAUD)
            break
        except:
            time.sleep(.1)
            pass

    while atm.isOpen():
        atm.set_cmd('AT')
        reply = atm.wait_for_rx(log_file=log_file)
        #print(reply)
        #print(reply[-1])
        #print('OK' in reply)
        if reply is None or len(reply) == 0:
            time.sleep(1)
        elif 'OK' in reply[-1]:
            break

    # the COPS=? command can take several minutes
    atm.set_msg_timeout( 300 )
    for cmd in atCommands:
    	atm.set_cmd(cmd)
    	atm.wait_for_rx(log_file=log_file)
    	log_file.write('-----\r\n')
    	print('-----\r\n')

    # How you can parse out ICCID
    atm.set_cmd('AT+QCCID')
    reply = atm.wait_for_rx(log_file=log_file)
    print('----')
    if len(reply) >= 2 and reply[1] == 'OK':
        x = re.findall('[0-9]+', reply[0])
        print(x)
    else:
        print('Invalid reponse!')

    # close interfaces
    log_file.close()
    atm.close()

    print("Good bye!")

# Python stuff
if __name__ == '__main__':
    main()