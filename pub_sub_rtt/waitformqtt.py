import socket
import time
import sys

host = "mosquitto"
port = 1883  # ou 8883 conforme o container

while True:
    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"Conectado a {host}:{port}")
            break
    except Exception as e:
        print(f"Aguardando {host}:{port}... ({e})")
        time.sleep(2)

sys.exit(0)