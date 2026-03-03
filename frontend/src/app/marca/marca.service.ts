import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Marca } from './marca';

@Injectable({
  providedIn: 'root'
})
export class MarcaService {
  private apiUrl = 'http://localhost:5001/marcas';

  constructor(private http: HttpClient) { }

  getMarcas(): Observable<Marca[]> {
    return this.http.get<Marca[]>(this.apiUrl);
  }

  getMarca(id: number): Observable<Marca> {
    return this.http.get<Marca>(`${this.apiUrl}/${id}`);
  }

  crearMarca(marca: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, marca);
  }

  actualizarMarca(id: number, marca: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, marca);
  }

  eliminarMarca(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }

  getReporteMarcas(): Observable<any> {
    return this.http.get<any>('http://localhost:5001/reporte-marcas');
  }
}