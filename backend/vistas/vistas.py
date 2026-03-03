from flask_restful import Resource
from data.mock_data import reporte_marcas
from modelos.modelos  import db, Marca, MarcaSchema,Vehiculo,VehiculoSchema
from flask import request
from datetime import datetime

marca_schema = MarcaSchema()
vehiculo_schema= VehiculoSchema()
class VistaMarcas(Resource):
    def get(self):
        return [marca_schema.dump(marca) for marca in  Marca.query.order_by(Marca.nombre).all()]
    
    def post(self):
        nombre=request.json.get("nombre")
        pais=request.json.get("pais")
        fundacion =request.json.get("fundacion")
        if nombre == None:
            return {'error': "El nombre no puede estar vacío"},400
        if pais == None:
            return {'error': "El país no puede estar vacío"},400
        anio_actual = datetime.now().year
        
        if not isinstance(nombre, str) or not isinstance(pais, str) or not isinstance(fundacion, int):
            return {'error': "Por favor verificar la informacion ingresada"},400
        
        if fundacion == None or fundacion < 1800 or fundacion > anio_actual+1:
            return {'error': "El año de fundación no puede estar vacío y debe ser un año válido"}
        
        if Marca.query.filter_by(nombre=nombre).first():
            return {'error': "La marca ya se encuentra registrada"},400
        
        nueva_marca = Marca()
        nueva_marca.nombre = nombre
        nueva_marca.pais = pais
        nueva_marca.fundacion = fundacion
        db.session.add(nueva_marca)
        db.session.commit()
        return marca_schema.dump(nueva_marca)

class VistaMarca(Resource):
    def get(self, id_marca):
        return None
    
    def put(self, id_marca):
        return None
    def delete(self,id_marca):
        try:
            marca = db.session.get(Marca,id_marca)
            if marca.vehiculos != []:
                return {'error':"No se puede eliminar la marca porque tiene vehículos asociados"},400      
            db.session.delete(marca)
            db.session.commit()
            return {"mensaje":"Marca eliminada exitosamente"},200
                
        except Exception as e:
            return {'error':"Error al eliminar la marca"},400
class VistaVehiculos(Resource):
    def get(self):
        return [vehiculo_schema.dump(vehiculo) for vehiculo in Vehiculo.query.order_by(Vehiculo.modelo).all()]
    def post(self):
        return None
    def delete(self):
        return None
class VistaVehiculo(Resource):
    def get(self, id_vehiculo):
        return None
        
    
    def put(self, id_vehiculo):
        return None
    def delete(self, id_vehiculo):
        
        return None
        
class VistaReporteMarcas(Resource):
    def get(self):
        return None