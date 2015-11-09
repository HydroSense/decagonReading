#!/usr/bin/env python3

#Colby Rome 11-1-2015

import serial
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
import re

NUM_SECS = 300 # Time axis of graphs

def receiving(ser):
    ''' This function plots data from the SDI-12 sensor
    '''
    new = True # Initialize graphs to initial y-values (not 0)
    plt.ion() # Interactive plot
    temp = [0]*NUM_SECS
    depth = [0]*NUM_SECS
    cond = [0]*NUM_SECS
    plt.figure(figsize=(10,10)) # Adjust the figsize

    # Temperature
    plt.subplot(311)
    plt.title('Current Decagon Sensor Readings')
    plt.xlabel('seconds')
    plt.ylabel('Temperature (C)')
    temp_x, = plt.plot(temp)

    # Depth
    plt.subplot(312)
    plt.xlabel('seconds')
    plt.ylabel('Depth (mm)')
    depth_x, = plt.plot(depth)

    # Conductivity
    plt.subplot(313)
    plt.xlabel('seconds')
    plt.ylabel('Conductivity (dS/m)')
    cond_x, = plt.plot(cond)

    while True:
        # Read from serial line; decode into ascii string
        last_received = ser.readline().decode('ascii')

        # Example response from sensor:
        # 0+130+22.3+283 OR
        # 0-11+22.3+0 (This is invalid; can't have negative depth)
        
        # regex matching expression:
        # ^[0][+-][0-9]+[+-][0-9]+.[0-9][+-][0-9]+

        p = re.compile('^[0][+][0-9]+[+-][0-9]+.[0-9][+-][0-9]+')
        match = p.match(last_received)
        print('received: ', last_received)
        if match is not None: # If received valid string
            print(last_received.split('+'))
            newTemp = float(last_received.split('+')[2])
            print(last_received.split('+')[2])
            newDepth = -float(last_received.split('+')[1]) 
            print(last_received.split('+')[1])
            newCond = float(last_received.split('+')[3].split('\\')[0])
            print(last_received.split('+')[3].split('\\')[0])
            if(new == True): # only occurs once
                # This is to initialize the y-values to the initial readings
                new = False
                temp = [newTemp]*NUM_SECS
                depth = [newDepth]*NUM_SECS
                cond = [newCond]*NUM_SECS

            # Append the new readings to the list. This is operating as
            # a circular buffer
            temp.append(newTemp)
            del temp[0]
            depth.append(newDepth)
            del depth[0]
            cond.append(newCond)
            del cond[0]

            # Define appropriate range for each graph
            minTemp=float(min(temp))-1
            maxTemp=float(max(temp))+1
            minDepth = float(min(depth))-7
            maxDepth = float(max(depth))+7
            minCond = float(min(cond))-50
            maxCond = float(max(cond))+50

            # Temperature
            plt.subplot(311)
            plt.ylim([minTemp,maxTemp])
            temp_x.set_xdata(np.arange(len(temp)))
            temp_x.set_ydata(temp)

            # Depth
            plt.subplot(312)
            plt.ylim([minDepth,maxDepth])
            depth_x.set_xdata(np.arange(len(depth)))
            depth_x.set_ydata(depth)

            # Conductivity
            plt.subplot(313)
            plt.ylim([minCond,maxCond])
            cond_x.set_xdata(np.arange(len(cond)))
            cond_x.set_ydata(cond)
            
            #Draw to the screen
            plt.draw()

if __name__ == '__main__':
    # Modify the serial port as necessary
    ser = serial.Serial('/dev/ttyACM0', 9600);
    receiving(ser)
