import paho.mqtt.client as mqtt
import json

dictionary = eval(open("tokens.txt").read())
print(dictionary)

broker_address= "54.171.128.181"
port = 1883
thing_id = dictionary["thing2_id"] #app id
print(thing_id)
thing_key= dictionary["thing2_key"]
print(thing_key)
channel_id= dictionary["channel_id"]
print(channel_id)
clientID = "thing2: subscribed to data"

topic= "channels/" + str(channel_id) +  "/messages"

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	client.subscribe(topic)

def on_message(client, userdata, msg):
	message=str(msg.payload.decode('UTF-8'))
	print(message)

client = mqtt.Client()
client.username_pw_set(thing_id,thing_key)
client.on_connect= on_connect
client.on_message= on_message
client.connect(broker_address,port)
client.loop_forever()
