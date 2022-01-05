import cv2
import numpy as np
import sqlite3
import csv

def insertorUpdate(ID,Name,RollNo):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM Person WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE Person SET Name="+str(Name)+"WHERE ID="+str(Id)
        cmd="UPDATE Person SET RollNo="+str(Rollno)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO Person(ID,Name,ROllNo) Values("+str(Id)+","+str(Name)+","+str(RollNo)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()

Id=input('Enter the user id: ')
name=input('Enter the Name as a String: ')
Rollno=input('Enter the RollNo as a String: ')
insertorUpdate(Id,name,Rollno)

cap = cv2.VideoCapture(0)
function = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

samplenum = 0
while(True):
    ret,frame=cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = function.detectMultiScale(gray,1.32,5)

    for (x,y,w,h) in faces:
        cropped =gray[y:y+h,x:x+w]
        samplenum = samplenum+1;
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2,cv2.LINE_AA)
        cv2.imwrite("DataBase/User."+str(Id)+"."+str(samplenum)+".jpg",cropped)
       
    cv2.imshow('frame',frame)
    cv2.waitKey(100)
    if(samplenum>=50):
        break;
cap.release()
cv2.destroyAllWindows()
