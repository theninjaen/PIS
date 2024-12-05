#define LED 4 //indicator, Grove - LED is connected with D4 of Arduino
boolean led_state = LOW; //state of LED, each time an external interrupt 
                         //will change the state of LED
unsigned char counter = 0; // Initialisation de counter
unsigned long temp[21]; // Changement de la taille du tableau
unsigned long sub;
bool data_effect = true;
unsigned int heart_rate; //the measurement result of heart rate

const int max_heartpluse_duty = 2000; //you can change it follow your system's request.
//2000 means 2 seconds. System return error 
//if the duty overtrip 2 second.

void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
    Serial.println("Please ready your chest belt.");
    delay(5000);
    arrayInit();
    Serial.println("Heart rate test begin.");
    attachInterrupt(digitalPinToInterrupt(2), interrupt, RISING); //set interrupt 0, digital port 2
}

void loop() {
    digitalWrite(LED, led_state); // Update the state of the indicator
}

/*Function: calculate the heart rate*/
void sum() {
    if (data_effect) {
        heart_rate = 1200000 / (temp[20] - temp[0]); // 60*20*1000/20_total_time 
        Serial.print("Heart_rate_is:\t");
        Serial.println(heart_rate);
    }
    data_effect = true; //sign bit
}

/*Function: Interrupt service routine. Get the signal from the external interrupt*/
void interrupt() {
    Serial.println("Interrupt triggered");
    temp[counter] = millis();
    Serial.print("Counter: ");
    Serial.println(counter, DEC);
    Serial.print("Time: ");
    Serial.println(temp[counter]);

    switch (counter) {
        case 0:
            sub = temp[counter] - temp[20];
            break;
        default:
            sub = temp[counter] - temp[counter - 1];
            break;
    }
    Serial.print("Sub: ");
    Serial.println(sub);

    if (sub > max_heartpluse_duty) { //set 2 seconds as max heart pulse duty
        data_effect = false; //sign bit
        counter = 0;
        Serial.println("Heart rate measure error, test will restart!");
        arrayInit();
    } else if (counter == 20 && data_effect) {
        counter = 0;
        sum();
    } else if (counter != 20 && data_effect) {
        counter++;
    } else {
        counter = 0;
        data_effect = true;
    }
}

/*Function: Initialization for the array(temp)*/
void arrayInit() {
    for (unsigned char i = 0; i < 20; i++) {
        temp[i] = 0;
    }
    temp[20] = millis();
}
