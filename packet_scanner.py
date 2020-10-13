# Packet Scanner -- current build is IP and Windows only
# tested on Win10 Home + Python 3.8
#
# Displays packet information and saves packets as binary data 

import os
import sys
import socket 
import re
from multiprocessing import Process
import time


def showData(data):
    bit_data = ''
    
    for b in data:
        bitStr = ''
    
        for i in range(8):
            bitStr += str((b >> i) & 1)
    
        bit_data += bitStr[::-1]
    
    # print(bit_data) # DEBUG

    print()
    print("Version: {}".format(int(bit_data[0:4], 2)))
    print("IHL: {}".format(int(bit_data[4:8], 2)))
    print("DSCP: {}".format(int(bit_data[8:14], 2)))
    print("ECN: {}".format(int(bit_data[14:16], 2)))
    print("Total Length: {}".format(int(bit_data[16:32], 2))) # int() parses the string as is, resulting in big-endian form

def readPackets(conn):
    # for all eternity
    while True:
        # receive from socket
        packet = conn.recvfrom(65535) # returns tuple with (bytes, address of socket)
        
        showData(packet[0]) 
        # update packet number
            
        # display (optional?)
        # save to file (optional?)





if __name__ == '__main__':
    # get all local IP adresses with corresponding (human-readable, if available) NIC
    # request user input -- which IP / NIC to use

    # get NIC information (WMIC = WinXP Pro and later)
    cmd = "wmic nicconfig where dnshostname='{}' \
           get ipaddress, macaddress, description \
           2> nul".format(socket.gethostname()) # redirecting stderr to nul to prevent error output
    stream = os.popen(cmd)
    output = stream.read()
    stream.close()
    
    # remove headers
    lines = output.split('\n')
    lines = list(filter(None, lines))[1:]
    
    # make sure we have a NIC to work with
    if (not lines):
        print('No suitable network interfaces found. Exiting...')
        sys.exit() # 0 = default
    # one or more suitable interfaces found
    else:
        # parse interface list
        device_list = []
        
        for line in lines:
            name = re.search(r'([a-zA-Z]+\s)+', line).group()
            ipv4 = re.search(r'(?:\d{1,3}\.){3}\d{1,3}', line).group()
            mac = re.search(r'(?:(?:[A-Z0-9]){2}\:){5}(?:[A-Z]|[0-9]){2}', line).group()
            
            device = {'name' : name, 'ipv4' : ipv4, 'mac' : mac}
            device_list.append(device)    
          
        # skip selection if only one interface can be used
        if (len(device_list) == 1):
            selected_device = device_list[0]
        else:
            # print out interfaces we can use
            print("Suitable Network Interfaces:")
            print()
            
            line_number = 0
            for device in device_list:    
                ip = '{:<20}'.format(device.get('ipv4'))
                mac = '{:<20}'.format(device.get('mac'))
                name = '{:<20}'.format(device.get('name'))
                    
                print("({}) {ip} {mac} {name}".format(line_number, ip=ip, mac=mac, name=name))
                line_number += 1
            
            print()
            
            # ask the user which device to use
            choice = int(input("Choose a Network Interface to listen on: "))
            selected_device = device_list[choice]
            print()
            

    # create a raw socket and bind it to a random available port on chosen IP / NIC
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    conn.bind((selected_device.get('ipv4'), 0)) # bind on random available port

    # include the IP headers
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # enable promiscuous mode to forward all packets received
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # let user know how to stop the program
    print("To exit the program gracefully, press 'Enter'.")
    
    # display information for chosen interface
    msg = "Listening on: {}".format(selected_device.get('ipv4'))
    print(msg)
    print()
    
    # give user time to read the starting messages
    print("Starting in 5 seconds.")
    print("-" * len(msg))
    print()
    time.sleep(5)
    
    # open child process
    proc = Process(target=readPackets, args=(conn,))
    proc.start()
           
    # wait for user input to exit
    input()
    proc.kill()   
     
    # close socket
    conn.close()
    
    # exit
    sys.exit()