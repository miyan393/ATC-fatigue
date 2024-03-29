# -*- coding: UTF-8 -*-
from scipy.spatial import distance as dist
from imutils.video import VideoStream

from imutils.video import FileVideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import pyglet
import argparse
import imutils
import time
import dlib
import cv2

def sound_alarm(path):
    music = pyglet.resource.media('alarm.wav')
    music.play()
    pyglet.app.run()

def eye_aspect_ratio(eye):
    # compute the vertical eye euclidean distances
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance of horizon
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear
def mouth_aspect_ratio(mouth):
    # compute the vertical mouth euclidean distances
    P = dist.euclidean(mouth[12], mouth[18])
    Q = dist.euclidean(mouth[14], mouth[16])
    # compute the euclidean distance of horizon
    R = dist.euclidean(mouth[11], mouth[15])
    # compute the mouth aspect ratio
    mouth = (P + Q) / (2.0 * R)
    return mouth

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")


ap.add_argument("-a", "--alarm", type=str, default="",
                help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
ap.add_argument("-v", "--video", type=str, default="",
	            help="path to input video file")
args = vars(ap.parse_args())
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.26
EYE_AR_CONSEC_FRAMES = 48
MOUTH_AR_THRESH = 0.75
MOUTH_AR_CONSECUTIVE_FRAMES = 48

# it is the frame counter used to indicate if the alarm is going off
COUNTER = 0
ALARM_ON = False
MOUTH_COUNTER = 0

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# starting the video stream thread
print("[INFO] starting video stream thread...")
#vs = VideoStream(src=args["webcam"]).start()

vs = FileVideoStream(args["video"]).start()
fileStream = True

time.sleep(1.0)

while True:
    # resizing the frame and converting into Grayscale
    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect faces in the grayscale frame
    facee = detector(gray, 0)
    
    # loop over the face detections
    for rect in facee:
        # determine facial landmarks and then converting to NumPyarray
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        # and mouth
        
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        mouth = shape[mStart:mEnd]

        leftmouth1= mouth[0][0]
        leftmouth2 = mouth[0][1]
        rightmouth1 = mouth[6][0]
        rightmouth2 = mouth[6][1]
        lefteye1 = leftEye[0][0]
        lefteye2 = leftEye[0][1]
        left_righteye1 = leftEye[3][0]
        left_righteye2 = leftEye[3][1]
        righteye1 = rightEye[0][0]
        righteye2 = rightEye[0][1]
        righteye3 = rightEye[3][0]
        righteye4 = rightEye[3][1]
       # eye_len = (righteye1 - left_righteye2)//2
        eye_len = (righteye3 - righteye1) //2 + (righteye3 - righteye1) //5
        buchong = (righteye3 - righteye1) //5
        ew = (rightmouth1 - leftmouth1)//2

        
        # average the eye aspect ratio together for both eyes and mouth
        ear = (leftEAR + rightEAR) / 2
        mar = mouth_aspect_ratio(mouth)

        
        # compute the convex hull for the left and right eye and mouth, then
        # visualize each of the eyes and mouth
        mouthHull = cv2.convexHull(mouth)
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        #---------------眼嘴标记多点图，不是方框
        # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        # cv2.drawContours(frame, [mouthHull], -1, (255, 0, 0), 1)
        #------------------------------------------------------------------------------
        cv2.rectangle(frame, (leftmouth1 , leftmouth2 - ew),
                       (rightmouth1, rightmouth2 + ew), (255, 0, 0), 2)
        cv2.rectangle(frame, (lefteye1 - buchong, lefteye2 - eye_len),
                      (left_righteye1 + buchong, left_righteye2 + eye_len), (0, 255, 0), 2)
        cv2.rectangle(frame, (righteye1 - buchong, righteye2 - eye_len),
                      (righteye3 + buchong, righteye4 + eye_len), (0, 255, 0), 2)
        #---------------------------------------------------------------

        # cv2.rectangle(frame, (mouthHull[0][0]),
        #               (mouthHull[8][0]),
        #               (0, 155, 255),
        #               2)
        # face = image[bounding_box[1]:bounding_box[1] + bounding_box[3],
        #        bounding_box[0]:bounding_box[0] + bounding_box[2]]
        # ew = (keypoints['right_eye'][0] - keypoints['left_eye'][0]) // 3
        # cv2.rectangle(image, (keypoints['left_eye'][0] - ew, keypoints['left_eye'][1] - ew),
        #               (keypoints['left_eye'][0] + ew, keypoints['left_eye'][1] + ew), (0, 255, 0), 2)
        # cv2.rectangle(image, (keypoints['right_eye'][0] - ew, keypoints['right_eye'][1] - ew),
        #               (keypoints['right_eye'][0] + ew, keypoints['right_eye'][1] + ew), (0, 255, 0), 2)

        if mar < MOUTH_AR_THRESH or ear < EYE_AR_THRESH:
            COUNTER += 1
        
        # if the eyes or mouth were closed for a sufficient number of frames
        # then sound the alarm
            if COUNTER >= MOUTH_AR_CONSECUTIVE_FRAMES or COUNTER >= EYE_AR_CONSEC_FRAMES:
                # if the alarm is not on, turn it on
                if not ALARM_ON:
                    ALARM_ON = True
                    
                
                    if args["alarm"] != "":
                        t = Thread(target=sound_alarm,
                                   args=(args["alarm"],))
                        t.deamon = True
                        t.start()
            
                cv2.putText(frame, "Alert!", (10, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1.0 , (0, 0, 255), 2)
                cv2.putText(frame, "you maybe  feeling sleepy", (10, 240),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        

    # otherwise, the eye aspect ratio and mouth aspect ratio is not below the blink threshold, so reset the counter and alarm
        else:
            COUNTER = 0
            ALARM_ON = False
        
        #putting the eye and mouth ratio on the frame only if you need
        #cv2.putText(frame, "EYES: {:.2f}".format(ear), (400, 30),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        #cv2.putText(frame, "MOUTH: {:.2f}".format(mar), (10, 60),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

# if the `s` key was pressed, then stop or breaking from the loop
#         if key == ord("s"):
#             break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# at last clearing the window
cv2.destroyAllWindows()
vs.stop()
#python main.py -p 68_face_landmarks.dat -v 3.mp4