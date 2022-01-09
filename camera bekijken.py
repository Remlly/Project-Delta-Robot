import cv2 # importeer de opencv module in python
import time # importeer de time module, nodig voor sleep
import numpy as np # beelden zijn numpy arrays, numpy gebruiken we ook

cv2.WINDOW_AUTOSIZE
cv2.namedWindow("beeld1",cv2.WINDOW_AUTOSIZE)
cv2.moveWindow("beeld1",0,0) # Plaats beeld1 linksboven op (0,0)

webcam = cv2.VideoCapture(0) # Open de default-camera
webcam.set(cv2.CAP_PROP_FRAME_WIDTH,640) # 1920 bij breedbeeldcamera’s
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,480) # 1080 bij breedbeeldcamera’s

#writer = cv2.VideoWriter(filename="C:/users/freek/Videos/opencvtutorial1.avi", fourcc=cv2.VideoWriter_fourcc(*'XVID'), fps=15, frameSize=(640,480), isColor=1)

while True:
 retval, img = webcam.read() # inlezen van het beeld in de variabele img
 if(retval == True): # Als retval (return value) True dan…
    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img_gray2 = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    #img_gray2[:,:,1:3] = np.zeros((480,640,2), dtype=np.uint8)
    cv2.imshow("beeld1",img) # …beeld is ok, dus geef het weer
    #writer.write(img_gray2)
    if(cv2.waitKey(10) == 27): # Als Escapetoets (code 27) ingedrukt dan…
        break # …spring uit while-lus

#writer.release()
webcam.release() # …ontkoppel camera…
cv2.destroyWindow("beeld1") # …verwijder alleen window beeld1…