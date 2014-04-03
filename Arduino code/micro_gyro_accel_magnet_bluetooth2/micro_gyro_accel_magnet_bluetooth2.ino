/********************************************************************************
* ADXL345 Library Examples- pitch_roll.ino                                      *
*                                                                               *
* Copyright (C) 2012 Anil Motilal Mahtani Mirchandani(anil.mmm@gmail.com)       *
*                                                                               *
* License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html> *
* This is free software: you are free to change and redistribute it.            *
* There is NO WARRANTY, to the extent permitted by law.                         *
*                                                                               *
*********************************************************************************/

#include <Wire.h>
#include <ADXL345.h>  //accelerometer
#include <L3G.h>  //gryo
#include <HMC5883L.h>  //compass


const float alpha = 0.5;

double fXg = 0;
double fYg = 0;
double fZg = 0;

L3G gyro;
ADXL345 acc;
HMC5883L compass;

// Record any errors that may occur in the compass.
int error = 0;

void setup() {
    Wire.begin();
//    Serial.begin(9600);
    Serial1.begin(9600); //bluetooth
//      while (!Serial) {
//    ; // wait for serial port to connect. Needed for Leonardo only
//  }
        while (!Serial1) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
    
    //Accelerometer setup
    acc.begin();
    
    //Gyro Setup
    if (!gyro.init())
    {
      Serial1.println("Failed to autodetect gyro type!");
//      Serial.println("Failed to autodetect gyro type!");
      while (1);
    }
    gyro.enableDefault();
         // while the serial stream is not open, do nothing:
    
    //Magnetometer setup
     error = compass.SetScale(1.3); // Set the scale of the compass.
     error = compass.SetMeasurementMode(Measurement_Continuous); // Set the measurement mode to Continuous
    
    
//        Serial.println("start");
//	delay(500);
}


void loop(){
  //read from the accelerometer and print to Serial as x,y,z
  
	double  Xg, Yg, Zg;
	acc.read(&Xg, &Yg, &Zg);
        

	//Low Pass Filter
	fXg = Xg * alpha + (fXg * (1.0 - alpha));
	fYg = Yg * alpha + (fYg * (1.0 - alpha));
	fZg = Zg * alpha + (fZg * (1.0 - alpha));
//        Serial.print("{'accel':(");
//        Serial.print(fXg);
//        Serial.print(",");
//        Serial.print(fYg);
//        Serial.print(",");
//        Serial.print(fZg);
//        Serial.print(")");
//        
        Serial1.print("{'accel':(");
        Serial1.print(fXg);
        Serial1.print(",");
        Serial1.print(fYg);
        Serial1.print(",");
        Serial1.print(fZg);
        Serial1.print(")");
        
        gyro.read();
//        Serial.print(",'gyro':(");
//        Serial.print((int)gyro.g.x);
//        Serial.print(",");
//        Serial.print((int)gyro.g.y);
//        Serial.print(",");
//        Serial.print((int)gyro.g.z);
//        Serial.print(")");
        
        Serial1.print(",'gyro':(");
        Serial1.print((int)gyro.g.x);
        Serial1.print(",");
        Serial1.print((int)gyro.g.y);
        Serial1.print(",");
        Serial1.print((int)gyro.g.z);
        Serial1.print(")");
        
        MagnetometerScaled scaled = compass.ReadScaledAxis();
//        Serial.print(",'magnet':(");
//        Serial.print(scaled.XAxis);
//        Serial.print(",");   
//        Serial.print(scaled.YAxis);
//        Serial.print(",");   
//        Serial.print(scaled.ZAxis);
//        Serial.print(")}");
        
        Serial1.print(",'magnet':(");
        Serial1.print(scaled.XAxis);
        Serial1.print(",");   
        Serial1.print(scaled.YAxis);
        Serial1.print(",");   
        Serial1.print(scaled.ZAxis);
        Serial1.print(")}");
        
//        Serial.println();
        Serial1.println();   
        
        
	delay(100);

}
