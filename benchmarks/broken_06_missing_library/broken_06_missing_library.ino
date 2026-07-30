#include <ArduinoJson.h>

void setup() {
  Serial.begin(9600);
}

void loop() {
  JsonDocument doc;
  doc["message"] = "hello";
  serializeJson(doc, Serial);
  Serial.println();
  delay(1000);
}