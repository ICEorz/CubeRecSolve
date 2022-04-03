 #include <SoftwareSerial.h>

 SoftwareSerial
 softSerial(7, 8);

void setup() {
    Serial.begin(9600);
     softSerial.begin(9600);
}

 void loop() {
     if (softSerial.available()) {
         int k = softSerial.read();
         Serial.println(k);
     }
 }
