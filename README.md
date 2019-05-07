# SecurityCam

Security camera system build on a Raspberry Pi platform.

Developed by:
  - Cristopher Hernandez cristopherh@csu.fullerton.edu
  - Duy Do duy.ado@csu.fullerton.edu

For CPSC-440 Computer System Architecture

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

## Implementation

The three most vital functions of this project are:

- The camera
- Emailing alerts
- Measuring distance

### Camera

The camera's computer vision functions were enabled through OpenCV. This allowed the camera to detect if a person had entered the frame, and subsequently activate. Interfacing with the camera was primarily done through the PiCamera library, which provides methods for controling the camera module.

### Emailing

To simplify the process of emailing and future customization we wrote a Mail class. Mail are sent using the email, smtplib, and ssl modules that come standard on python. The Mail class crudentials can be implicitly setup with an accounts for automation or exlicitly on the terminal for each use. The Mail class supports both standard planintext or HTML mail, both verision will be attached if HTML mail option is checked. The Mail class also supports multiple attachments of any file type, attachments must reside within the same folder or an absolute path is needed.

### Distance

Measuring distance was performed by an HC-SR04 ultrasonic sensor, connected to the Raspberry Pi via GPIO pins.
Essentially, the sensor measured distance by putting a high value (corresponding to 1) through to the echo wire of the sensor.
Once this was done, the sensor waited until a return value was read from the receiver wire of the sensor.
Finally, the distance was determined based on the time it took for the echo to return to the sensor.
In order to increase the accuracy of the sensor's readings, a series of samples were used, rather than an individual reading.
In other words, the sensor would take several measurements, then average these results to produce the final distance.
This was done to reduce the chanmce of erroneous values and errors in the distance measurement. 

## Issues Faced

While working on this project, we encountered several issues which had to be discussed and overcome.

###  Using OpenCV

Using OpenCV made the computer vision aspect of this projec much easier, but it still came with its own issues. First, installing OpenCV on the Raspberry Pi took some exploration. We eventually found packages for both Python 2 and 3, and then settled on using Python 3. Next, there was the issue of how to feed the camera data into the OpenCV models. While OpenCV has its own functions and methods for accessing cameras, these did not seem to be readily compatible with the Raspberry Pi's camera module. As a result, we eventually had to use an infinite iteration on the camera's frames (from the PiCamera method "capture_continuous") to read in each frame manually. Luckily, the Raspberry Pi is still fast enough to handle the data, so it doesn't provide too many noticeable hitches.

### Triggering The Email

A couple of different methods were tried for triggering the sending of the alert email. At first, the idea was to use a "scan" approach. Simply put, the Raspberry Pi would "scan" the area every few seconds with the distance sensor, then activate the camera component when something gets too close. Following this, the Raspberry Pi would use OpenCV to check if the object was a person, then send the email if it was. However, this approach was not as effective as originally thought. This made the camera more difficult to trigger, and made it such that one couldn't easily view what the Raspberry Pi sees through its camera (since the camera only activates after the distance sensor is tripped). As a result, we ended up reversing this logic. In the current implementation, the camera uses OpenCV to check for people in its current frame of view. If a person is detected, the camera activates its distance sensor to see if the person is close. If they are within a threshold, then the camera takes a snapshot and sends an email alert. This method proved easier to use, and more predictable in testing.

## Possible Future Developments

We have considered several ideas for future features or improvements which could be made to this project.

#### Graphical Interface

A graphical interface would make setting up and modifying the camera application much easier. Currently, the camera must be launched and configured entirely from the command line.

#### Recording Video After Detection

The camera would be even more useful if it could record short videos following activation. The initial version only takes static pictures.

#### Live Feed on Mobile or Web

It would be very convenient if a user could look at the camera's view at any time. A mobile app or web page which provides this would be very effective at making the camera more useful.

#### Remote Commands

An idea we have had is to allow the camera to process commands by reading in responses to its alerts. Essentially, a user could respond to an alert and tell the camera to take some action. This action could be any number of things, such as: contacting an additional person or the authorities, recording for longer, taking more screenshots, etc.

## Credits

Haar Casacade training classifiers belongs to The Intel Corperations. Additional licensing informations and documentations can be found on the OpenCV Official GitHub Repository.

OpenCV Official GitHub Repository: https://github.com/opencv/opencv

Wiring for the HC-SR04 was performed on a breadboard, with help from this tutorial:

https://pimylifeup.com/raspberry-pi-distance-sensor/
