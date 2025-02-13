import { Injectable } from '@angular/core';
import mqtt, { MqttClient, IClientOptions } from 'mqtt';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MqttService {
  private client!: MqttClient;
  private temperaturaSubject = new BehaviorSubject<number>(0);
  private umidadeSubject = new BehaviorSubject<number>(0);

  temperatura$ = this.temperaturaSubject.asObservable();
  umidade$ = this.umidadeSubject.asObservable();

  constructor() {
    this.connectMQTT();
  }

  private connectMQTT() {
    const options: IClientOptions = {
      protocol: 'ws',
      hostname: 'mosquitto', // Nome do serviço Mosquitto no Docker Compose
      port: 9001,
    };

    this.client = mqtt.connect(options);

    this.client.on('connect', () => {
      console.log('Conectado ao MQTT');
      this.client.subscribe('home/sensors/temperatura');
      this.client.subscribe('home/sensors/umidade');
    });

    this.client.on('message', (topic: string, message: Buffer) => {
      const value = parseFloat(message.toString());
      if (topic === 'home/sensors/temperatura') {
        this.temperaturaSubject.next(value);
      } else if (topic === 'home/sensors/umidade') {
        this.umidadeSubject.next(value);
      }
    });

    this.client.on('error', (error: any) => {
      console.error('Erro MQTT:', error);
    });
  }
}
