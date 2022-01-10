import socket 
import StructFuncs as struct
import numpy as np
import cv2
import os


pcHostName = socket.gethostname() 
hostIp = socket.gethostbyname(pcHostName) 
hostPort = 2000 
serverAddress = (hostIp, hostPort)      # create (tuple) 

cv2.WINDOW_AUTOSIZE
cv2.namedWindow("Capture",cv2.WINDOW_AUTOSIZE)
cv2.moveWindow("Capture",0,0) # Plaats beeld1 linksboven op (0,0)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 160)
cv2.createTrackbar("Threshold1", "Parameters", 115, 255, empty) # naam, window, start waarde, eindwaarde, functie die aangeroepen wordt
cv2.createTrackbar("Threshold2", "Parameters", 240, 255, empty)
cv2.createTrackbar("Area", "Parameters", 2000, 10000, empty)
cv2.moveWindow("Parameters", 0, 650)

cv2.namedWindow("Image Parameters")
cv2.resizeWindow("Image Parameters", 640, 160)
cv2.createTrackbar("X-Coordinaat", "Image Parameters", 255, 1920, empty) # naam, window, start waarde, eindwaarde, functie die aangeroepen wordt
cv2.createTrackbar("Y-Coordinaat", "Image Parameters", 136, 1080, empty)
cv2.createTrackbar("Grootte", "Image Parameters", 87, 100, empty)
cv2.moveWindow("Image Parameters", 650, 650)

webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Open de default-camera
webcam.set(cv2.CAP_PROP_FRAME_WIDTH,1280) # 1920 bij breedbeeldcamera’s
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT,720) # 1080 bij breedbeeldcamera’s

boundaries =  np.array([[65, 105, 0],  	    # kleuren boundaries in HSV
                        [85, 185, 0],        #groen
                        [0, 105, 180], 
                        [10, 185, 240],        #oranje
                        [15, 160, 120], 
                        [40, 220, 160],        #rood
                        [95, 95, 10], 
                        [115, 230, 70],        #blauw
                        [15, 20, 10], 
                        [90, 100, 255],        #wit
                        [22, 140, 195], 
                        [35, 200, 255],        #geel
                        [115, 80, 70], 
                        [140,200, 130],        #paars
])

coordinates = np.array([[0,0],      #groen = 0
                        [1,1],      #oranje = 1
                        [2,2],      #rood = 2
                        [3,3],      #blauw = 3
                        [4,4],      #wit = 4
                        [5,5],      #geel = 5
                        [6,6]])     #paars = 6


def getContours(img, imgContour, imgDefault):
    
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            imgStandard = imgDefault.copy()
            hsv = cv2.cvtColor(imgStandard, cv2.COLOR_BGR2HSV)
            hsv[:,:,1] += 10     #20 toevoegen om saturation omhoog te krijgen
            hsv[:,:,2] += 10     #50 toevoegen om helderheid omhoog te krijgen
            imgStandard = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            mask = np.zeros(imgStandard.shape, np.uint8)
            mask_black = np.zeros(imgStandard.shape[:2], np.uint8)
            channel_count = imgStandard.shape[2]
            ignore_mask_color = (255,)*channel_count

            if(len(approx) == 4):
                midden = [(int(x+(0.5*w))), (int(y+(0.5*h)))]
                roi_corners = np.array([[(approx[0,0,0],approx[0,0,1]), (approx[1,0,0],approx[1,0,1]), (approx[2,0,0],approx[2,0,1]), (approx[3,0,0],approx[3,0,1])]], dtype=np.int32)
                roi_corners_black = roi_corners.reshape((-1,1,2))
                cv2.fillPoly(mask_black, [roi_corners_black], 255)

            elif(len(approx) == 3):
                xt = round((approx[0,0,0] + approx[1,0,0] + approx[2,0,0]) / 3, 2)
                yt = round((approx[0,0,1] + approx[1,0,1] + approx[2,0,1]) / 3, 2)
                midden = [(int(xt)), (int(yt))]
                roi_corners = np.array([[(approx[0,0,0],approx[0,0,1]), (approx[1,0,0],approx[1,0,1]), (approx[2,0,0],approx[2,0,1])]], dtype=np.int32)
                roi_corners_black = roi_corners.reshape((-1,1,2))
                cv2.fillPoly(mask_black, [roi_corners_black], 255)

            else:
                break
            #cv2.imshow("Center", imgStandard)
            cv2.fillConvexPoly(mask, roi_corners, ignore_mask_color)
            imgStandard = cv2.bitwise_and(imgStandard, mask)
            imgStandard = (cv2.medianBlur(imgStandard, 9))
            hsv =cv2.cvtColor(imgStandard, cv2.COLOR_BGR2HSV)
            Average_color = np.array(cv2.mean(hsv, mask_black)).astype(np.uint8)
            h, s, v = cv2.split(hsv)
             
            cv2.circle(imgContour, midden, 3, (128,0,128), 10)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Middle: " + str(midden), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Color: " + str(Average_color[:3]), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)

            #Groen
            if((Average_color[0] >= boundaries[0][0]) and (Average_color[1] >= boundaries[0][1]) and (Average_color[0] <= boundaries[1][0]) and (Average_color[1] <= boundaries[1][1]) ):
                coordinates[0] = midden
            #Oranje
            if((Average_color[0] >= boundaries[2][0]) and (Average_color[1] >= boundaries[2][1]) and (Average_color[0] <= boundaries[3][0]) and (Average_color[1] <= boundaries[3][1]) ):
                coordinates[1] = midden
            #Rood

            #if((Average_color[0] >= boundaries[4][0]) and (Average_color[1] >= boundaries[4][1]) and (Average_color[0] <= boundaries[5][0]) and (Average_color[1] <= boundaries[5][1]) ):
             #   coordinates[2] = midden
            #Blauw
            if((Average_color[0] >= boundaries[6][0]) and (Average_color[1] >= boundaries[6][1]) and (Average_color[0] <= boundaries[7][0]) and (Average_color[1] <= boundaries[7][1]) ):
                coordinates[3] = midden
            #Wit
            if((Average_color[0] >= boundaries[8][0]) and (Average_color[1] >= boundaries[8][1]) and (Average_color[0] <= boundaries[9][0]) and (Average_color[1] <= boundaries[9][1]) ):
                coordinates[4] = midden
            #Geel
            if((Average_color[0] >= boundaries[10][0]) and (Average_color[1] >= boundaries[10][1]) and (Average_color[0] <= boundaries[11][0]) and (Average_color[1] <= boundaries[11][1]) ):
                coordinates[5] = midden
            #Paars
            if((Average_color[0] >= boundaries[12][0]) and (Average_color[1] >= boundaries[12][1]) and (Average_color[0] <= boundaries[13][0]) and (Average_color[1] <= boundaries[13][1]) ):
                coordinates[6] = midden
            
            else: 
                coordinates[2] = midden

def display_coordinates(imgContour):
    cv2.putText(imgContour, "Groen:  " + str(coordinates[0]), (10,50), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2) 
    cv2.putText(imgContour, "Oranje: " + str(coordinates[1]), (10,75), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2) 
    cv2.putText(imgContour, "Rood:   " + str(coordinates[2]), (10,100), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2)  
    cv2.putText(imgContour, "Blauw:  " + str(coordinates[3]), (10,125), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2)  
    cv2.putText(imgContour, "Wit:    " + str(coordinates[4]), (10,150), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2)  
    cv2.putText(imgContour, "Geel:   " + str(coordinates[5]), (10,175), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2)  
    cv2.putText(imgContour, "Paars:  " + str(coordinates[6]), (10,200), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 140, 255), 2)      
           


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)






tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

tcpSocket.bind(serverAddress)           # Bind to the port 
tcpSocket.listen(5)                     # Wait for (max 5) connecting clients 
tcpSocket.settimeout(2)









connected = False

while True:
     clearConsole()
     
    
     while not connected:
         try:
             print("[*] Started listening on", hostIp, ":", hostPort) 
             # Establish connection with client. 
             client, clientAddress = tcpSocket.accept() 
             
             # clientAddress[0] contains client-ip 
             # clientAddress[1] contains client-port 
         except socket.timeout:
             print("[*] timed out trying again...")
         
         else:
             print("[*] Got connection from ", 
                   clientAddress[0], ":", clientAddress[1])
             
             client.settimeout(0.1)
             connected = True 
             break
     
     try:
         
         data = client.recv(1024)   
         unpacked_data = struct.unpack_array(data)  
         unpacked_data = list(unpacked_data)
         print(f"[*] Data is {unpacked_data}")
     except socket.timeout:
         print("[*] no data recieved ")
         
         continue
     except ConnectionResetError:
         print("[*] Connection lost")
         connected = False
         continue 
     
     else:
         print("[*] sending response")
         
         if(unpacked_data[0] == 10):
             
             coordinates = coordinates.astype(float)                #PLC and struct expects a float array
             coordinates = coordinates.flatten()                    #PLC does not handle 2D arrays
             packed_coordinates = struct.pack_array(coordinates)    #Packing        
             client.send(packed_coordinates)                        #Sending
             unpacked_data[0] = 0                                   #Reset message
             
         else:
             print("[*] unkown message, discarding...")
             unpacked_data[0] = 0
    
     finally:


         #vision   
         retval, img = webcam.read() # inlezen van het beeld in de variabele img
         if(retval == True): # Als retval (return value) True dan…
            img = img [(cv2.getTrackbarPos("Y-Coordinaat", "Image Parameters")):(int(7.2*(cv2.getTrackbarPos("Grootte", "Image Parameters")))), (cv2.getTrackbarPos("X-Coordinaat", "Image Parameters")):(int(12.8*(cv2.getTrackbarPos("Grootte", "Image Parameters"))))]
            imgContour = img.copy()
        
            imgBlur = cv2.GaussianBlur(img, (7,7), 1)
            imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        
            threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
            threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
            imgCanny = cv2.Canny(imgBlur, threshold1, threshold2)
            kernel = np.ones((5,5))
            imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
        
            getContours(imgDil, imgContour, img)
        
            display_coordinates(imgContour)
        
            cv2.imshow("Capture", imgContour) 
            if(cv2.waitKey(10) == 27): # Als Escapetoets (code 27) ingedrukt dan…
                break # …spring uit while-lus
                
            

webcam.release() # …ontkoppel camera…
cv2.destroyWindow("Capture") # …verwijder alleen window capture
