from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os


def fill_general_information(driver, report_id, hasClass=False) -> None:
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane1_content_txtROSN_NumeroReporteValor")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane1_content_txtROSN_NumeroReporteValor",
    ).send_keys(report_id)

    if hasClass:
        driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane1_content_ddlClaseReporte")
        report_type_select = driver.find_element(
            By.CSS_SELECTOR,
            "#ctl00_ContentPlaceHolder1_AccordionPane1_content_ddlClaseReporte",
        )
        Select(report_type_select).select_by_value("I")


def upload_legal_entity_file(driver) -> None:
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane2_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane2_header",
    ).click()

    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane2_content_WUCROSN_PersonaJuridica1_fileTarjetas")
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


def upload_natural_person_file(driver) -> None:
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane3_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane3_header",
    ).click()

    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane3_content_WECPersonaNatural_fileTarjetas")
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


def fill_ros_details(driver, data) -> None:
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane4_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_header",
    ).click()

    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1")

    start_date_field = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1",
    )
    end_date_field = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha2",
    )

    driver.execute_script("arguments[0].value = arguments[1];", start_date_field, data["start_date"])
    driver.execute_script("arguments[0].value = arguments[1];", end_date_field, data["end_date"])

    driver.wait_if_loading()
    driver.set_textarea_value(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_DescripcionOperacionSospechosa_txtTexto",
        data["description"],
    )

    driver.wait_if_loading()
    operation_type_select = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOOPERACION_ID",
    )
    Select(operation_type_select).select_by_visible_text(data["operation_reason"])

    driver.wait_if_loading()
    for reason in data["alert_reasons"]:
        driver.set_textarea_value(
            "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtSenalesAlerta_txtTexto",
            reason[:200],
        )
        driver.wait_if_loading()
        driver.find_element(
            By.CSS_SELECTOR,
            "#ctl00_ContentPlaceHolder1_AccordionPane4_content_btnAgregarSennalesAlerta_btnBoton",
        ).click()
        driver.wait_if_loading()

    currency_select = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOMONEDA_ID",
    )
    Select(currency_select).select_by_value("1")

    driver.wait_if_loading()
    driver.set_textarea_value(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_ValorTransaccion_txtTexto",
        data["transaction_amount"],
    )
    driver.wait_if_loading()


def fill_try_details(driver, data) -> None:
    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane4_header")
    driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_header",
    ).click()

    driver.wait_if_loading()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1")

    start_date_field = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1",
    )
    end_date_field = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha2",
    )

    driver.execute_script("arguments[0].value = arguments[1];", start_date_field, data["start_date"])
    driver.execute_script("arguments[0].value = arguments[1];", end_date_field, data["end_date"])

    driver.wait_if_loading()
    driver.set_textarea_value(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSNI_Descripcion_txtTexto",
        data["description"],
    )

    driver.wait_if_loading()
    operation_type_select = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOOPERACION_ID",
    )
    Select(operation_type_select).select_by_visible_text(data["operation_reason"])

    driver.wait_if_loading()

    currency_select = driver.find_element(
        By.CSS_SELECTOR,
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOMONEDA_ID",
    )
    Select(currency_select).select_by_value("1")

    driver.wait_if_loading()
    driver.set_textarea_value(
        "#ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSNI_ValorTransaccion_txtTexto",
        data["transaction_amount"],
    )
    driver.wait_if_loading()


# ctl00_ContentPlaceHolder1_AccordionPane3_content_txtNoticiaprensa_txtTexto URL
# ctl00_ContentPlaceHolder1_AccordionPane3_content_txtFechaNoticia_txtFecha DATE
# ctl00_ContentPlaceHolder1_AccordionPane3_content_btnBotonAgregarNoticia_btnBoton PRESS

# ctl00_ContentPlaceHolder1_AccordionPane3_content_txtROSN_Descripcion_txtTexto CONTENT
