void blinkLed(int pin) {
  digitalWrite(pin, HIGH);
  delay(500);
  digitalWrite(pin, LOW);
  delay(500);
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  blinkLed();
}