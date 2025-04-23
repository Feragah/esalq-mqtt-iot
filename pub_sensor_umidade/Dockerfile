FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Cria e entra na pasta de trabalho
WORKDIR /app

# Copia o script de publicação e o script de espera para dentro do contêiner
COPY pub_sensor_umidade.py /app
COPY waitformqtt.py /app

# Instala a biblioteca paho-mqtt e o tcpdump (caso necessário para debug)
RUN pip install paho-mqtt==1.6.1
RUN apt-get update && apt-get install -y tcpdump

# Executa o wait script antes de rodar o publicador
CMD python waitformqtt.py && python -u pub_sensor_umidade.py
