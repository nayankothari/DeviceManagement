"""
Import Paho mqtt library for establish connections between server to client.
for installation of paho-mqtt use pip
pip install paho-mqtt
"""
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json, time


def on_connect(client, userdata, flag, rc):
    """
    This function come in action when script executed,
    when the rc is 0 then it means no error occur during connection
    between subscriber and broker server.
    """
    print("connected with result code: ", str(rc))
    client.subscribe("SERVER_SUBSCRIBER_DETAILS_HERE")


def on_message(client, userdata, msg):
    """
    This Function come in action When publisher publish
    a message to subscriber.
    We can use database to store values that we receive from clients.
    """
    message = bytes(msg.payload).decode()
    message2 = json.loads(message)
    try:
        site_id = message2.get("site_id")
        with open("temp_database//"+site_id+".json", "w") as f:
            json.dump(message2.get("device_details"), f)

    except Exception as e:
        print(e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
while True:
    try:
        client.connect("test.mosquitto.org", 1883, 60)
        break
    except:
        print("connection failed retry to connect.")
        time.sleep(2)

# client.username_pw_set()

# this loop_forever function use to keep connection active always.
client.loop_forever()


