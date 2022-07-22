
/***********************************************************************************
 *  Level sensor and N2O analog input set up for CANDO+P reactor
 *  Level sensor based on RobotGeek Aquarium Pump Refill tutorial and code
 *  N2O analog input sensor based on http://tinkeringpete.blogspot.com/2016/11/arduino-4-20-ma-input.html
 *
 *  Wiring
 *  Digital pin 2 - Float Switch
 *  Digital pin 7 - LED
 *  Analog pin 0 - N2O input
 *
 *  Control Behavior:
 *    If the float switch is not floating, keep LED off
 *    If the float switch is floating, turn on LED and write file

 ***********************************************************************************/
//define the input/output pins
#define FLOAT_SWITCH_PIN 2
#define LED_PIN 7
float N2O_READING;
float N2O_MAX = 50; //max N2O based on sensor head
float N2O_MIN = 0; //min N2O based on sensor head

//setup runs once
void setup()
{

  Serial.begin(9600);
  Serial.println("Time, Water level, N2O raw, N2O calc");
  
  //setup input pins for float switch 
  //Too use a bare switch with no external pullup resistor, set the pin mode to INPUT_PULLUP to use internal pull resistors. This will invert the standard high/low behavior
  pinMode(FLOAT_SWITCH_PIN, INPUT_PULLUP);
  
  //setup output pin for LED
  pinMode(LED_PIN, OUTPUT);
  
}

//loop() runs indefinitely 
void loop()
{
  delay(10000);
  Serial.print(millis());
  Serial.print(",");
  // check to see the state of the float switch, high/low are inverted because of INPUT_PULLUP
  // FLOAT_SWITCH_PIN == HIGH indicates normal water levels
  if(digitalRead(FLOAT_SWITCH_PIN) == HIGH)
  {
     digitalWrite(LED_PIN, LOW);    //turn off LED
     Serial.print("normal");
     Serial.print(",");
  }

  else
  // FLOAT_SWITCH_PIN == LOW indicates high water level
  {
     digitalWrite(LED_PIN, HIGH);    //turn on LED;
     Serial.print("high");
     Serial.print(",");
  }
  N2O_READING = analogRead(A0);
  Serial.print(N2O_READING);
  Serial.print(",");
  
  N2O_READING = (N2O_MAX-N2O_MIN)*N2O_READING/1023;
  Serial.println(N2O_READING);
}
