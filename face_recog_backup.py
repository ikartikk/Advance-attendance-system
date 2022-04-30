import cv2 as cv
import numpy as np
import face_recognition
import os
import pandas as pd
import datetime 
import pyttsx3

def Speak(command):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    engine.say(command)
    engine.runAndWait()


mypath = 'computer_vision/test1/student_data'
timages= []
className = []
mylist = os.listdir(mypath)
for cl in mylist:
    curImg = cv.imread(f'{mypath}/{cl}')
    timages.append(curImg)
    className.append(os.path.splitext(cl)[0].upper())


def findEnodings(images):
    encodeList = []    
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encode_face)
    return encodeList
encoded_face_train = findEnodings(timages)

def updateCsv(path,name1,value):
    df=pd.read_csv(path)
    df=df.append({'Name':name1,'LastSeen':value}, ignore_index=True)    
    df=df.dropna(axis=1)
    df=df.drop_duplicates('Name',keep="last")
    df.to_csv(path,index=False)

cap = cv.VideoCapture(0)
flag=1
while True:
    success,img = cap.read()
   #imgS = cv.resize(img, (0,0), None,0.25, 0.25)
    imgS = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS,faces_in_frame)
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train,encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train,encode_face)
        matchIndex = np.argmin(faceDist)
        #print(matchIndex)
        if matches[matchIndex]:
            
            name=className[matchIndex].upper()
            #name = className[matchIndex].upper()
            y1,x2,y2,x1 = faceloc
           #y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv.rectangle(img,(x1,y1),(x2,y2),(0,255,255),2)
            cv.rectangle(img,(x1,y2+30),(x2,y2),(0,255,255),-1)
            cv.putText(img,name,(x1,y2+27),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)   
            
            
            df = pd.read_csv('computer_vision/test1/lastSeen.csv')
            df.set_index('Name', inplace=True)
            try:
                ss=df.loc[name]['LastSeen']
            except:
                ss = 'Today'   
            
            updateCsv('computer_vision/test1/lastSeen.csv',name,datetime.datetime.now().strftime("%c"))
            break
            

        else:
            cap.release()
            cv.destroyAllWindows()            
            i=0
            for cl1 in mylist:
                cl1=os.path.splitext(cl1)[0]
                mylist[i]=cl1.upper()
                i+=1
            Speak("Enter your name please")
            Name = input("Enter Your Name: ")
            Name=Name.upper()
            Speak("Welcome"+ Name.lower())
            
            
            if Name not in mylist:

                count=0
                #mylist.append(Name)
                Speak("Press 'S' to start collecting face data and 'Q' to save your picture.")
                print("Press 'S' to start collecting face data and 'Q' to save your picture.")
                userinput = input()

                if userinput !='s':
                    print("Enter valid Input ")
                    exit()

                cap = cv.VideoCapture(0)

                while True:

                    status, frame = cap.read()
                    cv.imshow("Video window",frame)
                    gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    
                    cv.imwrite('D:/python/computer_vision/test1/student_data/'+Name+'.jpg',gray)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        Speak("Thankyou your image has been saved.")
                        cap.release()
                        cv.destroyAllWindows()
                        break
                    
            
    cv.imshow("webcam",img)        
    try:
        if flag == 1:
            Speak('Hello '+ name.lower())
            Speak("Last seen on "+ss)
            flag=0
    except:
        continue
    
    if cv.waitKey(1) & 0xFF == ord('q'):       
        break
