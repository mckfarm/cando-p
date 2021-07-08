
/***********************************************************************************
 *  Float switch level sensor for CANDO+P reactor
 *  Based on RobotGeek Aquarium Pump Refill tutorial and code
 *
 *  Wiring
 *  Pin 2 - Float Switch
 *  Pin 7 - LED
 *
 *  Control Behavior:
 *    If the float switch is not floating, keep LED off
 *    If the float switch is floating, turn on LED and write file
 *
 *  External Resources
 *
 ***********************************************************************************/
//define the input/output pins
#define FLOAT_SWITCH_PIN 2
#define LED_PIN 7

//setup runs once
void setup()
{
  //setup input pins for float switch 
  //Too use a bare switch with no external pullup resistor, set the pin mode to INPUT_PULLUP to use internal pull resistors. This will invert the standard high/low behavior
  pinMode(FLOAT_SWITCH_PIN, INPUT_PULLUP);
  
  //setup output pin for LED
  pinMode(LED_PIN, OUTPUT);

  //setup serial print for file generation if float switch is on
  Serial.begin(9600);
  
}

//loop() runs indefinitely 
void loop()
{
  // check to see the state of the float switch, high/low are inverted because of INPUT_PULLUP
  // FLOAT_SWITCH_PIN == HIGH indicates normal water levels
  if(digitalRead(FLOAT_SWITCH_PIN) == HIGH)
  {
     digitalWrite(LED_PIN, LOW);    //turn off LED
  }
  
  // FLOAT_SWITCH_PIN == LOW indicates high water level
  {
     digitalWrite(LED_PIN, HIGH);    //turn on LED
  }
}
