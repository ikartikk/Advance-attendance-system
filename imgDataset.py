import cv2 as cv
import os

mypath = 'computer_vision/test1/student_data'
mylist = os.listdir(mypath)
i=0
for cl in mylist:
    cl=os.path.splitext(cl)[0]
    mylist[i]=cl.upper()
    i+=1

#print(mylist)   

Name = input("Enter Your Name: ")
Name=Name.upper()

cap = cv.VideoCapture(0)


if Name not in mylist:

    count=0
    #mylist.append(Name)
    print("Press 'S' to start collecting face data and 'Q' to save your picture.")
    userinput = input()

    if userinput !='s':
        print("Enter valid Input ")
        exit()


    while True:

        status, frame = cap.read()
        cv.imshow("Video window",frame)
        gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        cv.imwrite('D:/python/computer_vision/test1/student_data/'+Name+'.jpg',gray)
        if cv.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv.destroyAllWindows()
            break

#else:
 #   exec(open("computer_vision/test1/fac_recog.py").read())
    

        








    
        




   


