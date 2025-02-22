import json
import paho.mqtt.client as mqttClient
import time
import random as r

dictionary = eval(open("tokens.txt").read())
print(dictionary)

broker_address= "54.171.128.181"
port = 1883
thing_id = dictionary["thing1_id"]
thing_key= dictionary["thing1_key"]
channel_id = dictionary["channel_id"]
clientID = "thing1: data publisher"
 
client = mqttClient.Client(clientID)               #create new instance
client.username_pw_set(thing_id, thing_key)    #set username and password

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

Connected = False   #global variable for the state of the connection
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker

topic= "channels/" + str(channel_id) +  "/messages"
data = {} #json dictionary


 
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
            temperature = r.uniform(15, 22)
            ph = r.uniform(1, 14)
            do = r.uniform(100, 200)
            conductivity = r.uniform(10, 20)
            lux = r.uniform(100, 400)
            flow = r.uniform(1, 40)
            timestamp = time.time()
            payload1 = [{"bn":"","n":"PH", "u":"C","v":ph, "t":timestamp}]
            payload2 = [{"bn":"","n":"DO", "u":"C","v":do, "t":timestamp}]
            payload3 = [{"bn":"","n":"Temperature", "u":"C","v":temperature, "t":timestamp}]
            client.publish(topic,json.dumps(payload1)) 
            client.publish(topic,json.dumps(payload2)) 
            client.publish(topic,json.dumps(payload3)) 
            time.sleep(2)
 
except KeyboardInterrupt:
    print("bye bye")
    client.disconnect()
    client.loop_stop()
