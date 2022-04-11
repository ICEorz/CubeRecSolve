int cnt = 1;
void setup() {
    for (int i = 2; i < 6; i++) {
        pinMode(i, OUTPUT);
    }
}

void clockwise(int num) {
    for (int cnt = 0; cnt < num; cnt++) {
        for (int i = 2; i < 6; i++) {
            digitalWrite(i, HIGH);
            delay(4);
            digitalWrite(i, LOW);
        }
    }
}

void anticlockwise(int num) {
    for (int cnt = 0; cnt < num; cnt++) {
        for (int i = 5; i > 1; i--) {
            digitalWrite(i, HIGH);
            delay(10);
            digitalWrite(i, LOW);
        }
    }
}

void loop() {
    if (cnt > 0) {
        clockwise(512);
        cnt --;
    }
    // delay(10);
    // anticlockwise(512);
}