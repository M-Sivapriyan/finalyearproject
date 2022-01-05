import cv2
import numpy as np
import time
import datetime
import sqlite3

cap = cv2.VideoCapture(0)
function = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("trainingData.yml")
path="Dataset"
prof = 0
def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT *FROM Person WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while(True):

    ret,frame=cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = function.detectMultiScale(gray,1.3,5)
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%y")
    time = now.strftime("%H:%M:%S")
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf = rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!=None):
            cv2.putText(frame,profile[1], (x, y+h+60), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3, cv2.LINE_AA)
            cv2.putText(frame,profile[2], (x, y+h+90), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3, cv2.LINE_AA)
            if(profile[1]!=prof or prof==0):
                conn=sqlite3.connect("FaceBase.db")
                conn.execute("INSERT INTO Attendance Values(?,?,?,?)",(profile[1],profile[2],date,time))
                conn.commit()
                conn.close()
                print("sucessfully print")
                prof=profile[1]
        else:
            id="Unknow"
            profile=getProfile(id)
            cv2.putText(frame,profile, (x, y+h+60), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3, cv2.LINE_AA) 
    cv2.imshow('frame',frame)
    if(cv2.waitKey(1)==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
        


