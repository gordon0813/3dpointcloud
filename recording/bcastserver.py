# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 09:53:11 2020

@author: gordon
"""


import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
message = b"your very important message"
while True:
    print("""input filename to start recording  
          \n input q to quit 
          \n input s to stop recording(not finish yet)
          \n input set <k> to set max recording time to k """)
    commend=input()
    message=commend.encode("utf-8")
    server.sendto(message, ('255.255.255.255', 37020))
    print("message sent!")
    #time.sleep(0.1)
    #server.sendto(message, ('<broadcast>', 37020))
    #print("message sent 2!")
    if(commend=="q"):
        print("end server section , goodbye")
        break