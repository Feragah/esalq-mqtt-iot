declare module "paho-mqtt" {
  export class Client {
    constructor(host: string, clientId: string);
    connect(options: {
      onSuccess?: () => void;
      onFailure?: (error: any) => void;
    }): void;
    disconnect(): void;
    subscribe(topic: string): void;
    onMessageArrived: (message: {
      destinationName: string;
      payloadString: string;
    }) => void;
  }
}
