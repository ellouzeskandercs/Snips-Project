
import numpy as np
import cv2
import pickle
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
def isdavid() : 
	empty = 0 
	face_cascade = cv2.CascadeClassifier('/home/pi/HelloSnips/data/haarcascade_frontalface_alt2.xml')
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read("/home/pi/HelloSnips/face-trainer.yml")

	labels = {"person_name": 1}
	with open("face-labels.pickle", 'rb') as f:
		inv_labels= pickle.load(f)
	labels= {v:k for k,v in inv_labels.items()}
	cap = PiCamera()
	cap.resolution = (640, 480)
	cap.framerate = 32
	rawCapture = PiRGBArray(cap, size=(640, 480))
	time.sleep(0.1)
	start = time.time()
	i = 0
	prop = 4*[0]
	#while(True):
	    # Capture frame-by-frame
	    #ret, frame = cap.read()
	for framep in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):		
		# Our operations on the frame come here
		frame = framep.array
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
		for (x, y, w, h) in faces:
		#print(x,y,w,h)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]

			id_, conf = recognizer.predict(roi_gray)

			if conf>=20 :
				#print(id_)

				prop[id_] = prop[id_] + 1
				font = cv2.FONT_HERSHEY_SIMPLEX
				name = labels[id_]
				color = (255, 255, 255)
				stroke = 2
				cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

				img_item = 'img'+str(i)+'.png'
				i = i + 1
				cv2.imwrite(img_item,roi_color)

			color = (255,0,0)
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h
			cv2.rectangle(frame,(x,y),(end_cord_x,end_cord_y),color,stroke)
		rawCapture.truncate(0)
		if (time.time()-start > 10):
			break
	cap.close()
	if max(prop) < 3 :
		print(prop)
		return([0,""])
	else :
		print(prop)
		return([1,labels[prop.index(max(prop))]])
# When everything done, release the capture

cv2.destroyAllWindows()

