import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxGaugeModule } from 'ngx-gauge'; // ✅ Importação corrigida!

@Component({
  selector: 'app-gauge',
  standalone: true,
  imports: [CommonModule, NgxGaugeModule], // ✅ Agora usando NgxGaugeModule
  template: `
    <ngx-gauge
      [value]="value"
      [label]="label"
      [min]="min"
      [max]="max"
      type="arch"
      cap="round"
      [thick]="10"
      [append]="unit"
      [foregroundColor]="color"
    >
    </ngx-gauge>
  `,
  styles: [
    `
      ngx-gauge {
        width: 200px;
        height: 200px;
      }
    `,
  ],
})
export class GaugeComponent {
  @Input() value: number = 0;
  @Input() label: string = '';
  @Input() min: number = 0;
  @Input() max: number = 100;
  @Input() unit: string = '';
  @Input() color: string = '#007bff';
}
