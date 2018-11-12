import os

import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class PruebasSistema(unittest.TestCase):
    driver = None
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path = 'C:\\Users\\Juan\\Desktop\\geckodriver')

    def tearDown(self):
        self.driver.close()

    def test_sistemaUno(self):
        self.driver.maximize_window()
        self.driver.get('http://127.0.0.1:5000/i')
        self.driver.get('http://127.0.0.1:5000/')
        
        eleUsuario = self.driver.find_element_by_id("email")
        eleUsuario.clear()
        eleUsuario.send_keys("rodrigo@ucr.ac.cr")
        
        eleCont = self.driver.find_element_by_id("passwd")
        eleCont.clear()
        eleCont.send_keys("pwd-de-rodrigo")
        
        print(self.driver.current_url)
        
        btnSend = self.driver.find_element_by_id("submit")
        btnSend.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == '.')
        except TimeoutException:
            self.fail("Loading time expired")
         
        eleCargar = self.driver.find_element_by_id("cargar")
        eleCargar.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == '.')
        except TimeoutException:
            self.fail("Loading time expired")
            
        
        eleCargador = self.driver.find_element_by_id("archivo")
        self.driver.execute_script("arguments[0].style.display = 'block';", eleCargador)
        eleCargador = self.driver.find_element_by_id("archivo")
        eleCargador.send_keys('c:\\users\\juan\\desktop\\4.png')
        btnSend = self.driver.find_element_by_id("enviar")
        btnSend.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == 'cargar')
        except TimeoutException:
            self.fail("Loading time expired")
            
    def test_sistemaDos(self):
        self.driver.maximize_window()
        self.driver.get('http://127.0.0.1:5000/i')
        self.driver.get('http://127.0.0.1:5000/')
        
        eleUsuario = self.driver.find_element_by_id("email")
        eleUsuario.clear()
        eleUsuario.send_keys("rodrigo@ucr.ac.cr")
        
        eleCont = self.driver.find_element_by_id("passwd")
        eleCont.clear()
        eleCont.send_keys("pwd-de-rodrigo")
        
        print(self.driver.current_url)
        
        btnSend = self.driver.find_element_by_id("submit")
        btnSend.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == '.')
        except TimeoutException:
            self.fail("Loading time expired")
         
        eleCargar = self.driver.find_element_by_id("cargar")
        eleCargar.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == '.')
        except TimeoutException:
            self.fail("Loading time expired")
            
        
        eleCargador = self.driver.find_element_by_id("archivo")
        self.driver.execute_script("arguments[0].style.display = 'block';", eleCargador)
        eleCargador = self.driver.find_element_by_id("archivo")
        eleCargador.send_keys('c:\\users\\juan\\desktop\\4.png')
        btnSend = self.driver.find_element_by_id("enviar")
        btnSend.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == 'cargar')
        except TimeoutException:
            self.fail("Loading time expired")
            
        self.driver.get('http://127.0.0.1:5000/')
        
        eleSegmentar = self.driver.find_element_by_id("segmentar")
        eleSegmentar.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == '.')
        except TimeoutException:
            self.fail("Loading time expired")
           
        eleSegmentar = self.driver.find_element_by_id("enviar")
        eleSegmentar.click()
        
        wait = WebDriverWait(self.driver, 5)
        
        try:
            page_loaded = wait.until_not(lambda driver: self.driver.current_url == 'segmentar2')
        except TimeoutException:
            self.fail("Loading time expired")
            
        

if __name__ == "__main__":
    unittest.main()