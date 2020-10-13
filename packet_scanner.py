# Packet Scanner -- current build is IP and Windows only
# tested on Win10 Home + Python 3.8
#
# Displays packet information and saves packets as binary data 

import os
import socket 
import re


if __name__ == '__main__':
    pass

# get all local IP adresses with corresponding (human-readable, if available) NIC
# request user input -- which IP / NIC to use
    # get NIC information (WMIC = WinXP Pro+)
    stream = os.popen("wmic nicconfig where dnshostname='{}' get ipaddress, macaddress, description".format(socket.gethostname()))
    output = stream.read()
    
    # remove headers
    lines = output.split('\n')
    lines = list(filter(None, lines))[1:]
    
    # parse interface list
    device_list = []
    
    for line in lines:
        name = re.search(r'([a-zA-Z]+\s)+', line).group()
        ipv4 = re.search(r'(?:\d{1,3}\.){3}\d{1,3}', line).group()
        mac = re.search(r'(?:(?:[A-Z0-9]){2}\:){5}(?:[A-Z]|[0-9]){2}', line).group()
        
        device = {'name' : name, 'ipv4' : ipv4, 'mac' : mac}
        device_list.append(device)    
      
    # print out interfaces we can use  
    ''' TODO: check whether we have any interfaces
        and don't ask for input if we only have one '''
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
    print()
    
    # display information for chosen interface
    print("Listening on: {}".format(device_list[choice].get('ipv4')))


# create a raw socket and bind it to a random available port on chosen IP / NIC

# include the IP headers

# enable promiscuous mode to forward all packets received
    
# open child process
    # for all eternity
        # receive from socket
        
        # update packet number
            
        # display (optional?)
        # save to file (optional?)
            
# wait for user input to exit
# close socket
# exit