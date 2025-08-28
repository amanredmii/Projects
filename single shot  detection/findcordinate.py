import cv2
import numpy as np
arr=[[]]
def distance1(a,b):
       arr.insert(0,b)
       arr.insert(0,a)
       if len(arr)>3:
         new_img=cv2.line(img,(arr[0],arr[1]),(arr[2],arr[3]),(0,255,0),1,4)
         cv2.imshow("video",new_img)
         print(arr)
         print((((arr[2]-arr[0])**2)+((arr[3]-arr[1])**2))**0.5)

def click_l(event,x,y,f,s):
    if event==cv2.EVENT_LBUTTONDOWN:
        s=f"{x},{y}"
        cv2.putText(img,s,(x,y),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0))
        cv2.imshow("video",img)
        distance1(x,y)
    elif event==cv2.EVENT_RBUTTONDOWN:
        b=img[y,x,0]
        g=img[y,x,1]
        r=img[y,x,2]
        s=f"{b},{g},{r}"
        cv2.putText(img,s,(x,y),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0))
        cv2.imshow("video",img)

def find_color():
    pass

webcam=False
path='sample_sheet_1.jpg'
cap=cv2.VideoCapture(0)

while True:
    if webcam:success,img=cap.read()
    else: img=cv2.imread(path)
    img=cv2.flip(img,1)
    img=cv2.resize(img,(500,500))
    cv2.imshow("video",img)
    #print(img)
    cv2.setMouseCallback("video",click_l)
    if cv2.waitKey(50) & 0xFF==ord('q'):
        break



 