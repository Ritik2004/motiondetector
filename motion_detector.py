import cv2, time, pandas
from datetime import datetime


first_frame = None
status_list = [None, None]
#in this we are storing when object was first scene and when it disappeared

times = []
df = pandas.DataFrame(columns=["start","end"])
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    #itterate through current frame

    check, frame = video.read()
    status = 0
  #convert frame to gray first
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)
   #blur the frame and convert it in grey frame
    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame,gray)
    #here we calculate the difference bw frame
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    #here we find threshold frame ie if delta frame is greater than 30 
    #it is threshold frame and we show it with white color(255)
    #it is black and white image
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   #contours detect change in the image colour and store as shape
   #it will display the contour whose area is greater than 1000 

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
#if here cintours are greater than 1000 than status change to 1
        status = 1
    
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)    

    status_list.append(status)

#here we see the last and second last value whether they are changing from
#1 to 0 or viceversa if yes then we save the time for the changing state
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("gray frame", gray)
    cv2.imshow("delta frame",delta_frame)
    cv2.imshow("thresh frame", thresh_frame)
    cv2.imshow("color_frame",frame)

    key = cv2.waitKey(1)
   # print(gray)
   # print(deltaq_frame)
    if(key == ord('q')):
        if status == 1:
            times.append(datetime.now())

        break
    
print(status_list)
print(times)  

for i in range(0,len(times),2):
    df = df.append({"start":times[i],"end" : times[i+1]}, ignore_index = True)
df.to_csv("Times.csv")
video.release()
#we need to store the value of first frame in numpy
#array and then we find difference bw 1 frame and current frame

cv2.destroyAllWindows