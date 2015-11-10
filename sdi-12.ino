//Colby Rome 11-1-2015

#include <SDI12.h>

#define DATAPIN 9
SDI12 mySDI12(DATAPIN);

String meas = "0M!"; // measure command
String send = "0D0!"; // send data (back to host) command

void setup(){
    Serial.begin(9600);
    mySDI12.begin();
    delay(1000);
}

void loop(){
    /* Should generate new data at approximately 1 Hz.
    */
    mySDI12.sendCommand(meas);
    int c;
    while((c = waitAndRead()) != '\n');
    //Next character
    while(waitAndRead() != '0');
    
    mySDI12.sendCommand(send);

    while((c = waitAndRead()) != '0');

    while((c = waitAndRead()) != '\n'){
        Serial.write(c);
    }
    Serial.println();
    delay(400); // Adjust to generate new data at ~1 Hz.
}

int waitAndRead()
{
    while(mySDI12.available() == 0) 
        delay(50); // needed due to software serial. Allows time for interrupts
    return mySDI12.read();
}
