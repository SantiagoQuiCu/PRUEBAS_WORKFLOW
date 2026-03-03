import unittest
from unittest.mock import patch
from modelos.modelos import db, Marca
from app import app

VISTA_MARCAS_URL = "/marcas"


class TestVistaMarcas(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        for marca in Marca.query.all():
            db.session.delete(marca)
        db.session.commit()

    def test_retorna_201_crear_marca(self):
        """Validar que al realizar un post devulve un diccionario"""
        nueva_marca = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertIsInstance(post.json,dict)

    def test_post_retorna_la_marca_nueva(self):
        "Prueba para revisar que al realizar un post devulve la marca nueva"
        nueva_marca = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.json.get('nombre'),"Mazda")
        self.assertEqual(post.json.get('pais'),"Japon")
        self.assertEqual(post.json.get('fundacion'),1920)
    
    def test_get_marcas_retorna_la_marca_guarda(self):
        "Prueba que se guarda la marca nueva y se puede ver la informacion en el listado de marcas"
        nueva_marca = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        resp=self.client.get(VISTA_MARCAS_URL)
        self.assertEqual(resp.json[0].get('nombre'),"Mazda")
        self.assertEqual(resp.json[0].get('pais'),"Japon")
        self.assertEqual(resp.json[0].get('fundacion'),1920)

    def test_retorna_400_si_falta_algun_dato(self):
        """Se prueba que al faltar algun campo en la creacion de marca retorna un error 400"""
        nueva_marca= {"nombre":"Mazda","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.status_code,400)
        nueva_marca= {"pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.status_code,400)
        nueva_marca= {"nombre":"Mazda","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.status_code,400)
    
    def test_retorna_mensaje_error_si_tipos_datos_diferentes(self):
        """Se prueba que al ingresar un tipo diferente de dato sale un mensaje de error"""
        nueva_marca= {"nombre":1230,"pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.json.get('error'),"Por favor verificar la informacion ingresada")
        nueva_marca= {"nombre":"Mazda","pais":12345,"fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.json.get('error'),"Por favor verificar la informacion ingresada")
        nueva_marca= {"nombre":"Mazda","pais":"Japon","fundacion":"mil"}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca)
        self.assertEqual(post.json.get('error'),"Por favor verificar la informacion ingresada")
    
    def test_retorna_mensaje_error_si_marca_repetida(self):
        """Se prueba que al ingresan una marca ya existente salga un mensaje de error"""
        nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
        nueva_marca_2 = {"nombre":"Mazda","pais":"Japon","fundacion":1945}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
        self.assertEqual(post.json.get('error'),"La marca ya se encuentra registrada")

    def test_retorna_lista_vacia_si_no_hay_marcas(self):
        """Se prueba que al no haber marcas en la base de datos el get retorne una lista vacia"""
        resp=self.client.get(VISTA_MARCAS_URL)
        self.assertEqual(resp.json,[])
        
    def test_retorna_listado_marcas_creadas_con_la_informacion_brindada(self):
        """Se prueba que al crear varias marcas el get retorne un listado con las marcas creadas con la informacion brindada"""
        nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
        nueva_marca_2 = {"nombre":"Toyota","pais":"Japon","fundacion":1930}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_2)
        resp=self.client.get(VISTA_MARCAS_URL)
        self.assertEqual(len(resp.json),2)
        self.assertEqual(resp.json[0].get('nombre'),"Mazda")
        self.assertEqual(resp.json[0].get('pais'),"Japon")
        self.assertEqual(resp.json[0].get('fundacion'),1920)
        self.assertEqual(resp.json[1].get('nombre'),"Toyota")
        self.assertEqual(resp.json[1].get('pais'),"Japon")
        self.assertEqual(resp.json[1].get('fundacion'),1930) 
        
    def test_verifica_que_el_listado_de_marcas_se_retorne_en_orden_alfabetico(self):
        """Se prueba que el listado de marcas se retorne en orden alfabetico"""
        nueva_marca_1 = {"nombre":"Mazda","pais":"Japon","fundacion":1920}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_1)
        nueva_marca_2 = {"nombre":"Toyota","pais":"Japon","fundacion":1930}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_2)
        nueva_marca_3 = {"nombre":"Audi","pais":"Alemania","fundacion":1910}
        post = self.client.post(VISTA_MARCAS_URL,json=nueva_marca_3)
        resp=self.client.get(VISTA_MARCAS_URL)
        self.assertEqual(len(resp.json),3)
        self.assertEqual(resp.json[0].get('nombre'),"Audi")
        self.assertEqual(resp.json[1].get('nombre'),"Mazda")
        self.assertEqual(resp.json[2].get('nombre'),"Toyota")