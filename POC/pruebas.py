import unittest
import os
import io
from server import app
from server import cargar_modelos
 
class TestUM(unittest.TestCase):
    vgg_model = None
    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        cargar_modelos()
    def tearDown(self):
        pass
    
    #testing de los codigos de estado
    
    def test_index_status_code(self):
        """Funcion para probar la respuesta al url: /index
        """
        result = self.app.get('/') 
        self.assertEqual(result.status_code, 200)
    def test_crear_status_code(self):
        """Funcion para probar la respuesta al url: /crear
        """
        result = self.app.get('/crear') 
        self.assertEqual(result.status_code, 200)
    def test_generar_status_code(self):
        """Funcion para probar la respuesta al url: /generar
        """
        result = self.app.get('/generar') 
        self.assertEqual(result.status_code, 200)
    def test_predecir_status_code(self):
        """Funcion para probar la respuesta al url: /predecir
        """
        result = self.app.get('/predecir') 
        self.assertEqual(result.status_code, 200)
    def test_cargar_status_code(self):
        """Funcion para probar la respuesta al url: /cargar
        """
        result = self.app.get('/cargar') 
        self.assertEqual(result.status_code, 200)
    
    def test_predecir_modelo_response(self):
        """Funcion para probar las funciones de prediccion
        Simula una peticion POST en la que le envia la imagen perro.jpg
        """
        data={}
        data['file'] = open('uploads\\perro.jpg', 'rb')
        #result = self.app.get('/cargar') 
        response = self.app.post(
            '/predictor', data=data, follow_redirects=True,
            content_type='multipart/form-data'
            )
        self.assertIn(b'wall_clock', response.data)
    def test_crear_csv(self):
        """Funcion para probar la funcion de generacion de archivos .csv
        Simula una peticion GET
        """
        data={}
        data['file'] = open('uploads\\perro.jpg', 'rb')
        result = self.app.get('/crear') 
        data2=result.data
        data2=b',first_name,last_name,age,preTestScore,postTestScore\r\n0,Jason,Miller,42,4,25\r\n1,Molly,Jacobson,52,24,94\r\n2,Tina,Ali,36,31,57\r\n3,Jake,Milner,24,2,62\r\n4,Amy,Cooze,73,3,70\r\n'
        self.assertIn(data2, result.data)
    
if __name__ == '__main__':
    unittest.main()