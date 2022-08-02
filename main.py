import PySimpleGUI as sg
import cv2
import numpy as np


def main():
    sg.theme('Black')

    # Define the window layout
    layout = [[sg.Text('174 Computer Vision: Final Project', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 14'),
               sg.Button('RED', size=(10, 1), font='Helvetica 14'),
               sg.Button('BLUE', size=(10, 1), font='Helvetica 14'),
               sg.Button('GREEN', size=(10, 1), font='Helvetica 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), 
                ]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, location=(800, 400))

    # Event LOOP Read and display frames, operate the GUI
    cap = cv2.VideoCapture(0)
    recording = False

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    red = False
    blue = False
    green = False

    #checking for button press
    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            recording = False
            return

        elif event == 'Start':
            recording = True

        elif event == 'RED':
            recording = True

            red = True
            blue = False
            green = False

        elif event == 'BLUE':
            recording = True
            
            red = False
            blue = True
            green = False
        
        elif event == 'GREEN':
            recording = True
            
            red = False
            blue = False
            green = True

        if recording:
            ret, frame = cap.read()    

            frame = cv2.GaussianBlur(frame,(11,11),1)

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(frame_gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  
                cv2.rectangle(frame, (x+25, y+25), (x+w-25, y+h-25), (0, 255, 0), 2)  

            #change the values for skin based on state (RED|BLUE|GREEN) 
            if len(faces) > 0:

                #set lower and upper bounds (hsv)    
                brown_lo=np.array([10,50,100])
                brown_hi=np.array([23,255,255])

                
                #OPTION 1 --------------------------------------------------------------------------
                #mask = cv2.inRange(frame_hsv, brown_lo, brown_hi)

                #patch_image = frame_hsv[y:h,x:w]

                #good enough values
                # brown_lo=np.array([7,7,30])
                # brown_hi=np.array([65,55,190])

                #END OF OPTION 1 --------------------------------------------------------------------------


                #OPTION 2 --------------------------------------------------------------------------
                #USING BGR MASK
                brown_lo2=np.array([9,9,35])
                brown_hi2=np.array([65,55,210])
                mask = cv2.inRange(frame, brown_lo2, brown_hi2)

                #END OF OPTION 1 --------------------------------------------------------------------------

                if red:
                    frame[mask>0] = (30,30,200)
                elif blue:
                    frame[mask>0] = (200,30,30)
                elif green:
                    frame[mask>0] = (30,200,30)

                imgbytes = cv2.imencode('.png', frame)[1].tobytes() 
                window['image'].update(data=imgbytes)

if __name__ == '__main__':
    main()

#SELF RECOMMENDATIONS
    # HSV RANGE FOR SKIN SHOULD BE BASED FROM/CALCULATED FROM FACE DETECTION  
    # INCREMENTS TO THE SPECIFIC COLOR SHOULD BE DYNAMIC
