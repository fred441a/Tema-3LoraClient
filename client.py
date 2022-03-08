import paho.mqtt.client as mqtt
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

def openMap():
    us_cities = pd.read_csv(r"mapdata.csv")
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Time"],
                            color_discrete_sequence=["fuchsia"], zoom=15, height=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")#"v3/fedtfirmatracker@eu1/devices/eui-70b3d57ed004da2b}/up")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "v3/fedtfirmatracker@ttn/devices/eui-70b3d57ed004da2b/up":
        data = json.loads(msg.payload)
        with open("mapdata.csv", "w") as file:
            coord = data["uplink_message"]["decoded_payload"]["text"].split(",")
            file.write(f"City,State,Time,lat,lon\nUCN,Aalborg,{datetime.now().strftime('%d/%m/%Y %H:%M:%S')},{coord[0]},{coord[1]}")
        openMap()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("fedtfirmatracker@ttn", "NNSXS.F7KJ7YXAQFXTA4J4FFPPAYFJNENNGZMSF3TV4QI.HEBRUV5J7OZFJ7IAAE7NIXHAHQJPHHCS77K7LI26ZKN6Z57U7JWQ")
client.connect("eu1.cloud.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()