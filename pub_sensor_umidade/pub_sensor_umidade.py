import paho.mqtt.client as mqtt
import time
import random
BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
#TOPIC = "home/sensors/umidade"
TOPIC = "home/sensors"
print("Iniciando pub_sensor_umidade...")  # Cheque se existe esse print no começo

client = mqtt.Client("pub_sensor_umidade")
client.connect(BROKER_ADDRESS, MQTT_PORT, 60)

while True:
    valor_aleatorio = random.randint(60, 70)
    message = f"{valor_aleatorio}"
    client.publish(TOPIC, message)
    print(f"Mensagem publicada: {message}")  # Cheque se esse print está presente
    time.sleep(5)
