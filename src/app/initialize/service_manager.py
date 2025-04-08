import threading
from app.util.error import CustomException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class SeleniumDriver(webdriver.Chrome):
    def __init__(self, OS):
        """Inicializa el controlador de Selenium y el monitor de loading.gif."""
        try:
            if OS == "MAC":
                service = Service("src/drivers/chromedriver-mac-arm64/chromedriver")
            elif OS == "WIN":
                service = Service("src/drivers/chromedriver-win64/chromedriver.exe")
            else:
                raise CustomException("OS en .env no es válido")
            super().__init__(service=service)

            self._lock = threading.Lock()

        except Exception:
            raise CustomException(
                "No se pudo crear el driver de Selenium, verifique la carpeta drivers"
            )

    def wait_for_element(self, css_selector, timeout=60):
        """Espera hasta que un elemento específico aparezca en la página."""
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except Exception:
            raise CustomException("La página parece no haber terminado de cargar")

    def is_loading_gif_visible_locked(self):
        """Versión protegida para uso dentro del lock."""
        try:
            img = self.find_element(By.XPATH, "//img[contains(@src, 'loading.gif')]")
            return img.is_displayed()
        except:
            return False

    def wait_if_loading(self, timeout=60):
        """Bloquea el flujo si el loading.gif está activo."""
        time.sleep(0.5)
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self._lock:
                if not self.is_loading_gif_visible_locked():
                    return  # loading ya no está visible
            time.sleep(0.1)
        raise CustomException("Timeout esperando que desaparezca el loading.gif")

    def quit(self):
        """Detiene el hilo de monitoreo y cierra el navegador."""
        self._stop_monitor = True
        super().quit()

    def set_textarea_value(self, selector, text):
        element = self.find_element(By.CSS_SELECTOR, selector)
        self.execute_script("arguments[0].value = arguments[1];", element, text)
        self.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
        self.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
