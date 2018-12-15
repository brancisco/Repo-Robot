#include <Sparki.h>
#include "pitches.h"

#define GRIP_OPEN 1
#define GRIP_CLOSED 0

char state = '1'; 
int gripper_state;

int threshold = 400;
int lineLeft   = sparki.lineLeft();  
int lineCenter = sparki.lineCenter(); 
int lineRight  = sparki.lineRight();
  
void setup() {
  sparki.servo(SERVO_CENTER);
//  sparki.gripperOpen(4);
  gripper_state = GRIP_OPEN;
  Serial.begin(9600); // set the baud rate
//  sparki.print("I'm ready :D"); //verify that Sparki is set up
  sparki.clearLCD();
  sparki.updateLCD();
}

//void beepboop() {
//int melody[] = { NOTE_FS6, NOTE_C7, NOTE_FS6, NOTE_C7, NOTE_FS6, NOTE_C7, NOTE_FS6, NOTE_C7, NOTE_FS6, NOTE_C7 };
//int noteDurations[] = { 4, 4, 4, 4, 4, 4, 4, 4, 4, 4 };
//for (int thisNote = 0; thisNote < 8; thisNote++) {
//  if(thisNote % 2 == 0){
//    sparki.RGB(RGB_RED);
//    }
//    else {
//      sparki.RGB(RGB_BLUE);
//      }
//      int noteDuration = 1000/noteDurations[thisNote];
//      sparki.beep(melody[thisNote],noteDuration);
//      int pauseBetweenNotes = noteDuration * 1.30;
//      delay(pauseBetweenNotes);
//      // stop the tone playing:
//      sparki.noBeep();
//      sparki.RGB(RGB_OFF);
//      }
//}

void follow_line() {  
  sparki.moveForward();
  if ( lineLeft < threshold ){  
    sparki.moveLeft();
  }
 
  if ( lineRight < threshold ){  
    sparki.moveRight(); 
  }
 
  if ( (lineCenter < threshold) && (lineLeft > threshold) && (lineRight > threshold) ){
    sparki.moveForward();
  }  
  if ( (lineCenter < threshold) && (lineLeft < threshold) && (lineRight < threshold) ){
    sparki.moveLeft(90);
    state = 'd';
  }  
}

void find_line() {
   sparki.moveForward();
   if (lineLeft < threshold || lineCenter < threshold || lineRight < threshold) {
      sparki.moveStop();
      if (lineLeft < threshold && lineCenter < threshold && lineRight < threshold) {
        sparki.moveRight(15);
      }
   }
}


void loop() {
//  sparki.clearLCD();
  int obj_dist = sparki.ping();
//  Serial1.println("Hello World");
  delay(1000);
  char inByte = ' ';
  if(Serial.available()){ // only send data back if data has been sent
    inByte = Serial.read(); // read the incoming data
  }
//    sparki.print(inByte); // send the data back in a new line so that it is not all one long line
//    sparki.print(' ');
//    sparki.updateLCD();
    sparki.clearLCD();
    sparki.print("Dist: ");
    sparki.println(obj_dist);
    sparki.print("State: ");
    sparki.println(state);
    sparki.updateLCD();
    if (inByte != ' ') {
      state = inByte;
    }
    if(state == '1') {
      sparki.print("Forward\n");
      sparki.updateLCD();
      sparki.moveForward();
   }
   if(state == '2') {
      sparki.print("Backward\n");
      sparki.updateLCD();
      sparki.moveBackward();
   }
   if(state == '3') {
      sparki.print("Right\n");
      sparki.updateLCD();
      sparki.moveRight();
   }
   if(state == '4') {
      sparki.print("Left\n");
      sparki.updateLCD();
      sparki.moveLeft();
   }
   if(state == '5') {
      sparki.print("Stop\n");
      sparki.updateLCD();
      sparki.moveStop();
   }
   if(state == '6') {
      sparki.print("Open Grip\n");
      sparki.updateLCD();
      sparki.gripperOpen(6);
   }
   if(state == '7') {
      sparki.print("Close Grip\n");
      sparki.updateLCD();
      sparki.gripperClose(3);
   }
  if(state == '8') {
      sparki.print("Following Line :)\n");
      follow_line();
      sparki.updateLCD();
  }
  if(state == '9') {
      sparki.print("Repoing\n");
      sparki.println(obj_dist);
      sparki.updateLCD();
      if ((obj_dist < 11) && (obj_dist > 0)){
        sparki.print("GOT EM");
        sparki.updateLCD();
        sparki.moveStop();
//        beepboop();
        sparki.gripperClose(5);
        delay(4000);
        sparki.moveBackward();
        delay(3000);
        gripper_state = GRIP_CLOSED;
        state = 't';
        }   
      else {
        sparki.moveForward();
        sparki.print("Too far!");
        sparki.updateLCD();
      }
  }
  if(state == 't') {
      sparki.print("Turning Around\n");
      sparki.updateLCD();
      sparki.motorRotate(MOTOR_LEFT, DIR_CCW, 100);
      sparki.motorRotate(MOTOR_RIGHT, DIR_CCW, 100);
      delay(5000);
      if(gripper_state == GRIP_CLOSED) {
        sparki.clearLCD();
        sparki.moveStop();
        state = '8';
      }
      if(gripper_state == GRIP_OPEN) {
        state = '8'; //change to different state later
       }  
  }

  if(state == 'd') {
    sparki.print("Bout to drop this car off a cliff, lol\n");
    sparki.updateLCD();
    sparki.moveForward(10);
    sparki.moveStop();
    sparki.gripperOpen(4);
    gripper_state = GRIP_OPEN;
    sparki.print("YEET");
    sparki.updateLCD();
    sparki.moveStop();
    state = 't';
    }
    
  delay(100); 
}
