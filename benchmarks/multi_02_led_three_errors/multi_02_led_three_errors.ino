const int led = LED_BUILTIN

void setup() {
  pinMode(led OUTPUT);
}

void loop() {
  digitalWrite(led);
  delay(500);
}