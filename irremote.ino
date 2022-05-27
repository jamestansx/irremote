#define DEBUG true 
#define DECODE_NEC
#define MAX_TIME 150
#define RECV_PIN 7

#include <Arduino.h>
#include <IRremote.hpp>

bool useSysVol = false;
unsigned long lastPressTime = millis();

void sendCommand(char* command, bool lockPressDown = false){ 
    if (lockPressDown){
        //Serial.print("locked: ");
        if (millis() - lastPressTime > MAX_TIME) Serial.println(command);
        lastPressTime = millis();
    }
    else {
        //Serial.print("unlocked: ");
        Serial.println(command);
    }
}
    
void setup() {
    Serial.begin(115200);
    IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);
    Serial.print("Ready to receive IR signals of protocols: ");
    printActiveIRProtocols(&Serial);
    Serial.println(String("at pin " + String(RECV_PIN)));
}

void loop() {
    if (IrReceiver.decode()) {
        if (IrReceiver.decodedIRData.protocol != UNKNOWN){ 
            if (DEBUG) IrReceiver.printIRResultShort(&Serial);
            switch (IrReceiver.decodedIRData.command) {
                case 0x7    : 
                    if (useSysVol) sendCommand("SYSVOLDOWN");
                    else sendCommand("VOLDOWN");
                    break;
                case 0x9    : useSysVol = !useSysVol;           break;
                case 0x15   : 
                    if (useSysVol) sendCommand("SYSVOLUP");
                    else sendCommand("VOLUP");
                    break;
                case 0x40   : sendCommand("FASTF");             break;
                case 0x43   : sendCommand("PLAY", true);        break;
                case 0x44   : sendCommand("REWIND");            break;
                case 0x16    : sendCommand("FULLSCREEN", true);  break;
                default     :                                   break;
            }
        }
        IrReceiver.resume();
    }
}


