import json
import paho.mqtt.client as mqttClient
import time
import random as r

dictionary = eval(open("tokens_localhost.txt").read())
print(dictionary)

broker_address= "localhost"
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

#topic= "channels/" + str(channel_id) +  "/messages/node1"
topic= "channels/" + str(channel_id) +  "/control"
topic_end = "control"
#topic = "bullshittopic"
data = {} #json dictionary

node_nb=5
 
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
        if topic_end== "control":
            timestamp = time.time()
            data = [{"bn":"","n":"Temperature", "u":"C","v":25, "t":timestamp}]
            client.publish(topic,json.dumps(data))  
            time.sleep(2)
        else:
            for i in range(node_nb):
                nodeid= "node"+str(i)+":"
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
                # topic= "channels/" + str(channel_id) +  "/control/PH"
                client.publish(topic,json.dumps(payload1)) 
                #  topic= "channels/" + str(channel_id) +  "/control/DO"
                client.publish(topic,json.dumps(payload2)) 
                # topic= "channels/" + str(channel_id) +  "/control/Temperature"
                client.publish(topic,json.dumps(payload3)) 
                time.sleep(2)
 
except KeyboardInterrupt:
    print("bye bye")
    client.disconnect()
    client.loop_stop()
