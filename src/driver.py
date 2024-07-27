import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement

from src.config import CONFIG

class Driver:
  def __init__(self,headless=False):
    CHROME_PATH = CONFIG.web_driver_path
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.driver = webdriver.Chrome(options=options, service=ChromeService(CHROME_PATH))


  def get(self,url):
    self.driver.get(url)

  def find_x(self,xpath, timeout=10, parent=None) -> WebElement:
    find_cb =  lambda: self.driver.find_element(By.XPATH, xpath)
    wait_cb = lambda: WebDriverWait(self.driver, timeout).until(
      EC.presence_of_element_located((By.XPATH, xpath)) )
    if parent:
      find_cb = lambda: parent.find_element(By.XPATH, xpath)
      wait_cb = lambda: WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath)) )

    try:
      result = find_cb()
      if result:
        return result
    except:
      try:
        wait_cb()
        
      except:
        return None
    return find_cb()
  
  def find_x_multi(self,xpath, timeout=10, parent=None) -> WebElement:
    find_cb =  lambda: self.driver.find_elements(By.XPATH, xpath)
    wait_cb = lambda: WebDriverWait(self.driver, timeout).until(
      EC.presence_of_element_located((By.XPATH, xpath)))
    if parent:
      find_cb = lambda: parent.find_elements(By.XPATH, xpath)
      wait_cb = lambda: WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath)) )
      
    try:
      result = find_cb()
      if result:
        return result
    except:
      try:
        wait_cb()
      except:
        return None
    return find_cb()
  
  def get_select_options(self,elem=None,x=None):
    if elem is None:
      elem = self.find_x(x)

    options = elem.find_elements(By.TAG_NAME, 'option')
    return options

  def set_select_option(self,elem,option):
    self.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'))",elem,option)
    time.sleep(0.3)

  def remove_elem(self,elem):
    self.driver.execute_script("arguments[0].remove();", elem)

  def execute_script(self,script,*args):
    return self.driver.execute_script(script,*args)