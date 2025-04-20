from selenium.webdriver.common.by import By

URL = "https://reportes.uiaf.gov.co/ReportesFSMCif64/Modules/Reportes/html/WFRROSNConsulta.aspx"


def redirect_new_ros(driver) -> None:
    abrir_pagina(driver, URL)
    presionar_boton_crear(driver)
    presionar_boton_confirmacion_crear(driver)


def abrir_pagina(driver, url) -> None:
    driver.get(url)
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_btnNuevo")


def presionar_boton_crear(driver) -> None:
    driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_btnNuevo").click()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_rbtROS_Positivo")


def presionar_boton_confirmacion_crear(driver) -> None:
    radio_button = driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_rbtROS_Positivo")
    driver.execute_script("arguments[0].click();", radio_button)
