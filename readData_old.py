#!/usr/bin/env python3

#Colby Rome 11-1-2015

import serial
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
import re

NUM_SECS = 300

def receiving(ser):
    new = True
    global last_received
    buffer_string = ''
    plt.ion()
    temp = [0]*300
    depth = [0]*300
    cond = [0]*300
#    plt.figure(1)
    plt.figure(figsize=(10,10))

    plt.subplot(311)
    plt.title('Current Sensor Readings')
    plt.xlabel('seconds')
    plt.ylabel('Temperature (C)')
    temp_x, = plt.plot(temp)

    plt.subplot(312)
    plt.xlabel('seconds')
    plt.ylabel('Depth (mm)')
    depth_x, = plt.plot(depth)

    plt.subplot(313)
    plt.xlabel('seconds')
    plt.ylabel('Conductivity (dS/m)')
    cond_x, = plt.plot(cond)

    while True:
        #        last_received = str(ser.readline())
        last_received = ser.readline().decode('ascii')
        # Example response from sensor:
        # 0+130+22.3+283 OR
        # 0-11+22.3+0
        # regex matching expression:
        # ^[0][+-][0-9]+[+-][0-9]+.[0-9][+-][0-9]+
        p = re.compile('^[0][+-][0-9]+[+-][0-9]+.[0-9][+-][0-9]+')
        print('match: ', p.match(ser.readline().decode('ascii')))
        print('received: ', last_received)
        if '+' in last_received:
            if len(last_received.split('+')) > 3:
                print(last_received.split('+'))
                newTemp = float(last_received.split('+')[2])
                print(last_received.split('+')[2])
                newDepth = -float(last_received.split('+')[1])
                print(last_received.split('+')[1])
                newCond = float(last_received.split('+')[3].split('\\')[0])
                print(last_received.split('+')[3].split('\\')[0])
                if(new == True):
                    new = False
                    temp = [newTemp]*NUM_SECS
                    depth = [newDepth]*NUM_SECS
                    cond = [newCond]*NUM_SECS

                temp.append(newTemp)
                del temp[0]
                depth.append(newDepth)
                del depth[0]
                cond.append(newCond)
                del cond[0]

                minTemp=float(min(temp))-1
                maxTemp=float(max(temp))+1
                minDepth = float(min(depth))-7
                maxDepth = float(max(depth))+7
                minCond = float(min(cond))-50
                maxCond = float(max(cond))+50

                plt.subplot(311)
                plt.ylim([minTemp,maxTemp])

                plt.subplot(312)
                plt.ylim([minDepth,maxDepth])

                plt.subplot(313)
                plt.ylim([minCond,maxCond])
                
                temp_x.set_xdata(np.arange(len(temp)))
                temp_x.set_ydata(temp)
                depth_x.set_xdata(np.arange(len(depth)))
                depth_x.set_ydata(depth)
                cond_x.set_xdata(np.arange(len(cond)))
                cond_x.set_ydata(cond)
                plt.draw()

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600);
    receiving(ser)
