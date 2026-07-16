void setup() {
  Serial.begin(9600);
}

void loop() {
  DynamicJsonDocument doc(1024);
  doc["message"] = "hello";
  serializeJson(doc, Serial);
  delay(1000);
}