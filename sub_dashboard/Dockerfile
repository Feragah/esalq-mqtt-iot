FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY sub_dashboard.py /app
RUN pip install paho-mqtt==1.6.1



CMD ["python", "-u", "sub_dashboard.py"]
