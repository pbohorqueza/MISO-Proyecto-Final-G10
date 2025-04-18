import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { SalesService } from '../sales.service';
import { getErrorMessages } from '../../../../shared/validators/error-messages';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { SalesPlanSeller } from '../models/sales';
import { map, Observable, startWith } from 'rxjs';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatChipsModule } from '@angular/material/chips';

const validaciones = {
  'nombre': [
    { type: 'required', message: 'El correo electronico es requerido' }
  ],
  'descripcion': [
    { type: 'required', message: 'El nombre es requerido' }
  ],
  'valor_objetivo': [
    { type: 'required', message: 'El valor objetivo es requerido' },
    { type: 'pattern', message: 'El valor objetivo debe ser un número' },
    { type: 'min', message: 'El valor objetivo debe ser mayor a 0' }
  ],
  'fecha_inicio': [
    { type: 'required', message: 'La fecha de inicio es requerida' },
    { type: 'pattern', message: 'La fecha de inicio debe ser una fecha válida' }
  ],
  'fecha_fin': [
    { type: 'required', message: 'La fecha de fin es requerida' },
    { type: 'pattern', message: 'La fecha de fin debe ser una fecha válida' }
  ],
  'seller_ids': [
    { type: 'required', message: 'Los vendedores son requeridos' },
    { type: 'minlength', message: 'Se requiere al menos un vendedor' }
  ]
};

@Component({
  selector: 'app-create',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatAutocompleteModule,
    MatChipsModule,
    FormsModule
  ],
  templateUrl: './create.component.html',
  styleUrl: './create.component.scss'
})

export class CreateComponent {
  createForm!: FormGroup;
  vendors: SalesPlanSeller[] = [
    { id: 1, seller_id: 1, nombre: 'Vendedor 1' },
    { id: 2, seller_id: 2, nombre: 'Vendedor 2' }
  ];

  filteredVendors: Observable<SalesPlanSeller[]> | undefined;

  private readonly router = inject(Router);
  private readonly fb = inject(FormBuilder);
  private readonly salesService = inject(SalesService);

  getErrorMessages = getErrorMessages;
  validaciones: { [key: string]: { type: string; message: string }[] } = validaciones;

  ngOnInit(): void {
    this.initForm();
  }

  initForm() {
    this.createForm = this.fb.nonNullable.group({
      nombre: ['', [Validators.required]],
      descripcion: ['', [Validators.required]],
      valor_objetivo: ['', [
        Validators.required,
        Validators.pattern(/^\d+(\.\d{1,2})?$/),
        Validators.min(1)
      ]],
      fecha_inicio: ['', [
        Validators.required
      ]],
      fecha_fin: ['', [
        Validators.required
      ]],
      seller_ids: this.fb.array([], [
        Validators.required,
        Validators.minLength(1)
      ]),
      vendorSearch: ['']
    });

    this.filteredVendors = this.createForm.get('vendorSearch')!.valueChanges.pipe(
      startWith(''),
      map(value => this._filterVendors(value || ''))
    );
  }


  private _filterVendors(value: string): SalesPlanSeller[] {
    const filterValue = value.toLowerCase();
    return this.vendors.filter(vendor =>
      vendor.nombre.toLowerCase().includes(filterValue));
  }

  get sellerIds(): FormArray {
    return this.createForm.get('seller_ids') as FormArray;
  }

  addSeller(vendor: SalesPlanSeller): void {
    // Check if vendor is already selected
    const existingIndex = this.getSellerIdIndex(vendor.id);
    if (existingIndex === -1) {
      this.sellerIds.push(this.fb.control(vendor.id));
    }
    // Clear the search input
    this.createForm.get('vendorSearch')?.setValue('');
  }

  removeSeller(index: number): void {
    this.sellerIds.removeAt(index);
  }

  getSellerIdIndex(id: number): number {
    return this.sellerIds.controls.findIndex(control => control.value === id);
  }

  isVendorSelected(id: number): boolean {
    return this.getSellerIdIndex(id) !== -1;
  }

  getVendorName(id: number) {
    const vendor = this.vendors.find(v => v.id === id);

return vendor ? vendor.nombre : id;
  }

  // Format date to YYYY-MM-DD string when date is changed
  onDateChange(event: any, controlName: string): void {
    if (event.value) {
      // Extract the date directly from the event value

      // Set the value in the form
      this.createForm.get(controlName)?.setValue(event.value);
    }
  }

  // Helper method to format date as YYYY-MM-DD
  formatDate(date: Date): string {
    // Create a new date with timezone offset applied to ensure the selected date is preserved

    // Format the adjusted date
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);

    return `${year}-${month}-${day}`;
  }

  onCreate() {
    if (this.createForm.valid) {
      const { nombre, descripcion, valor_objetivo, fecha_inicio, fecha_fin } = this.createForm.value;

      const formattedFechaInicio = this.formatDate(fecha_inicio);
      const formattedFechaFin = this.formatDate(fecha_fin);
      this.salesService.createSale({
        nombre: nombre!,
        descripcion: descripcion!,
        valor_objetivo: Number(valor_objetivo!),
        fecha_inicio: formattedFechaInicio!,
        fecha_fin: formattedFechaFin!,
        seller_ids: this.createForm.value.seller_ids as string[]
      });

      this.router.navigate(['private/sales']);
    } else {
      Object.keys(this.createForm.controls).forEach(key => {
        const control = this.createForm.get(key);
        control?.markAsTouched();
      });
    }
  }

  onCancel(): void {
    this.createForm.reset();
    // Reset the seller_ids array
    while (this.sellerIds.length !== 0) {
      this.sellerIds.removeAt(0);
    }
  }
}
