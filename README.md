# SecurityCam

Security camera system build on a Raspberry Pi platform.

### Basic Functions

The primary function of this system is to alert a user to activity near the area the device is set up.
The system works as follows:

- A camera uses OpenCV to detect if a person has entered its view frame
- Distance from the device to the subject is obtained
- If the subject is closer than a pre-defined threshold, the camera is tripped
- Once tripped, the camera saves an image of the subject
- Finally, the camera sends an email alert to the user, with the image attached

### Central Components

This project utilized the following hardware, in addition to the Raspberry Pi board itself:

- Raspberry Pi Camera Board V2.1
- HC-SR04 Ultrasonic Distance Sensor

Wiring for the HC-SR04 was performed on a breadboard, with help from this tutorial:
https://pimylifeup.com/raspberry-pi-distance-sensor/

### TODO

Finish README:
 - implementation notes
 - issues encountered
 - possible future developments
