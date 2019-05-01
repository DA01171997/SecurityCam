from datetime import datetime

from rangefinder import RangeFinder
from Mail import Mail
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import numpy as np
import time
import cv2


class SecurityCamera:
    """
    this class handles security camera functionality, along with email alerts for when it is triggered

    Configurable attributes:
        to_email -> email address to send notifications to
        mailer -> sends email notifications, configured by:
            from_email -> email address to use for sending notifications
            email_password -> password to use for sending notifications from from_email
        trigger_dist -> distance in CM which is the threshold for triggering the camera
        scan_interval -> time to wait (in seconds) between checking sensors
        trigger_interval -> time to wait (in seconds) between triggering detection again

    other attributes:
        range_finder -> uses a sonic distance sensor to measure how far something is from the camera
        face_cascade -> computer vision classifier for faces
        body_cascade -> computer vision classifier for bodies
        frame_data -> holds information on any given frame the camera may be analyzing
    """
    def __init__(self, to_email, from_email, email_password, trigger_dist=100, scan_interval=5, trigger_interval=15):
        self.mailer = Mail(from_email, email_password)  # mailer object
        self.to_email = to_email    # destination email
        self.trigger_dist = trigger_dist    # distance threshold
        self.scan_interval = scan_interval  # scan interval
        self.last_trigger = datetime.now()  # last trigger timestamp
        self.trigger_interval = trigger_dist    # trigger cooldown
        self.range_finder = RangeFinder()   # range finder object
        # computer vision models
        self.face_cascade = cv2.CascadeClassifier('./opencv_models/haarcascade_frontalface_default.xml')
        self.body_cascade = cv2.CascadeClassifier('./opencv_models/haarcascade_fullbody.xml')
        # frame data
        self.frame_data = {
            'img': None,
            'img-gray': None,
            'faces': (),
            'bodies': (),
        }

    def is_trigger_ready(self):
        """
        Returns True/False indicating if enough time has elapsed 
        since the last trigger to be ready for activation again
        """
        return (self.last_trigger - datetime.now()).total_seconds() > self.trigger_interval

    def send_alert(self, capture_file, capture_timestamp, distance):
        """
        Sends an email alert based on the provided information

        parameters:
            capture_file -> the name of a capture file to attach to the email
            capture_timestamp -> a timestamp for the capture
            distance -> the distance that was measured at the time of capture
        """
        self.mailer.addReceiver(self.to_email)  # add destination
        self.mailer.addSubjectHeader('Security Camera Alert')   # set the subject line
        self.mailer.addBody(    # add body content (both plain-text and HTML template render values)
            'ALERT: security camera detected activity at {0} from a distance of {1}'.format(capture_timestamp, distance), 
            html_context={
                'time_stamp': capture_timestamp,
                'distance': distance
            }
        )
        self.mailer.addAttachment(fileName=capture_file)    # add the capture file
        self.mailer.constructNSendMail()    # send the notification

    def monitor(self):
        """
        Begins monitoring sensors for activity, sends emails when necessary
        """
        capture_file = None # name of capture file
        capture_timestamp = None    # timestamp for file
        distance = None # distance measured

        try:
            while True:
                distance = self.range_finder.get_distance() # check the distance sensor
                if distance < self.trigger_dist and self.is_trigger_ready():    # no cooldown, and target is close
                    with PiCamera() as camera:  # open the camera
                        raw_capture = PiRGBArray(camera, size=(640, 480))   # configure the camera
                        camera.resolution = (640, 480)
                        camera.framerate = 60
                        time.sleep(0.1)  # allow camera to warm up for split second
                        # begin capturing frames from the camera
                        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
                            self.frame_data['img'] = frame.array    # get the image data
                            self.frame_data['img-gray'] = cv2.cvtColor(self.frame_data['img'], cv2.COLOR_BGR2GRAY)  # convert image data to gray
                            # run computer vision
                            self.frame_data['faces'] = self.face_cascade.detectMultiScale(self.frame_data['img-gray'], 1.3, 5)
                            self.frame_data['bodies'] = self.body_cascade.detectMultiScale(self.frame_data['img-gray'], 1.3, 5)

                            # outline all detections in the image
                            for (x_top, y_top, width, height) in self.frame_data['bodies']:
                                cv2.rectangle(self.frame_data['img'], (x_top, y_top), (x_top + width, y_top + height), (255, 0, 0), 2)
                            for (x_top, y_top, width, height) in self.frame_data['faces']: 
                                cv2.rectangle(self.frame_data['img'], (x_top, y_top), (x_top + width, y_top + height), (255, 255, 0), 2)

                            # if detections were found, send th
                            if len(self.frame_data['faces']) > 0 or len(self.frame_data['bodies']) > 0:
                                capture_timestamp = datetime.now()  # timestamp for capture
                                capture_file = 'detection_' + str(capture_timestamp).replace(' ', '_') + '.png' # generate filename from timestamp
                                cv2.imwrite(    # write the image data to a file
                                    capture_file,
                                    self.frame_data['img']
                                )
                                self.send_alert(capture_file, capture_timestamp, distance)  # send the email notice
                                break
                            elif self.is_trigger_ready():  # if the trigger is ready again, then stop looking for the time being
                                break
                            raw_capture.truncate(0) # reduce the capture data
                time.sleep(self.scan_interval)  # wait for the scan interval
        except KeyboardInterrupt:
            print('Stopping monitoring process.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Begins monitoring for activity available distance sensor and camera',
    )
    parser.add_argument(
        'email', 
        help='email address to send notifications to',
    )
    parser.add_argument(
        'sender', 
        help='email address to use to send notifications from an SMTP server',
    )
    parser.add_argument(
        'password', 
        help='password to use to send notifications from an SMTP server',
    )
    parser.add_argument(
        '--threshold',
        help='distance threshold in CM to activate the camera, default is 100',
        nargs='?',
        default=None,
    )
    parser.add_argument(
        '--scan',
        help='time in seconds to wait between scans, default is 5',
        nargs='?',
        default=None,
    )
    parser.add_argument(
        '--cooldown',
        help='time in seconds to wait before activating the camera again, default is 15',
        nargs='?',
        default=None,
    )
    args = parser.parse_args()
    security_cam = SecurityCamera(
        to_email=args.email,
        from_email=args.sender,
        email_password=args.password,
        trigger_dist=args.threshold or 100,
        scan_interval=args.scan or 5,
        trigger_interval=args.cooldown or 15,
    )
    security_cam.monitor()
