#!/usr/bin/env python3

#Colby Rome 11-1-2015

import serial
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
import re

NUM_SECS = 300 # Size of time axis for graphing

def receiving(ser):
    ''' This function plots data from the SDI-12 sensor in realtime.
        Input: a valid instance of a serial class
        Output: a real-time plot of the data from an SDI-12 sensor
    '''

    new = True # Initialize graphs to initial y-values (not 0)
    plt.ion() # Interactive plot
    
    # Create lists for holding sensor data
    temp = [0]*NUM_SECS
    depth = [0]*NUM_SECS
    cond = [0]*NUM_SECS
    plt.figure(figsize=(10,10)) # Adjust the figsize

    # Temperature
    plt.subplot(311) # Divides figure into 3x1 grid
    plt.title('Current Decagon Sensor Readings')
    plt.xlabel('seconds')
    plt.ylabel('Temperature (C)')
    temp_x, = plt.plot(temp)
    # plot() returns a list of Line2D objects. The comma unpacks
    # the single value into temp_x.

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
        # Read from serial line; decode binary into ascii string
        parsed = parse_sdi12_line(ser.readline().decode('ascii'))

        # Example response from sensor (indicating depth, temp, conductivity);
        # 0+130+22.3+283 OR
        # 0-11+22.3+0 (This is invalid; cannot have negative depth)
        # The sensor specifies that physical damage will occur if the 
        # temperature is less than 0C, so we will not plot values <0.
        
        print('received: ', parsed)
        if len(parsed) == 3: # if valid string

            newDepth = -parsed[0]
            newTemp = parsed[1]
            newCond = parsed[2]
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

"""
parse SDI-12 measurements like the sample below.

tested with Python3.4

Alan Marchiori
2015

"""
__r = re.compile('(?:[\+-]\d+)(?:\.\d*)?')

sample = """+119+25.3+299
-119+25.3+296
+119+25.3-295
+119+25.3+298
+119-25.3+302
+118+25.3+297
+119+25.3+299
-118+25.3+299
+119-25.3+295"""

def parse_sdi12_line(s):
    """
    Parse a single line of measurements like: +119-25.3+302
    
    regex explained:
    (?:[\+-]\d+)(?:\.\d*)?
     ----------  -------                 
                 ?: create a non-capture group for the decimal part
                 \.\d* = a single decimal (. has to be escaped) followed by ZERO or more digits
                 the trailing ? after this non-capture group means the whole group is optional
     ?: create a non-capture group for the whole number part
     [\+-] matches either + or - (plus has to be escaped)
     \d+ matches ONE or more digits
     
    """
    return [float(i) for i in __r.findall(s)]

if __name__ == '__main__':
    # Modify the serial port as necessary
    # TODO: make the serial port a command line argument?
    ser = serial.Serial('/dev/ttyACM0', 9600);
    receiving(ser)

