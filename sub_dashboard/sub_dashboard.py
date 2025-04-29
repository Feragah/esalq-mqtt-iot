import paho.mqtt.client as mqtt

BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
TOPIC = "home/sensors/#"
#CA_CERT = "/certs/ca.crt"  # caminho onde o cliente encontrará o certificado da CA

def on_message(client, userdata, message):
    print("Mensagem recebida:", str(message.payload.decode("utf-8")))

print("Iniciando sub_dashboard com sessão persistente...")

# Cria o cliente com Clean Session = False
client = mqtt.Client(client_id="sub_dashboard", clean_session=False)

client.on_message = on_message
# Configura TLS
#client.tls_set(ca_certs=CA_CERT)  # Usando o certificado CA para a verificação
# Conecta ao broker
client.connect(BROKER_ADDRESS, MQTT_PORT, keepalive=60)

# Subscreve ao tópico com QoS 1
client.subscribe(TOPIC, qos=1)

print(f"Assinado no tópico: {TOPIC} (sessão persistente)")

client.loop_forever()
