import cv2
import numpy as np

def find_c_score(d,f,l,u):#for digital reading
    if l<f<=(l+0.025):
        return (d+0.9)
    elif (l+0.025)<f<=(l+0.05):
        return (d+0.8)
    elif (l+0.05)<f<=(l+0.075):
        return (d+0.7)
    elif (l+0.075)<f<=(l+0.1):
        return (d+0.6)
    elif (l+0.1)<f<=(l+0.125):
        return (d+0.5)
    elif (l+0.125)<f<=(l+0.15):
        return (d+0.4)
    elif (l+0.15)<f<=(l+0.175):
        return (d+0.3)
    elif (l+0.175)<f<=(l+0.2):
        return (d+0.2)
    elif (l+0.2)<f<=(l+0.225):
        return (d+0.1)
    elif (l+0.225)<f<=u:
        return (d+0)

   

def find_score(distance):#for manual reading
    if 2 < distance <=2.25:
        k=find_c_score(1,distance,2,2.25)
        return k
    elif 1.75 < distance <=2:
        k=find_c_score(2,distance,1.75,2)
        return k
    elif 1.5 < distance <=1.75:
        k=find_c_score(3,distance,1.5,1.75)
        return k
    elif 1.25 < distance <=1.5:
        k=find_c_score(4,distance,1.25,1.5)
        return k
    elif 1 < distance <=1.25:
        k=find_c_score(5,distance,1,1.25)
        return k
    elif 0.75 < distance <=1:
        k=find_c_score(6,distance,0.75,1)
        return k
    elif 0.5 < distance <=0.75:
        k=find_c_score(7,distance,0.5,0.75)
        return k
    elif 0.25 < distance <=0.5:
        k=find_c_score(8,distance,0.25,0.5)
        return k
    elif 0 < distance <=0.25:
        k=find_c_score(9,distance,0,0.25)
        return k
    elif distance==0:
        return 10
    else:
        return 0


def cvt_into_square(a,b,c,d,image):#convert the image into square
    points_trapezium = np.float32([a, d, b, c])
    width = 500  
    height = 500  
    points_square = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(points_trapezium, points_square)
    result = cv2.warpPerspective(image, matrix, (width, height))
    return result

webcam=False
path='sample_sheet_1.jpg'
cap=cv2.VideoCapture(1)
stopper=0
while True:
    if webcam:success,image=cap.read()
    else: image=cv2.imread(path)
    image=cv2.flip(image,1)
    digital=cv2.imread("score_img.jpg")
    digital=cv2.resize(digital,(700,700))
    #score_dis=cv2.imread("score_display.png")
    #score_dis=cv2.resize(score_dis,(500,500))
    image=cv2.resize(image,(500,500))
    #408, 154, 441, 424, 173, 412, 193, 155         467, 106, 465, 334, 66, 334, 68, 104
    ary = np.array([466, 108, 465, 334, 68, 333, 68, 104])
    arr1 = ary.reshape(4, 2)
    a=arr1[3] #all the cordinate from the first image black sheet
    b=arr1[2]
    c=arr1[1]
    d=arr1[0]
    cv2.line(image,(a),(b),(255,0,0),1)
    cv2.line(image,(b),(c),(255,0,0),1)
    cv2.line(image,(c),(d),(255,0,0),1)
    cv2.line(image,(d),(a),(255,0,0),1)

    ans=cvt_into_square(a,b,c,d,image)#call the square function
    #cv2.imshow("k",ans)
    ans=cv2.resize(ans,(100,100))
    gray=cv2.cvtColor(ans,cv2.COLOR_BGR2GRAY)
    gray=cv2.bitwise_not(gray)
    threshold_level=80
    coords=np.array(np.where(gray<threshold_level))
    #print(coords)
    if len(coords)!=0: #if shoot is exist
        mask=gray<threshold_level
        ans[mask]=(0,0,255)
        #digital[mask]=(0,0,255)
        center=50
        cx=0
        cy=0
        min_dist=100
        for i in range(len(coords[0])): #find the minimum distance from center to all cordinates
            m=(((coords[0][i]-center)**2)+((coords[1][i]-center)**2))**0.5
            if m<min_dist:
                min_dist=m
                cx=coords[0][i]
                cy=coords[1][i]

        answer=min_dist
        h=6  #original=15
        answer=answer*h/100
        r_ans = round((answer), 2)
        jay=find_score(r_ans)
        s=f"Score={jay} Distance={r_ans}CM"
        t=f"{jay}"
        if jay>0: #if score is not equal to zero
            cv2.putText(digital,s,(20,30),cv2.QT_FONT_NORMAL,1,(0,0,0),2)
            cv2.line(ans,(cy,cx),(cy,cx),(255,0,0),4)
            cv2.line(ans,(center,center),(center,center),(255,0,0),3)
            cv2.line(ans,(cy,cx),(center,center),(0,255,0),1)
            cv2.line(digital,(cy*7,cx*7),(cy*7,cx*7),(0,0,255),15)
            #cv2.putText(image,t,(0,300),cv2.QT_FONT_NORMAL,10,(0,0,255),5)
            #cv2.putText(digital,"+",(cy*5,cx*5),cv2.QT_FONT_NORMAL,0.4,(0,0,255),1)


    #final=np.hstack((image,ans))
    #digital=cv2.resize(digital,(500,500))
    cv2.imshow("A",image)
    cv2.imshow("B",ans)
   # cv2.imshow("C",score_dis)
    cv2.imshow("C",digital)
    if jay==0:
       stopper=0
    if jay>0 and stopper==0: #if score not equal to zero
        print(s)
        stopper+=1
    if cv2.waitKey(100) & 0xFF==ord('q'):
        break
