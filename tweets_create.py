import json
import numpy as np
from datetime import datetime
import time
import paho.mqtt.client as mqtt

# Parametroak
json_file = 'tweets1.json'
gap = 4
broker = "mosquitto"  
port = 1883
topic = "tweets"
client_id = "python-producer"

# MQTT broker-era konektatu
client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
client.connect(broker, port, 60)
client.loop_start()

# Tweet-ak kargatu
try:
    with open(json_file, 'r') as file:
        try:
            tweets = json.load(file)
            while True:
                try:
                    user = np.random.randint(len(tweets))
                    tweet = np.random.randint(len(tweets[user]["tweets"]))
                    now = datetime.now()
                    formatted = now.strftime("%Y-%m-%d %H:%M:%S")

                    text = tweets[user]["tweets"][tweet].encode('utf-8','ignore').decode("utf-8").replace('\n', ' ')
                    text += "."
                    text = text.replace('"', "")
                    text = text.replace('\\', "")

                    message = {
                        "user_id": tweets[user]["id"],
                        "tweet": text,
                        "timestamp": formatted
                    }

                    payload = json.dumps(message)
                    client.publish(topic, payload)
                    print(f"[Enviado MQTT] {payload}")
                    time.sleep(2)

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    time.sleep(gap)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
