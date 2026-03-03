import unittest
from unittest.mock import patch
from modelos.modelos import db, Marca, Vehiculo
from app import app
from datetime import datetime

VISTA_VEHICULOS_URL = "/vehiculos"
VISTA_MARCAS_URL = "/marcas"

class TestVistaVehiculos(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        for vehiculo in Vehiculo.query.all():
          db.session.delete(vehiculo)
        for marca in Marca.query.all():
          db.session.delete(marca)
        db.session.commit()

    def test_get_vehiculos_retorna_lista(self):
        """Validar que al realizar un get devuelve una lista"""
        resp = self.client.get(VISTA_VEHICULOS_URL)
        self.assertIsInstance(resp.json,list)
    
    def test_get_vehiculos_retorna_lista_vacia(self):
      """Validar que al realizar un get devuelve una lista vacía si no hay vehiculos registrados"""
      resp = self.client.get(VISTA_VEHICULOS_URL)
      self.assertEqual(resp.json,[])
    
    def test_retorna_listado_vehiculos(self):
      """Validar que al realizar un get devuelve una lista con los vehiculos registrados"""
      nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
      post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
      marca=Marca.query.get(str(post.json.get("id")))
      vehiculo = Vehiculo( modelo="Corolla", anio=2020, precio=20000, color="Blanco")
      marca.vehiculos.append(vehiculo)
      db.session.add(vehiculo)
      db.session.commit()
      resp = self.client.get(VISTA_VEHICULOS_URL)
      self.assertEqual(len(resp.json),1)
      self.assertEqual(resp.json[0]["modelo"],"Corolla")
      self.assertEqual(resp.json[0]["anio"],2020)
      self.assertEqual(resp.json[0]["precio"],20000)
      self.assertEqual(resp.json[0]["color"],"Blanco")
      self.assertEqual(resp.json[0]["marca_id"],1)
      
    def test_verificar_orden_alfabetico_listado_vehiculos(self):
      """Validar que al realizar un get devuelve una lista con los vehiculos registrados ordenados alfabeticamente por modelo"""
      nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
      post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
      marca=Marca.query.get(str(post.json.get("id")))
      vehiculo_1 = Vehiculo( modelo="Corolla", anio=2020, precio=20000, color="Blanco")
      vehiculo_2 = Vehiculo( modelo="323", anio=2021, precio=22000, color="Negro")
      marca.vehiculos.append(vehiculo_1)
      marca.vehiculos.append(vehiculo_2)
      db.session.add(vehiculo_1)
      db.session.add(vehiculo_2)
      db.session.commit()
      resp = self.client.get(VISTA_VEHICULOS_URL)
      self.assertEqual(len(resp.json),2)
      self.assertEqual(resp.json[0]["modelo"],"323")
      self.assertEqual(resp.json[1]["modelo"],"Corolla")
      
    def test_validar_todos_los_vehiculos_existen_en_listado(self):
      """Validar que al realizar un get devuelve una lista con todos los vehiculos registrados"""
      nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
      post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
      marca=Marca.query.get(str(post.json.get("id")))
      vehiculo_1 = Vehiculo( modelo="Corolla", anio=2020, precio=20000, color="Blanco")
      vehiculo_2 = Vehiculo( modelo="323", anio=2021, precio=22000, color="Negro")
      marca.vehiculos.append(vehiculo_1)
      marca.vehiculos.append(vehiculo_2)
      db.session.add(vehiculo_1)
      db.session.add(vehiculo_2)
      db.session.commit()
      resp = self.client.get(VISTA_VEHICULOS_URL)
      self.assertEqual(len(resp.json),2)
      modelos_en_listado = [vehiculo["modelo"] for vehiculo in resp.json]
      self.assertIn("Corolla",modelos_en_listado)
      self.assertIn("323",modelos_en_listado)
      
    def test_validar_formato_retornado_datos_vehiculos(self):
      """Validar que al realizar un get devuelve una lista con los vehiculos registrados con el formato correcto"""
      nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
      post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
      marca=Marca.query.get(str(post.json.get("id")))
      vehiculo_1 = Vehiculo( modelo="Corolla", anio=2020, precio=20000, color="Blanco")
      marca.vehiculos.append(vehiculo_1)
      db.session.add(vehiculo_1)
      db.session.commit()
      resp = self.client.get(VISTA_VEHICULOS_URL)
      self.assertEqual(len(resp.json),1)
      self.assertIsInstance(resp.json[0]["id"],int)
      self.assertIsInstance(resp.json[0]["modelo"],str)
      self.assertIsInstance(resp.json[0]["anio"],int)
      self.assertGreater(resp.json[0]["anio"],1800)
      anio_actual = datetime.now().year
      self.assertLessEqual(resp.json[0]["anio"],anio_actual+1)
      self.assertIsInstance(resp.json[0]["precio"],int)
      self.assertIsInstance(resp.json[0]["color"],str)
      self.assertIsInstance(resp.json[0]["marca_id"],int)