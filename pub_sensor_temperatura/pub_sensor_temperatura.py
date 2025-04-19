import paho.mqtt.client as mqtt
import time
import random

BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
TOPIC = "home/sensors/temperatura"

def publish_loop():
    client = mqtt.Client("pub_sensor_temperatura")
    client.connect(BROKER_ADDRESS, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            value = round(random.uniform(25.0, 35.0), 2)
            print(f"Mensagem publicada: {value}")
            client.publish(TOPIC, str(value), qos=1)
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

publish_loop()
