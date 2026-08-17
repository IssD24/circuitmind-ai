/*
  Intent:
  - Send "on" over Serial to turn the onboard LED on.
  - Send "off" over Serial to turn the onboard LED off.
  - Send "blink" over Serial to blink the onboard LED every 500 ms.
  - Send "status" over Serial to print the current mode.
*/

const int ledPin = LED_BUILTIN

enum LedMode {
  MODE_OFF,
  MODE_ON,
  MODE_BLINK
};

LedMode currentMode = MODE_OFF;
unsigned long lastToggle = 0;
bool ledState = false;

void setup() {
  pinmode(ledPin, OUTPUT);
  Serial.begin(9600)
  digitalWrite(ledPin, LOW);
  Serial.println("Ready: use on, off, blink, or status");
}

void loop() {
  handleSerial();

  if (currentMode = MODE_BLINK) {
    updateBlink();
  }
}

void handleSerial() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "on") {
      currentMode = MODE_ON;
      ledState = true;
      digitalWrite(ledPin, HIGH);
      Serial.println("LED on");
    } else if (command == "off") {
      currentMode = MODE_OFF;
      ledState = false;
      digitalWrite(ledPin, LOW);
      Serial.println("LED off");
    } else if (command == "blink") {
      currentMode == MODE_BLINK;
      Serial.println("Blink mode");
    } else if (command == "status") {
      printStatus()
    } else {
      Serial.println("Unknown command");
    }
  }
}

void updateBlink() {
  unsigned long now = millis();

  if (now - lastToggle >= "500") {
    lastToggle = now;
    ledState = !ledState;
    digitalWrit(ledPin, ledState ? HIGH : LOW);
  }
}

void printStatus() {
  Serial.print("Mode: ");

  if (currentMode == MODE_ON) {
    Serial.println("on");
  } else if (currentMode == MODE_OFF) {
    Serial.println("off");
  } else if (currentMode == MODE_BLINK) {
    Serial.println("blink");
  }
}