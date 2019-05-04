# SecurityCam

Security camera system build on a Raspberry Pi platform.

## Basic Functions

The primary function of this system is to alert a user to activity near the area the device is set up.
The system works as follows:

- A camera uses OpenCV to detect if a person has entered its view frame
- Distance from the device to the subject is obtained
- If the subject is closer than a pre-defined threshold, the camera is tripped
- Once tripped, the camera saves an image of the subject
- Finally, the camera sends an email alert to the user, with the image attached

## Central Components

This project utilized the following hardware, in addition to the Raspberry Pi board itself:

- Raspberry Pi Camera Board V2.1
- HC-SR04 Ultrasonic Distance Sensor

Wiring for the HC-SR04 was performed on a breadboard, with help from this tutorial:
https://pimylifeup.com/raspberry-pi-distance-sensor/

## Implementation

The three most vital functions of this project are:

- The camera
- Emailing alerts
- Measuring distance

### Camera

TODO

### Emailing

TODO

### Distance

Measuring distance was performed by an HC-SR04 ultrasonic sensor, connected to the Raspberry Pi via GPIO pins.
Essentially, the sensor measured distance by putting a high value (corresponding to 1) through to the echo wire of the sensor.
Once this was done, the sensor waited until a return value was read from the receiver wire of the sensor.
Finally, the distance was determined based on the time it took for the echo to return to the sensor.
In order to increase the accuracy of the sensor's readings, a series of samples were used, rather than an individual reading.
In other words, the sensor would take several measurements, then average these results to produce the final distance.
This was done to reduce the chanmce of erroneous values and errors in the distance measurement. 

### Additional TODOs

Finish README:
 - issues encountered
 - possible future developments
