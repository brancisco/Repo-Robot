#include <Sparki.h>

#define EMPTY ' '
#define GRIP_OPEN 1
#define GRIP_CLOSED 0

char STATE;
int GRIPPER_STATE;


void setup() {
  sparki.servo(SERVO_CENTER);
  Serial.begin(9600);
  sparki.clearLCD();
}

void loop() {
  int obj_dist = sparki.ping();
  char inByte = EMPTY;
  if (Serial.available()){ // only send data back if data has been sent
    inByte = Serial.read();
  }
  if (inByte != EMPTY)
    STATE = inByte;
  sparki.print(STATE);
  sparki.updateLCD();
  sparki.clearLCD();
  if(STATE == '1') {
      sparki.print("Forward\n");
      sparki.updateLCD();
      sparki.moveForward();
   }
   if(STATE == '2') {
      sparki.print("Backward\n");
      sparki.updateLCD();
      sparki.moveBackward();
   }
   if(STATE == '3') {
      sparki.print("Right\n");
      sparki.updateLCD();
      sparki.moveRight();
   }
   if(STATE == '4') {
      sparki.print("Left\n");
      sparki.updateLCD();
      sparki.moveLeft();
   }
   if(STATE == '5') {
      sparki.print("Stop\n");
      sparki.updateLCD();
      sparki.moveStop();
   }
   if(STATE == '6') {
      sparki.print("Open Grip\n");
      sparki.updateLCD();
      sparki.gripperOpen(6);
   }
   if(STATE == '7') {
      sparki.print("Close Grip\n");
      sparki.updateLCD();
      sparki.gripperClose(3);
   }
   if(STATE == '8') {
      sparki.print("Following Line :)\n");
      // follow_line();
      sparki.updateLCD();
    }
    if(STATE == '9') {
      sparki.print("Repoing\n");
      sparki.println(obj_dist);
      sparki.updateLCD();
      if ((obj_dist < 11) && (obj_dist > 0)){
        sparki.print("GOT EM");
        sparki.updateLCD();
        sparki.moveStop();
        // beepboop();
        sparki.gripperClose(5);
        delay(4000);
        sparki.moveBackward();
        delay(3000);
        GRIPPER_STATE = GRIP_CLOSED;
        STATE = 't';
        }   
      else {
        sparki.moveForward();
        sparki.print("Too far!");
        sparki.updateLCD();
      }
  }
  if(STATE == 't') {
    sparki.print("Turning Around\n");
    sparki.updateLCD();
    sparki.motorRotate(MOTOR_LEFT, DIR_CCW, 100);
    sparki.motorRotate(MOTOR_RIGHT, DIR_CCW, 100);
    delay(5000);
    if(GRIPPER_STATE == GRIP_CLOSED) {
      sparki.clearLCD();
      sparki.moveStop();
      STATE = '8';
    }
    if(GRIPPER_STATE == GRIP_OPEN) {
      STATE = '8'; //change to different STATE later
    }  
  }

  if(STATE == 'd') {
    sparki.print("Bout to drop this car off a cliff, lol\n");
    sparki.updateLCD();
    sparki.moveForward(10);
    sparki.moveStop();
    sparki.gripperOpen(4);
    GRIPPER_STATE = GRIP_OPEN;
    sparki.print("YEET");
    sparki.updateLCD();
    sparki.moveStop();
    delay(500);
    STATE = 't';
  }
}



