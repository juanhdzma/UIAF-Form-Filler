from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


BASE_URL = "https://reportes.uiaf.gov.co/ReportesFSMCif64/Modules/Home/html/home.aspx"
ENTIDADES = {
    "Comisionista": "SCOTIA SECURITIES (COLOMBIA) SA SOCIEDAD COMISIONISTA DE BOLSA",
    "Fiduciaria": "FIDUCIARIA COLPATRIA S.A. - FIDUCOLPATRIA",
    "Banco": "SCOTIABANK COLPATRIA",
}


def redirect_entity(driver, kind):
    driver.get(BASE_URL)
    driver.wait_for_element("#ctl00_templateEntity")

    select_element = driver.find_element(By.CSS_SELECTOR, "#ctl00_CambiarEntidad1_ddlEntities")
    Select(select_element).select_by_visible_text(ENTIDADES[kind])

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    driver.get(BASE_URL)
    driver.wait_for_element("#ctl00_templateEntity")
