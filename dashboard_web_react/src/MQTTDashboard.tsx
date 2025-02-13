import { useState, useEffect } from "react";
import { Client } from "paho-mqtt";



import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// Definição dos tipos de dados recebidos
interface SensorData {
  time: string;
  value: number;
}

const MQTTDashboard: React.FC = () => {
  const [temperatura, setTemperatura] = useState<SensorData[]>([]);
  const [umidade, setUmidade] = useState<SensorData[]>([]);

  useEffect(() => {
    const client = new Client("ws://localhost:9001/mqtt", "dashboard_" + Math.random());


    client.connect({
      onSuccess: () => {
        console.log("Conectado ao MQTT!");
        client.subscribe("home/sensors/temperatura");
        client.subscribe("home/sensors/umidade");
      },
      onFailure: (error) => console.error("Erro ao conectar:", error),
    });

    client.onMessageArrived = (message) => {
      const topic = message.destinationName;
      const value = parseFloat(message.payloadString);

      if (topic === "home/sensors/temperatura") {
        setTemperatura((prev) => [...prev, { time: new Date().toLocaleTimeString(), value }]);
      } else if (topic === "home/sensors/umidade") {
        setUmidade((prev) => [...prev, { time: new Date().toLocaleTimeString(), value }]);
      }
    };

    return () => client.disconnect();
  }, []);

  return (
    <div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Dashboard MQTT</h1>

      <div className="w-full max-w-3xl bg-white p-4 rounded shadow">
        <h2 className="text-lg font-semibold">Temperatura (°C)</h2>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={temperatura}>
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#ff3d00" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="w-full max-w-3xl bg-white p-4 mt-4 rounded shadow">
        <h2 className="text-lg font-semibold">Umidade (%)</h2>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={umidade}>
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#007bff" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MQTTDashboard;
