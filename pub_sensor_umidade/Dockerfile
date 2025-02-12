FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Cria e entra na pasta de trabalho
WORKDIR /app

# Copia o script para dentro do contêiner
COPY pub_sensor_umidade.py /app

# Instala a biblioteca paho-mqtt
RUN pip install paho-mqtt==1.6.1



# Executa o script
CMD ["python", "-u", "pub_sensor_umidade.py"]


