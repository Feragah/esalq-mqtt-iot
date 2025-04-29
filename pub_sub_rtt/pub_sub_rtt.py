import paho.mqtt.client as mqtt
import time
import threading

BROKER_ADDRESS = "mosquitto"
MQTT_PORT = 1883
TOPIC = "home/RTT"
CA_CERT = "/certs/ca.crt"  # caminho onde o cliente encontrará o certificado da CA
# Dicionário para armazenar os timestamps das mensagens enviadas
sent_messages = {}

# Função de envio periódico
def publish_loop():
    client_id = 0
    while True:
        timestamp = time.time() * 1000  # milissegundos
        message_id = f"ping:{client_id}:{timestamp} : Teste Payload"
        sent_messages[str(client_id)] = timestamp
        client.publish(TOPIC, message_id, qos=1)
        print(f"Mensagem publicada: {message_id}")
        client_id += 1
        time.sleep(2)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de retorno: {rc}")
    client.subscribe(TOPIC, qos=1)
    print(f"Assinado no tópico: {TOPIC} (sessão persistente)")

def on_message(client, userdata, message):
    received_time = time.time() * 1000  # milissegundos
    payload = message.payload.decode("utf-8")

    if payload.startswith("ping:"):
        try:
            parts = payload.split(":")
            msg_id = parts[1]
            sent_time = float(parts[2])
            rtt = received_time - sent_time
            print(f"Mensagem recebida: {payload}")
            print(f"RTT da mensagem {msg_id}: {rtt:.2f} ms")
        except Exception as e:
            print(f"Erro ao calcular RTT: {e}")
    else:
        print("Mensagem recebida (não é ping):", payload)

print("Iniciando pub_sub_RTT com sessão persistente...")

client = mqtt.Client(client_id="pub_sub_RTT", clean_session=False)

client.on_connect = on_connect
client.on_message = on_message
# Configura TLS
#client.tls_set(ca_certs=CA_CERT)  # Usando o certificado CA para a verificação
client.connect(BROKER_ADDRESS, MQTT_PORT, keepalive=60)

# Inicia o loop de recebimento de mensagens em uma thread separada
client.loop_start()

# Inicia o envio periódico em outra thread
publish_thread = threading.Thread(target=publish_loop, daemon=True)
publish_thread.start()

# Mantém o script ativo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando cliente MQTT...")
    client.loop_stop()
    client.disconnect()
