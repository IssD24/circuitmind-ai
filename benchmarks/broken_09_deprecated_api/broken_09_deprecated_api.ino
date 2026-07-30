void setup() {
  Serial.begin(9600);
}

void loop() {
  byte value = 300;
  Serial.println(value);
  delay(1000);
}