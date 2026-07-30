void setup() {
  Serial.begin(9600);
}

void loop() {
  std::vector<int> values;
  values.push_back(1);

  Serial.println(values.size());
  delay(1000);
}