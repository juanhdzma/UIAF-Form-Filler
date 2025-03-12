from app.util.error import CustomException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SeleniumDriver(webdriver.Chrome):
    def __init__(self, OS):
        """Inicializa el controlador de Selenium."""
        try:
            if OS == "MAC":
                service = Service("src/drivers/chromedriver-mac-arm64/chromedriver")
            elif OS == "WIN":
                service = Service("src/drivers/chromedriver-win64/chromedriver.exe")
            else:
                raise CustomException("OS en .env no es valido")
            super().__init__(service=service)
        except Exception:
            raise CustomException(
                "No se pudo crear el driver de selenium, verifique la carpeta drivers"
            )

    def wait_for_element(self, css_selector, timeout=60):
        """Espera hasta que un elemento específico aparezca en la página."""
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except Exception:
            raise CustomException(f"La pagina parece no haber terminado de cargar")
