# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 09:53:36 2020

@author: gordon
"""
import socket
import pyrealsense2 as rs
import time
realsense_ctx = rs.context()
pipeline_1 =[]
config_1=[]
connected_devices = []
for i in range(len(realsense_ctx.devices)):
    detected_camera = realsense_ctx.devices[i].get_info(rs.camera_info.serial_number)
    connected_devices.append(detected_camera)
print("connected device : ",connected_devices)
for i in connected_devices:
    config_new = rs.config()
    config_new.enable_device(i)
    config_new.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config_new.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)
    config_1.append(config_new) 
    pipeline_1.append(rs.pipeline())
def initconfig(connected_devices,config):
    for i in connected_devices:
        config_new = rs.config()
        config_new.enable_device(i)
        config_new.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config_new.enable_stream(rs.stream.infrared, 1280, 720, rs.format.y8, 30)
        config.append(config_new)
    
def record(conf1,pipeline_1,filename1,maxtime):
    for i in range(len(conf1)):
        conf1[i].enable_record_to_file(filename1[i]+".bag")
        pipeline_1[i].start(conf1[i])
    start = time.time()
    while True:
        for pip in pipeline_1:
            frames=pip.wait_for_frames()
        print (time.time()-start)
        if(time.time()-start>maxtime):
            break
    for pip in pipeline_1:
        pip.stop()

maxtime=8
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))
recvstring=""
beforeStr=""
while True:
    print("waiting for commend to start recording...")
    # Thanks @seym45 for a fix
    data, addr = client.recvfrom(1024)
    beforeStr=recvstring
    recvstring=data.decode("utf-8")
    if(beforeStr==recvstring):
        print("should not use same filename...")
        continue
    if(recvstring=="q"):
        print("end client section ,goodbye")
        break
    spl=recvstring.split()
    if(spl[0]=="set"):
        maxtime=int(spl[1])
        print("set max recording time to : ",maxtime)
        continue
    print("received message: ",recvstring)
    record(config_1,pipeline_1,[recvstring+"c1",recvstring+"c2"],maxtime)
    
