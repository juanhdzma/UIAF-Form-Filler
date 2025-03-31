from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def fill_general_info(driver, case_id):
    ingresar_numero_caso(driver, case_id)
    seleccionar_tipo_reporte(driver)


def ingresar_numero_caso(driver, case_id):
    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_txtROSN_NumeroReporteValor"
    )
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_txtROSN_NumeroReporteValor",
    ).send_keys(case_id)


def seleccionar_tipo_reporte(driver):
    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_ddlClaseReporte "
    )
    select_element = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_ddlClaseReporte",
    )
    select = Select(select_element)
    select.select_by_value("I")
