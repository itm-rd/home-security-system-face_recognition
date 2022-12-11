import requests
import face_recognition
import cv2
import numpy as np
import telepot
from gpiozero import  DistanceSensor,Button,MotionSensor,LED
import time
import os

chat_id=........
bot_token = '.......'
bot=telepot.Bot('........')

def telegram_bot_sendtext(bot_message):
   bot_token = '..........'
   bot_chatID = '.........'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)

   return response.json()


directory_path = os.getcwd()
folder_name = os.path.basename(directory_path)
face_folder=os.path.join(directory_path,"faces")
known_face_encodings =[]
known_face_names = []

for root, dirs, files in os.walk(face_folder, topdown=True):
    for name in files:
        member_img = face_recognition.load_image_file(os.path.join(face_folder,name))
        encoding = face_recognition.face_encodings(member_img)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name.replace(".png","").lower())
print(known_face_names)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

sensor= DistanceSensor(echo =18,trigger=17)
video_capture = cv2.VideoCapture(0)
try:    
        button=Button(27)
        if button.is_pressed:
            pir=MotionSensor(22)
            if pir.motion_detected:
                test = telegram_bot_sendtext(f"{name}Unusual Motion Detect at {time.ctime()}")
        else:
            print("no")
        a=sensor.distance*100
        time.sleep(0.5)
        
        if a<99:
            while True:
                # Grab a single frame of video
                ret, frame = video_capture.read()
                cv2.imwrite(os.path.join(directory_path,'current','currentimg.jpg'),frame)
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    # if GPIO.input (IR_PIN)== True:
                    #             print("close.............")
                    #             p.start(8.8)
                                
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        test = telegram_bot_sendtext(f"{name} parson Detect at {time.ctime()}")
                        bot.sendPhoto(chat_id,photo=open('current/currentimg.jpg','rb'))
                        #os.remove("current/currentimg.jpg")
                        time.sleep(5)
                        # Or instead, use the known face with the smallest distance to the new face
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            print(name)
                            test = telegram_bot_sendtext(f"{name} Entered at {time.ctime()}")
                            bot.sendPhoto(chat_id,photo=open('current/currentimg.jpg','rb'))
                            os.remove("current/currentimg.jpg")
                        if name in known_face_names:
                                print("Door open")                             
                                time.sleep(10)
                        else:
                                print("door close")
                                os.remove("current/currentimg.jpg")                                              
                        face_names.append(name)
                process_this_frame = not process_this_frame
                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
              
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # Display the resulting image
                cv2.imshow('Video', frame)    
                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
except KeyboardInterrupt:
  video_capture.release()
  cv2.destroyAllWindows()
