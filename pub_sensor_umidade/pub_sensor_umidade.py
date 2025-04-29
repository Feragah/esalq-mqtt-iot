import paho.mqtt.client as mqtt
import time
import random

BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
TOPIC = "home/sensors"
#TOPIC = "home/sensors/umidade"
#CA_CERT = "/certs/ca.crt"  # caminho onde o cliente encontrará o certificado da CA

def publish_loop():
    print("Iniciando pub_sensor_umidade...")  # Cheque se existe esse print no começo
    client = mqtt.Client("pub_sensor_umidade")
     # Configura TLS
    #client.tls_set(ca_certs=CA_CERT)  # Usando o certificado CA para a verificação
    time.sleep(5)
    client.connect(BROKER_ADDRESS, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            valor_aleatorio = random.randint(60, 70)
            message = f"{valor_aleatorio}"
            client.publish(TOPIC, message, qos=1, retain=True)
            print(f"Mensagem publicada: {message}")  # Cheque se esse print está presente
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

publish_loop()
