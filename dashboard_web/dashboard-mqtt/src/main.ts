import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { MqttService } from './app/services/mqtt.service';

bootstrapApplication(AppComponent, {
  providers: [MqttService],
}).catch((err) => console.error(err));
