//Colby Rome 11-1-2015

#include <SDI12.h>

#define DATAPIN 9
SDI12 mySDI12(DATAPIN);

String meas = "?M!"; // measure command
String send = "?D0!"; // send data (back to host) command

void setup(){
    Serial.begin(9600);
    mySDI12.begin();
}

void loop(){
    /* Should generate new data at approximately 1 Hz.
    */
    mySDI12.sendCommand(meas);
    delay(400);
    mySDI12.sendCommand(send);
    delay(200);
    while(mySDI12.available()){
        Serial.write(mySDI12.read());
    }
    delay(200);
}
