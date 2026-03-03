import unittest
from unittest.mock import patch
from modelos.modelos import db, Marca, Vehiculo
from app import app
import random 

VISTA_MARCA_URL = "/marcas"

class TestVistaMarcas(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        for marca in Marca.query.all():
            db.session.delete(marca)
        db.session.commit()

    def test_retorna_400_al_eliminar_marca_no_existe(self):
        """Validar que al realizar un delete devuelve un error 400 si no hay marcas existentes"""
        delete = self.client.delete(VISTA_MARCA_URL+"/1")
        self.assertEqual(delete.status_code,400)
    
    def test_retorna_200_al_eliminar_la_primera_marca(self):
        """Validar que al realizar un delete devuelve 200 si se elimina la primera marca"""
        marca = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        db.session.add(marca)
        db.session.commit()

        delete= self.client.delete(VISTA_MARCA_URL+"/1")
        self.assertEqual(delete.status_code,200)

    def test_retorna_None_al_eliminar_una_marca(self):
        """Validar que al realizar un delete de cualquier marca existente retorno None al buscar esa marca en la base de datos"""
        marca1 = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        marca2 = Marca(nombre="Toyota",pais="Japon",fundacion=1910)
        marca3 = Marca(nombre="Ford",pais="EEUU",fundacion=1900)
        db.session.add(marca1)
        db.session.add(marca2)
        db.session.add(marca3)
        db.session.commit()
        number=random.randint(1,3)
        delete= self.client.delete(VISTA_MARCA_URL+f"/{number}")
        self.assertEqual(db.session.get(Marca,str(number)),None)
    
    def test_retorna_mensaje_al_eliminar_marca_correctamente(self):
        """Validar que al realizar un delete de cualquier marca existente retorna un mensaje Marca eliminada exitosamente"""
        marca1 = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        marca2 = Marca(nombre="Toyota",pais="Japon",fundacion=1910)
        marca3 = Marca(nombre="Ford",pais="EEUU",fundacion=1900)
        db.session.add(marca1)
        db.session.add(marca2)
        db.session.add(marca3)
        db.session.commit()
        number=random.randint(1,3)
        delete= self.client.delete(VISTA_MARCA_URL+f"/{number}")
        self.assertEqual(delete.json.get("mensaje"),"Marca eliminada exitosamente")
    
    def test_retorna_mensaje_de_error(self):
        """Validar que al no poder realizar un delete de cualquier marca existente retorna un mensaje Error al eliminar la marca"""
        marca1 = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        marca2 = Marca(nombre="Toyota",pais="Japon",fundacion=1910)
        db.session.add(marca1)
        db.session.add(marca2)
        db.session.commit()
        delete= self.client.delete(VISTA_MARCA_URL+"/3")
        self.assertEqual(delete.json.get("error"),"Error al eliminar la marca")
    
    def test_retorna_error_al_borrar_marca_con_vehiculo(self):
        """Validar que si la marca tiene un vehiculo asociado al realizar un delete no se realiza la operacion """
        marca = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        vehiculo = Vehiculo(modelo="CX",anio=2025,precio=50000,color="rojo")
        marca.vehiculos.append(vehiculo)
        db.session.add(marca)
        db.session.commit()
        delete= self.client.delete(VISTA_MARCA_URL+"/1")
        self.assertIsInstance(db.session.get(Marca,1),Marca)

    def test_retorna_error_400_al_borrar_marca_con_vehiculo(self):
        """Validar que si la marca tiene un vehiculo asociado al realizar un delete retorna un error 400 """
        marca = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        vehiculo = Vehiculo(modelo="CX",anio=2025,precio=50000,color="rojo")
        marca.vehiculos.append(vehiculo)
        db.session.add(marca)
        db.session.commit()
        delete= self.client.delete(VISTA_MARCA_URL+"/1")
        self.assertEqual(delete.status_code, 400)
    
    def test_retorna_mensaje_de_error_al_borrar_marca_con_vehiculo(self):
        """Validar que si la marca tiene un vehiculo asociado al realizar un delete retorna un mensaje No se puede eliminar la marca porque tiene vehículos asociados """
        marca = Marca(nombre="Mazda",pais="Japon",fundacion=1920)
        vehiculo = Vehiculo(modelo="CX",anio=2025,precio=50000,color="rojo")
        marca.vehiculos.append(vehiculo)
        db.session.add(marca)
        db.session.commit()
        delete= self.client.delete(VISTA_MARCA_URL+"/1")
        self.assertEqual(delete.json.get("error"), "No se puede eliminar la marca porque tiene vehículos asociados")


    