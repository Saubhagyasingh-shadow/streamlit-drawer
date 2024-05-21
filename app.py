# from flask import Flask, render_template, Response
# import cv2
# import numpy as np
# import HandTrackingModule as htm
# import os

# app = Flask(__name__)

# # Initialize hand detector
# detector = htm.handDetector(detectionCon=0.45, maxHands=1)

# # Video capture setup
# cap = cv2.VideoCapture(1)
# cap.set(3, 1280)
# cap.set(4, 720)

# folderPath = "header"
# mylist = os.listdir(folderPath)
# overlayList = []
# for imgPath in mylist:
#     image = cv2.imread(f'{folderPath}/{imgPath}')
#     # print({imgPath})
#     overlayList.append(image)

# # print(len(overlayList))
# header = overlayList[0]
# # print(header.shape)

# drawColor = (0, 0, 255)
# brushThickness = 25
# eraserThickness = 150
# xp, yp = 0, 0
# imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# @app.route('/')
# def index():
#     return render_template('index.html')

# def gen_frames():
#     while True:
#         global header  # Access the global header variable
#         global drawColor,brushThickness,eraserThickness
#         success, img = cap.read()
        
#         if not success:
#             break
#         else:
#             img = cv2.flip(img, 1)
#             img = detector.findHands(img)
            
#             lmList, bbox = detector.findPosition(img, draw=False)
  
#             if len(lmList) != 0:
#                 if len(lmList) > 12:
#                     x1, y1 = lmList[8][1:]
#                     x2, y2 = lmList[12][1:]

#                     fingers = detector.fingersUp()

#                     if isinstance(fingers, list) and len(fingers) == 5:
#                         if fingers[1] and fingers[2]:
#                             xp, yp = 0, 0
#                             if y1 < 142:
#                                 if 70 < x1 < 230:
#                                     # header = overlayList[4]
#                                     header = overlayList[1]

#                                     drawColor = (0, 0, 255)
#                                 elif 240 < x1 < 430:
#                                     # header = overlayList[3]
#                                     header = overlayList[1]

#                                     drawColor = (0, 255, 0)
#                                 elif 440 < x1 < 620:
#                                     header = overlayList[1]
#                                     drawColor = (255, 0, 0)
#                                 elif 660 < x1 < 880:
#                                     header = overlayList[2]
#                                     drawColor = (0, 0, 0)
#                             cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

#                         if fingers[1] and not fingers[2]:
#                             cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
#                             if xp == 0 and yp == 0:
#                                 xp, yp = x1, y1
#                             cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
#                             cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
#                             xp, yp = x1, y1

#             imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
#             _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
#             imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
#             img = cv2.bitwise_and(img, imgInv)
#             img = cv2.bitwise_or(img, imgCanvas)
          
#             # print(img.shape)
#             img[0:142, 0:1280] = header
            
#             ret, buffer = cv2.imencode('.jpg', img)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video')
# def video():
#      return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)
import streamlit as st
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import os

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.45, maxHands=1)

# Video capture setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

folderPath = "header"
overlayList = [cv2.imread(f'{folderPath}/{imgPath}') for imgPath in os.listdir(folderPath)]
header = overlayList[0]

drawColor = (0, 0, 255)
brushThickness = 25
eraserThickness = 150
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

st.title("Live Hand Tracking and Drawing")

# Define Streamlit video frame generator function
def gen_frames():
    global header, drawColor, brushThickness, eraserThickness, xp, yp, imgCanvas
    while True:
        success, img = cap.read()
        if not success:
            st.error("Failed to capture video", icon="🚨")
            break
        else:
            img = cv2.flip(img, 1)
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img, draw=False)

            if lmList:
                if len(lmList) > 12:
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]

                    fingers = detector.fingersUp()

                    if fingers and len(fingers) == 5:
                        if fingers[1] and fingers[2]:
                            xp, yp = 0, 0
                            if y1 < 142:
                                if 70 < x1 < 230:
                                    header = overlayList[1]
                                    drawColor = (0, 0, 255)
                                elif 240 < x1 < 430:
                                    header = overlayList[1]
                                    drawColor = (0, 255, 0)
                                elif 440 < x1 < 620:
                                    header = overlayList[1]
                                    drawColor = (255, 0, 0)
                                elif 660 < x1 < 880:
                                    header = overlayList[2]
                                    drawColor = (0, 0, 0)
                            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

                        if fingers[1] and not fingers[2]:
                            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                            if xp == 0 and yp == 0:
                                xp, yp = x1, y1
                            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                            xp, yp = x1, y1

            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img, imgInv)
            img = cv2.bitwise_or(img, imgCanvas)
            img[0:142, 0:1280] = header
            
            # Return the video frame as a byte array
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            return frame

# Display the video frames in Streamlit
stframe = st.empty()
while True:
    frame = gen_frames()
    stframe.image(frame, channels='BGR')
