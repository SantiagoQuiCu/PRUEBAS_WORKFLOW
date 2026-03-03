import { Component, OnInit } from '@angular/core';
import { VehiculoService } from './vehiculo/vehiculo.service';
import { MarcaService } from './marca/marca.service';
import { Vehiculo } from './vehiculo/vehiculo';
import { Marca } from './marca/marca';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  vistaActual = 'principal';
  vehiculos: Vehiculo[] = [];
  marcas: Marca[] = [];
  vehiculoSeleccionado: Vehiculo | null = null;
  marcaSeleccionada: Marca | null = null;
  reporteMarcas: any = null;
  mensaje: string = '';
  tipoMensaje: 'success' | 'error' | '' = '';
  
  nuevoVehiculo = {
    modelo: '',
    anio: 0,
    precio: 0,
    color: '',
    marca_id: 0
  };
  
  nuevaMarca = {
    nombre: '',
    pais: '',
    fundacion: 0
  };

  constructor(
    private vehiculoService: VehiculoService,
    private marcaService: MarcaService
  ) {}

  ngOnInit() {
    this.cargarVehiculos();
    this.cargarMarcas();
  }

  cargarVehiculos() {
    this.vehiculoService.getVehiculos().subscribe(vehiculos => {
      this.vehiculos = vehiculos;
    });
  }

  cargarMarcas() {
    this.marcaService.getMarcas().subscribe(marcas => {
      this.marcas = marcas;
    });
  }

  mostrarVista(vista: string) {
    this.vistaActual = vista;
    this.limpiarFormularios();
  }

  limpiarFormularios() {
    this.nuevoVehiculo = {
      modelo: '',
      anio: 0,
      precio: 0,
      color: '',
      marca_id: 0
    };
    this.nuevaMarca = {
      nombre: '',
      pais: '',
      fundacion: 0
    };
    this.vehiculoSeleccionado = null;
    this.marcaSeleccionada = null;
  }

  mostrarMensaje(texto: string, tipo: 'success' | 'error') {
    this.mensaje = texto;
    this.tipoMensaje = tipo;
    setTimeout(() => {
      this.mensaje = '';
      this.tipoMensaje = '';
    }, 3000);
  }

  crearVehiculo() {
    this.vehiculoService.crearVehiculo(this.nuevoVehiculo).subscribe(
      () => {
        this.cargarVehiculos();
        this.mostrarVista('principal');
        this.mostrarMensaje('Vehiculo creado exitosamente', 'success');
      },
      error => {
        const mensaje = error?.error?.mensaje || 'Error al crear el vehiculo. Verifique los datos.';
        this.mostrarMensaje(mensaje, 'error');
      }
    );
  }

  editarVehiculo(vehiculo: Vehiculo) {
    this.vehiculoSeleccionado = { ...vehiculo };
    this.nuevoVehiculo = {
      modelo: vehiculo.modelo,
      anio: vehiculo.anio,
      precio: vehiculo.precio,
      color: vehiculo.color,
      marca_id: vehiculo.marca_id
    };
    this.vistaActual = 'editar-vehiculo';
  }

  actualizarVehiculo() {
    if (this.vehiculoSeleccionado) {
      this.vehiculoService.actualizarVehiculo(this.vehiculoSeleccionado.id, this.nuevoVehiculo).subscribe(
        () => {
          this.cargarVehiculos();
          this.mostrarVista('principal');
          this.mostrarMensaje('Vehiculo actualizado exitosamente', 'success');
        },
        error => {
          const mensaje = error?.error?.mensaje || 'Error al actualizar el vehiculo. Verifique los datos.';
          this.mostrarMensaje(mensaje, 'error');
        }
      );
    }
  }

  eliminarVehiculo(id: number) {
    if (confirm('Esta seguro de eliminar este vehiculo?')) {
      this.vehiculoService.eliminarVehiculo(id).subscribe(
        () => {
          this.cargarVehiculos();
          this.mostrarMensaje('Vehiculo eliminado exitosamente', 'success');
        },
        error => {
          const mensaje = error?.error?.mensaje || 'Error al eliminar el vehiculo';
          this.mostrarMensaje(mensaje, 'error');
        }
      );
    }
  }

  verDetalleVehiculo(vehiculo: Vehiculo) {
    this.vehiculoSeleccionado = vehiculo;
    this.vistaActual = 'detalle-vehiculo';
  }

  crearMarca() {
    this.marcaService.crearMarca(this.nuevaMarca).subscribe(
      () => {
        this.cargarMarcas();
        this.mostrarVista('marcas');
        this.mostrarMensaje('Marca creada exitosamente', 'success');
      },
      error => {
        const mensaje = error?.error?.mensaje || 'Error al crear la marca. Verifique los datos.';
        this.mostrarMensaje(mensaje, 'error');
      }
    );
  }

  editarMarca(marca: Marca) {
    this.marcaSeleccionada = { ...marca };
    this.nuevaMarca = {
      nombre: marca.nombre,
      pais: marca.pais,
      fundacion: marca.fundacion
    };
    this.vistaActual = 'editar-marca';
  }

  actualizarMarca() {
    if (this.marcaSeleccionada) {
      this.marcaService.actualizarMarca(this.marcaSeleccionada.id, this.nuevaMarca).subscribe(
        () => {
          this.cargarMarcas();
          this.mostrarVista('marcas');
          this.mostrarMensaje('Marca actualizada exitosamente', 'success');
        },
        error => {
          const mensaje = error?.error?.mensaje || 'Error al actualizar la marca. Verifique los datos.';
          this.mostrarMensaje(mensaje, 'error');
        }
      );
    }
  }

  eliminarMarca(id: number) {
    if (confirm('Esta seguro de eliminar esta marca?')) {
      this.marcaService.eliminarMarca(id).subscribe(
        () => {
          this.cargarMarcas();
          this.mostrarMensaje('Marca eliminada exitosamente', 'success');
        },
        error => {
          const mensaje = error?.error?.mensaje || 'No se puede eliminar marca con vehiculos asociados';
          this.mostrarMensaje(mensaje, 'error');
        }
      );
    }
  }

  cargarReporte() {
    this.marcaService.getReporteMarcas().subscribe(reporte => {
      this.reporteMarcas = reporte;
      this.vistaActual = 'reporte';
    });
  }

  getMarcaNombre(marcaId: number): string {
    const marca = this.marcas.find(m => m.id === marcaId);
    return marca ? marca.nombre : 'Sin marca';
  }

  getMarcaCompleta(marcaId: number): Marca | undefined {
    return this.marcas.find(m => m.id === marcaId);
  }
}