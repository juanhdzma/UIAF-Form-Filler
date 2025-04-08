from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os


def fill_general_info(driver, case_id):
    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_txtROSN_NumeroReporteValor"
    )
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_txtROSN_NumeroReporteValor",
    ).send_keys(case_id)

    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_ddlClaseReporte "
    )
    select_element = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_ddlClaseReporte",
    )
    select = Select(select_element)
    select.select_by_value("I")


def load_juridica(driver):
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane2_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane2_header",
    ).click()

    driver.wait_if_loading()

    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane2_content_WUCROSN_PersonaJuridica1_fileTarjetas"
    )

    driver.wait_if_loading()

    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane2_content_WUCROSN_PersonaJuridica1_fileTarjetas",
    ).send_keys(os.path.abspath("output_files/JURIDICA.xlsx"))

    driver.wait_if_loading()

    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane2_content_WUCROSN_PersonaJuridica1_btnImportar_btnBoton",
    ).click()


def load_natural(driver):
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane3_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane3_header",
    ).click()

    driver.wait_if_loading()

    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane3_content_WECPersonaNatural_fileTarjetas"
    )

    driver.wait_if_loading()

    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane3_content_WECPersonaNatural_fileTarjetas",
    ).send_keys(os.path.abspath("output_files/NATURAL.xlsx"))

    driver.wait_if_loading()

    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane3_content_WECPersonaNatural_btnImportar_btnBoton",
    ).click()


def load_detalles(driver, data):
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane4_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_header",
    ).click()

    driver.wait_if_loading()

    driver.wait_for_element(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1"
    )

    fecha_inicio = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1",
    )
    fecha_fin = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha2",
    )

    driver.execute_script(
        "arguments[0].value = arguments[1];", fecha_inicio, data["fecha_inicio"]
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];", fecha_fin, data["fecha_fin"]
    )

    driver.wait_if_loading()

    # ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1 text inicio fecha on change
    # ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha2 text fin fecha on change

    driver.set_textarea_value(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_DescripcionOperacionSospechosa_txtTexto",
        data["texto_detalles"],
    )

    driver.wait_if_loading()

    # ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_DescripcionOperacionSospechosa_txtTexto pegar texto largo

    select_element = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOOPERACION_ID",
    )
    select = Select(select_element)
    select.select_by_visible_text(data["motivo"])

    driver.wait_if_loading()

    # ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOOPERACION_ID select tipo de operacion option sea igual

    for item in data["razones"]:
        driver.set_textarea_value(
            "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtSenalesAlerta_txtTexto",
            item[:200],
        )

        driver.wait_if_loading()

        driver.find_element(
            By.CSS_SELECTOR,
            "#ctl00_ContentPlaceHolder1_AccordionPane4_content_btnAgregarSennalesAlerta_btnBoton",
        ).click()

        driver.wait_if_loading()

    # ctl00_ContentPlaceHolder1_AccordionPane4_content_txtSenalesAlerta_txtTexto senal de alerta
    # ctl00_ContentPlaceHolder1_AccordionPane4_content_btnAgregarSennalesAlerta_btnBoton boton agregar senal de alerta

    select_element = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOMONEDA_ID",
    )
    peso_select = Select(select_element)
    peso_select.select_by_value("1")

    driver.wait_if_loading()

    # ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOMONEDA_ID moneda select value 1 o pesos

    driver.set_textarea_value(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_ValorTransaccion_txtTexto",
        data["valor"],
    )

    driver.wait_if_loading()

    # ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_ValorTransaccion_txtTexto valor transaccion
