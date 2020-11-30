import paho.mqtt.client as mqtt 
import json
import time
from facerecognition import isdavid
def on_connect(client, userdata, flags, rc): 
	print('Connected') 
	mqtt1.subscribe('cam/mov')	
	mqtt1.subscribe('cam/speak')
def on_connect2(client, userdata, flags, rc): 
	print('Connected2') 
def on_subscribe(client, userdata, mid, granted_qos):
	print('subscribed')
def on_message(client,userdata,msg):
	if msg.topic == 'cam/mov' : 	# le topic correspondant à la demande : is someone in the next room ? 
		print("test")	
		m_decode= str(msg.payload.decode("utf-8","ignore")) # les trois lignes suivantes servent à decoder le msg 
		m_decode  = m_decode[1:len(m_decode)-1]
		b = m_decode.split("%")
		if b[0] == '0'	: # si c'est une demande 
			T = isdavid()	
			
			if T[1] : # si la réponse est positive
				text = "Yes" + T[1] + "is in the next room"
			else : #si la réponse est négative
				text = "No Sorry the next room is empty"
			a = {"text": text ,'siteId'  : 'default'}
			data_out=json.dumps(a)
			mqtt2.publish('hermes/tts/say',data_out)
			mqtt1.publish('cam/mov',json.dumps("1%"+str(T[0])+"%"+T[1]+" "))
	if msg.topic == 'cam/speak' :# le topic correspondant à une conversation
		mqtt1.subscribe('hermes/asr/textCaptured')		# être alerté quand l'utilisateur parle 
		m_decode= str(msg.payload.decode("utf-8","ignore"))
		m_decode  = m_decode[1:len(m_decode)-1]
		b = m_decode.split("%")
		print(b)
		if "end conversation" in b[1] : 
			mqtt1.unsubscribe('hermes/asr/textCaptured')		
		if b[0] == "1" : 			
			a = {"text": b[1] ,'siteId'  : 'default'}
			data_out=json.dumps(a)
			mqtt1.publish('hermes/tts/say',data_out)
	if msg.topic == 'hermes/asr/textCaptured' :
		m_decode= str(msg.payload.decode("utf-8","ignore"))
		m_decode = m_decode[9:m_decode.index(',')-1]
		
		a = json.dumps("0%"+m_decode) # le 0,1 correspondent aux différents utilisateurs 
		mqtt1.publish('cam/speak',a) # on envoie ce qu'on dit 
	
#print(str(isdavid()))
mqtt1 = mqtt.Client()
mqtt2 = mqtt.Client()
mqtt1.connect('snips.local', 1883) 
mqtt1.loop_start()
mqtt1.on_connect = on_connect
mqtt1.on_message = on_message
mqtt1.on_subscribe = on_subscribe
mqtt2.connect('snips2.local', 1883) 
mqtt2.loop_start()
mqtt2.on_connect = on_connect2

while True :
	mqtt1.loop_start()
	mqtt2.loop_start()
	time.sleep(3)
	mqtt1.loop_stop()
	mqtt2.loop_stop()
