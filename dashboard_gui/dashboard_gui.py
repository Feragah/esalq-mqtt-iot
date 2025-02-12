import sys
import re
from collections import deque

import paho.mqtt.client as mqtt

from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer
from PySide6.QtGui import QPixmap, QIcon, QPen, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QDial, QProgressBar, QLCDNumber, QTabWidget, QGroupBox
)
from PySide6.QtCharts import QChart, QChartView, QLineSeries

# --------------------------
# CONFIGURAÇÕES MQTT
# --------------------------
BROKER_ADDRESS = "localhost"  # ou "localhost" se o broker estiver mapeado na 1883
MQTT_PORT = 1883

TOPIC_TEMPERATURA = "home/sensors/temperatura"
TOPIC_UMIDADE     = "home/sensors/umidade"

MAX_TEMPERATURA = 50
MAX_UMIDADE     = 100

# --------------------------
# THREAD MQTT
# --------------------------
class MqttThread(QThread):
    temperaturaSignal = Signal(float)
    umidadeSignal = Signal(float)

    def __init__(self):
        super().__init__()
        self.client = mqtt.Client("sub_dashboard_qt_icons")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def run(self):
        """Inicia o loop MQTT na thread."""
        self.client.connect(BROKER_ADDRESS, MQTT_PORT, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT com sucesso.")
            client.subscribe(TOPIC_TEMPERATURA)
            client.subscribe(TOPIC_UMIDADE)
        else:
            print("Falha ao conectar. Código:", rc)

    def on_message(self, client, userdata, msg):
        texto = msg.payload.decode("utf-8").strip()
        valor = self.extrair_valor_numerico(texto)
        if msg.topic == TOPIC_TEMPERATURA:
            self.temperaturaSignal.emit(valor)
        elif msg.topic == TOPIC_UMIDADE:
            self.umidadeSignal.emit(valor)

    def extrair_valor_numerico(self, texto):
        # Remove caracteres não numéricos/ponto
        texto_limpo = re.sub(r"[^0-9\.]", "", texto)
        try:
            return float(texto_limpo)
        except ValueError:
            return 0.0

# --------------------------
# JANELA PRINCIPAL
# --------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard IoT - Exemplo Avançado com Ícones")

        # Widget central + layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Tabs
        self.tabWidget = QTabWidget()
        main_layout.addWidget(self.tabWidget)

        # Abas: Leitura Atual e Histórico
        self.tabLeituraAtual = QWidget()
        self.tabHistorico = QWidget()
        self.tabWidget.addTab(self.tabLeituraAtual, "Leitura Atual")
        self.tabWidget.addTab(self.tabHistorico, "Histórico Temp")

        # Montar cada aba
        self.setupTabLeitura()
        self.setupTabHistorico()

        # Thread MQTT
        self.mqtt_thread = MqttThread()
        self.mqtt_thread.temperaturaSignal.connect(self.update_temperature)
        self.mqtt_thread.umidadeSignal.connect(self.update_humidity)
        self.mqtt_thread.start()

    # -----------------------------------------
    # ABA 1: Leitura Atual com Ícones
    # -----------------------------------------
    def setupTabLeitura(self):
        layout = QVBoxLayout()
        self.tabLeituraAtual.setLayout(layout)

        # Título no topo
        labelTitulo = QLabel("Leitura de Sensores - Atual")
        labelTitulo.setAlignment(Qt.AlignCenter)
        labelTitulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(labelTitulo)

        # Container (GroupBox) para agrupar Temperatura
        groupTemp = QGroupBox("Temperatura")
        groupTempLayout = QVBoxLayout()
        groupTemp.setLayout(groupTempLayout)

        # Ícone de termômetro na parte superior
        iconTherm = QLabel()
        pixTherm = QPixmap("icons/thermometer.png")  # Ajuste caminho conforme seu projeto
        pixTherm = pixTherm.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        iconTherm.setPixmap(pixTherm)
        iconTherm.setAlignment(Qt.AlignCenter)
        groupTempLayout.addWidget(iconTherm)

        # Layout horizontal: dial + LCD
        tempHLayout = QHBoxLayout()
        groupTempLayout.addLayout(tempHLayout)

        self.dialTemp = QDial()
        self.dialTemp.setRange(0, MAX_TEMPERATURA)
        self.dialTemp.setNotchesVisible(True)
        self.dialTemp.setValue(0)
        tempHLayout.addWidget(self.dialTemp)

        self.lcdTemp = QLCDNumber()
        self.lcdTemp.setDigitCount(5)
        self.lcdTemp.display(0.0)
        tempHLayout.addWidget(self.lcdTemp)

        # Label texto
        self.labelTemp = QLabel("Temperatura: -- °C")
        self.labelTemp.setAlignment(Qt.AlignCenter)
        groupTempLayout.addWidget(self.labelTemp)

        # Container (GroupBox) para Umidade
        groupUmid = QGroupBox("Umidade")
        groupUmidLayout = QVBoxLayout()
        groupUmid.setLayout(groupUmidLayout)

        # Ícone de água (umidade)
        iconWater = QLabel()
        pixWater = QPixmap("icons/water.png")  # Ajuste caminho
        pixWater = pixWater.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        iconWater.setPixmap(pixWater)
        iconWater.setAlignment(Qt.AlignCenter)
        groupUmidLayout.addWidget(iconWater)

        # Layout horizontal: progress bar + LCD
        umidHLayout = QHBoxLayout()
        groupUmidLayout.addLayout(umidHLayout)

        self.progressUmid = QProgressBar()
        self.progressUmid.setRange(0, MAX_UMIDADE)
        self.progressUmid.setValue(0)
        umidHLayout.addWidget(self.progressUmid)

        self.lcdUmid = QLCDNumber()
        self.lcdUmid.setDigitCount(5)
        self.lcdUmid.display(0.0)
        umidHLayout.addWidget(self.lcdUmid)

        # Label texto
        self.labelUmid = QLabel("Umidade: -- %")
        self.labelUmid.setAlignment(Qt.AlignCenter)
        groupUmidLayout.addWidget(self.labelUmid)

        # Agora, colocar groupTemp e groupUmid lado a lado
        hSensorsLayout = QHBoxLayout()
        hSensorsLayout.addWidget(groupTemp)
        hSensorsLayout.addWidget(groupUmid)

        layout.addLayout(hSensorsLayout)

    # -----------------------------------------
    # ABA 2: Histórico de Temperatura (gráfico)
    # -----------------------------------------
    def setupTabHistorico(self):
        layout = QVBoxLayout()
        self.tabHistorico.setLayout(layout)

        # Guardar últimos N valores no deque
        self.temp_history = deque(maxlen=50)

        # Série e Chart
        self.seriesTemp = QLineSeries()
        self.seriesTemp.setName("Temperatura (°C)")

        self.chart = QChart()
        self.chart.addSeries(self.seriesTemp)
        self.chart.setTitle("Histórico de Temperatura")
        self.chart.createDefaultAxes()
        self.chart.axisX(self.seriesTemp).setTitleText("Amostras")
        self.chart.axisY(self.seriesTemp).setRange(0, MAX_TEMPERATURA)
        self.chart.axisY(self.seriesTemp).setTitleText("Temperatura (°C)")

        pen = QPen(QColor("red"))
        pen.setWidth(2)
        self.seriesTemp.setPen(pen)

        chartView = QChartView(self.chart)
        layout.addWidget(chartView)

        # Timer para atualizar o gráfico (1s)
        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.updateTempChart)
        self.updateTimer.start(1000)

    # -----------------------------------------
    # Slots de Atualização (recebem valores da thread MQTT)
    # -----------------------------------------
    @Slot(float)
    def update_temperature(self, valor):
        if valor < 0:
            valor = 0
        if valor > MAX_TEMPERATURA:
            valor = MAX_TEMPERATURA

        # Atualiza dial, LCD e label
        self.dialTemp.setValue(int(valor))
        self.lcdTemp.display(valor)
        self.labelTemp.setText(f"Temperatura: {valor:.1f} °C")

        # Salva no histórico
        self.temp_history.append(valor)

    @Slot(float)
    def update_humidity(self, valor):
        if valor < 0:
            valor = 0
        if valor > MAX_UMIDADE:
            valor = MAX_UMIDADE

        self.progressUmid.setValue(int(valor))
        self.lcdUmid.display(valor)
        self.labelUmid.setText(f"Umidade: {valor:.1f} %")

    def updateTempChart(self):
        # Redesenha a série de temperatura no gráfico
        self.seriesTemp.clear()
        for i, v in enumerate(self.temp_history):
            self.seriesTemp.append(i, v)

# --------------------------
# MAIN
# --------------------------
def main():
    app = QApplication(sys.argv)

    # (Opcional) Definir um ícone para a janela principal
    # app.setWindowIcon(QIcon("icons/thermometer.png"))

    window = MainWindow()
    window.resize(800, 500)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
