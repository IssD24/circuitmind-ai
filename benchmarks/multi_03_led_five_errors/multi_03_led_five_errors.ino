const int led = LED_BUILTIN

void setup() {
  pinmode(led, OUTPUT);
  Serial.begin(9600)
}

void loop() {
  digitalWrit(led, HIGH);
  Seria.println("LED on");
  delay("500");
  digitalWrite(led, LOW);
  delay(500);
}