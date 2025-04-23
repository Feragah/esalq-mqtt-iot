FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Copia os scripts para o contêiner
COPY sub_dashboard.py /app
COPY waitformqtt.py /app

# Instala dependências
RUN pip install paho-mqtt==1.6.1
RUN apt-get update && apt-get install -y tcpdump

# Aguarda o Mosquitto estar disponível na porta 1883, depois executa o consumidor
CMD python waitformqtt.py && python -u sub_dashboard.py
