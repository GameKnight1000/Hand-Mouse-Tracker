# Importing the Modules
import cv2
import mediapipe
import pyautogui

clickDown = False

#Taking webcam footage and storing it
capture = cv2.VideoCapture(0)

mediapipeHands = mediapipe.solutions.hands
hands = mediapipeHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mediapipeDraw = mediapipe.solutions.drawing_utils

while True:
    success, img = capture.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if clickDown == True:
        pyautogui.mouseDown(button='left')
        print ('Left Click')
   
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

            mediapipeDraw.draw_landmarks(img, handLms, mediapipeHands.HAND_CONNECTIONS)
            rightHand = bool(int(str(results.multi_handedness).split()[3]))

            x_coordinate_index = float(f'{handLms.landmark[mediapipeHands.HandLandmark(8).value]}'.split()[1])
            y_coordinate_index = float(f'{handLms.landmark[mediapipeHands.HandLandmark(8).value]}'.split()[3])
            
            y_coordinate_middle12 = float(f'{handLms.landmark[mediapipeHands.HandLandmark(12).value]}'.split()[3])
            y_coordinate_middle10 = float(f'{handLms.landmark[mediapipeHands.HandLandmark(10).value]}'.split()[3])

            pyautogui.moveTo(1920 * x_coordinate_index, 1080 * y_coordinate_index)

            x_coordinate_thumb = float(f'{handLms.landmark[mediapipeHands.HandLandmark(4).value]}'.split()[1])

            if abs(y_coordinate_middle12 - y_coordinate_middle10) < 0.05:
                pyautogui.mouseDown(button='right')
                print ('Right Click')

            else:
                pyautogui.mouseUp()

            if (x_coordinate_thumb - x_coordinate_index) < 0.05:
                pyautogui.mouseDown(button='left')
                clickDown = True
                print ('Left Click')

            else:
                pyautogui.mouseUp()
                clickDown = False
            

    cv2.imshow("Image", img)

    k = cv2.waitKey(30) & 0xff
   
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
