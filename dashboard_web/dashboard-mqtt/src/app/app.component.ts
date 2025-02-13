import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GaugeComponent } from './components/gauge/gauge.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    GaugeComponent, // ✅ Certifique-se de que está importando corretamente
  ],
  template: `
    <div class="dashboard">
      <h1>Dashboard MQTT</h1>
      <div class="gauge-container">
        <app-gauge
          [value]="temperatura"
          [label]="'Temperatura (°C)'"
          [min]="0"
          [max]="50"
          [unit]="'°C'"
          [color]="'#ff3d00'"
        >
        </app-gauge>

        <app-gauge
          [value]="umidade"
          [label]="'Umidade (%)'"
          [min]="0"
          [max]="100"
          [unit]="'%'"
          [color]="'#007bff'"
        >
        </app-gauge>
      </div>
    </div>
  `,
  styles: [
    `
      .dashboard {
        text-align: center;
        font-family: Arial, sans-serif;
      }

      .gauge-container {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 20px;
      }
    `,
  ],
})
export class AppComponent {
  temperatura: number = 0;
  umidade: number = 0;
}
