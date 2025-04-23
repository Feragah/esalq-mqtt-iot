import paho.mqtt.client as mqtt
import time
import random

BROKER_ADDRESS = "mosquitto"  # nome do serviço/container no Docker Compose
MQTT_PORT = 1883  # porta TLS
TOPIC = "home/sensors/temperatura"
#CA_CERT = "/certs/ca.crt"  # caminho onde o cliente encontrará o certificado da CA

def publish_loop():
    client = mqtt.Client("pub_sensor_temperatura")

    # Configura TLS
    #client.tls_set(ca_certs=CA_CERT)  # Usando o certificado CA para a verificação

    # Conectar ao broker MQTT
    client.connect(BROKER_ADDRESS, MQTT_PORT, keepalive=60)

    # Iniciar o loop para gerenciar a conexão
    client.loop_start()

    try:
        while True:
            # Gerar um valor de temperatura aleatório
            value = round(random.uniform(25.0, 35.0), 2)
            print(f"Mensagem publicada: {value}")
            
            # Publicar o valor de temperatura no tópico
            client.publish(TOPIC, str(value), qos=1)
            
            # Esperar 3 segundos antes de publicar a próxima mensagem
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        # Parar o loop e desconectar
        client.loop_stop()
        client.disconnect()

# Chamada para iniciar o loop de publicação
publish_loop()
