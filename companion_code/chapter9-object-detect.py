import cv2
#import numpy

factor_down = 0.33
factor_up = 3

capture = cv2.VideoCapture(0)

eye_data = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')
smile_data = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_mcs_mouth.xml')

while True:

    return_val, frame = capture.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    small_gray_frame = cv2.resize(gray_frame, (0,0), fx=factor_down, fy=factor_down)

    eyes = eye_data.detectMultiScale(small_gray_frame, 1.3, 5)
    for (eye_x, eye_y, eye_width, eye_height) in eyes:
        cv2.rectangle(frame, (eye_x*factor_up, eye_y*factor_up),
                      (eye_x*factor_up + eye_width*factor_up, 
                      eye_y*factor_up+eye_height*factor_up), 
                      (255,0,0),2)

    smiles = smile_data.detectMultiScale(small_gray_frame, 1.3, 5)
    for (smile_x, smile_y, smile_width, smile_height) in smiles:
        cv2.rectangle(frame, (smile_x*factor_up, smile_y*factor_up),
                      (smile_x*factor_up + smile_width*factor_up, 
                      smile_y*factor_up+smile_height*factor_up), 
                      (0,255,0),2)

    cv2.imshow('Face', frame)
    
    key = cv2.waitKey(5)
    if key == 113:
        break
