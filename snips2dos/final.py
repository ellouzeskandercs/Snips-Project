import paho.mqtt.client as mqtt 
import json
import time

def on_connect1(client, userdata, flags, rc): 
	if client==mqtt1:	
		print('Connected1') 
		mqtt1.subscribe('hermes/intent/Skander97:someone') #l'intent qui correspont à la demande : is someone in the next room ? 
		
def on_connect2(client, userdata, flags, rc): 
	print('Connected2') 
	
def on_publish(client,userdata,result):
	if client==mqtt1:	
		print('published1')
	else:
		print('published2')
def on_disconnect(client,userdata,rc):
	if client==mqtt1: 
		T1 = False
	else:
		T2=False
def on_message(client,userdata,msg):
	if msg.topic == 'hermes/intent/Skander97:someone' : # si la demande est : is someone in the next room ? 
		a = json.dumps("0%0% ")
		mqtt2.publish('cam/mov',a)  # on envoie la demande au second appareil qui est souscrit sur ce topic
		mqtt2.subscribe('cam/mov') # on souscrit pour écouter la réponse
		print("okkkk")
	if msg.topic  == 'hermes/intent/Skander97:No':  # si la demande est : i don't want to talk with him 
		mqtt1.unsubscribe('hermes/intent/Skander97:yes') 
		mqtt1.unsubscribe('hermes/intent/Skander97:no')
 
	if msg.topic  == 'hermes/intent/Skander97:yes' : # si la demande est : i want to talk with him
		print('confirmed')	
		mqtt1.subscribe('hermes/asr/textCaptured')		# etre alerté quand l'utilisateur a parlé 
		mqtt2.subscribe('cam/speak')	# correspond au topic ou les messages entre les deux appareils von circuler
		mqtt1.unsubscribe('hermes/intent/Skander97:yes')
		mqtt1.unsubscribe('hermes/intent/Skander97:no')

	
	if msg.topic  == 'hermes/asr/textCaptured' :
		intent_json = json.loads(msg.payload)
		print("1%"+intent_json['text'])
		a = json.dumps("1%"+intent_json['text'])
		mqtt2.publish('cam/speak',a) # on envoie le texte capturé à l'autre appareil 
		print('sent')
		
	
		

def on_message2(client,userdata,msg):
	print(msg.topic)
	if msg.topic == 'cam/mov' : 
		m_decode= str(msg.payload.decode("utf-8","ignore"))
		m_decode  = m_decode[1:len(m_decode)-1]
		a = m_decode.split("%")
		print(a)
		if a[0] == '1' and a[1] == "1"	:
			speak_1('would you like to talk to him')
			mqtt1.subscribe('hermes/intent/Skander97:yes')
			mqtt1.subscribe('hermes/intent/Skander97:no')
			mqtt2.unsubscribe('cam/mov')

	if msg.topic == 'cam/speak' :
		m_decode= str(msg.payload.decode("utf-8","ignore"))
		m_decode  = m_decode[1:len(m_decode)-1]
		b = m_decode.split("%")
		print(b)
		if "end conversation" in b[1] : 
			mqtt1.subscribe('hermes/asr/textCaptured')
			mqtt1.unsubscribe('hermes/asr/textCaptured')		
			mqtt2.unsubscribe('cam/speak')	
		if b[0] == "0" : 			
			a = {"text": b[1] ,'siteId'  : 'default'}
			data_out=json.dumps(a)
			mqtt1.publish('hermes/tts/say',data_out)
	
def speak_1(msg):
	# Parse the json response
	print("speak1")
	global T1,P1	
	a = {"text": msg ,'siteId'  : 'default'}
	data_out=json.dumps(a)
	mqtt1.publish('hermes/tts/say',data_out)
	


def speak_2(msg):
	# Parse the json response
	global T2,P2	
	a = {"text": msg ,'siteId'  : 'default'}
	data_out=json.dumps(a)
	mqtt2.publish('hermes/tts/say',data_out)


mqtt1 = mqtt.Client()
mqtt2 = mqtt.Client()
mqtt2.connect('snips.local', 1883) 
mqtt1.connect('snips2.local', 1883) 
mqtt2.loop_start()
mqtt1.loop_start()
mqtt1.on_publish = on_publish
mqtt1.on_disconnect = on_disconnect
mqtt1.on_connect = on_connect1
mqtt1.on_message = on_message
mqtt2.on_publish = on_publish
mqtt2.on_disconnect = on_disconnect
mqtt2.on_connect = on_connect2
mqtt2.on_message = on_message2
while True :
	mqtt2.loop_start()
	mqtt1.loop_start()
	time.sleep(3)
	mqtt2.loop_stop()
	mqtt1.loop_stop()
print("aa")
MQTT_ADDR = "localhost:1883"        # Specify host and port for the MQTT broker

