import paho.mqtt.client as mqtt
import time
import random

BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
TOPIC = "home/sensors/temperatura"
#TOPIC = "home/sensors"
print("Iniciando pub_sensor_temperatura...")  # Cheque se existe esse print no começo

client = mqtt.Client("pub_sensor_temperatura")
client.connect(BROKER_ADDRESS, MQTT_PORT, 60)

while True:
    valor_aleatorio = random.uniform(15, 40)
    message = f"{valor_aleatorio:.2f}"
    client.publish(TOPIC, message)
    print(f"Mensagem publicada: {message}")  # Cheque se esse print está presente
    time.sleep(5)
