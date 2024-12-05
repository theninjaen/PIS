#include "HX711.h" //This library can be obtained here http://librarymanager/All#Avia_HX711

#define LOADCELL_DOUT_PIN  4
#define LOADCELL_SCK_PIN  3

int HEART_RATE_PIN = 2;

HX711 scale;

float calibration_factor = -7050; // -7050 worked for my 440lb max scale setup

void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale();
  scale.tare();  // Reset the scale to 0
  scale.set_scale(calibration_factor); // Adjust to this calibration factor

  pinMode(HEART_RATE_PIN, INPUT);
}

void loop() {
  float weight = scale.get_units();  // Get the weight reading
  int beat = digitalRead(HEART_RATE_PIN);
  // // Print the weight as a readable number
  // Serial.print("Weight: ");
  // Serial.print(weight);
  // Serial.println(" kg");  // Assuming the weight is in kilograms

  Serial.print("Weight: ");
  Serial.print(scale.get_units(), 1);
  Serial.print(" Heartbeat: ");
  Serial.println(beat);
  
  delay(1000/30);  // Add a delay to control the rate of data sending
}
