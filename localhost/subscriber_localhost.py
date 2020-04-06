import paho.mqtt.client as mqtt
import json
import time

dictionary = eval(open("tokens_localhost.txt").read())
print(dictionary)

broker_address= "localhost"
port = 1883
thing_id = dictionary["thing2_id"] #app id
print(thing_id)
thing_key= dictionary["thing2_key"]
print(thing_key)
channel_id= dictionary["channel_id"]
print(channel_id)
clientID = "thing2: subscribed to data"

topic= "channels/" + str(channel_id) +  "/control"
#topic= "GetSR/" + str(channel_id) +  "/sensors"
#topic = "bullshittopic"
def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	client.subscribe(topic)

def on_message(client, userdata, msg):
	print ("RX")
	message=str(msg.payload.decode('UTF-8')) #message is string now, not json
	print(message)
	message = eval(message) #transform to dictionary
	print(message['type'])
	if str(message['type']) == "SET_SR": 
		print("yes")
		SetSR(message['sensor'], message['v'], message['u'])
	else:
		print("not this type of message")

def SetSR(sensor, value, unit):
	global client, topic
	print ("Setting the SR of the " + str(sensor) + " sensor to "+ str(value) +str(unit))
	timestamp = time.time()
	#data = [{"bn":"","n":sensor, "u":unit,"v":value, "t":timestamp}]
	#print(data)
	data = [{"bn":"","n":sensor, "u":unit,"v":int(value), "t":timestamp}]
	client.publish(topic,json.dumps(data))  


client = mqtt.Client()
client.username_pw_set(thing_id,thing_key)
#client.username_pw_set("mqtt-redis","mqtt")
client.on_connect= on_connect
client.on_message= on_message
client.connect(broker_address,port)
client.loop_forever()
