import paho.mqtt.client as mqtt

BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
TOPIC = "home/sensors"

def on_message(client, userdata, message):
    print("Mensagem recebida:", str(message.payload.decode("utf-8")))

print("Iniciando sub_dashboard...")
client = mqtt.Client("sub_dashboard")
client.on_message = on_message
client.connect(BROKER_ADDRESS, MQTT_PORT, 60)
client.subscribe(TOPIC)
print(f"Assinado no tópico: {TOPIC}")

client.loop_forever()
