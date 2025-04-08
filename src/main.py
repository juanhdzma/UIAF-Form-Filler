from app.initialize.config import EnvLoader
from app.initialize.service_manager import SeleniumDriver
from app.controllers.login_manager import login
from app.controllers.redirect_manager import redirect
from app.controllers.fill_manager import (
    fill_general_info,
    load_juridica,
    load_natural,
    load_detalles,
)
from app.util.read_directory import read_directory_data
from app.util.read_file import read_excel_file
from app.util.read_user import read_user_data
from app.util.relations_manager import process_relation_df
from time import sleep


env = EnvLoader()

driver = SeleniumDriver(env.OS)

login(driver, env)
redirect(driver)

cached_file = read_excel_file()
data = read_user_data(cached_file, "MOTI MORDEHAY YOSEF LEVIN LEVIN")

fill_general_info(driver, data["case_id"])

process_relation_df(data["relacionados"], "NATURAL")
process_relation_df(data["relacionados"], "JURIDICA")

load_juridica(driver)
load_natural(driver)
load_detalles(driver, data)

sleep(231232)


# JURIDICAS
# ctl00_ContentPlaceHolder1_AccordionPane2_header click
# ctl00_ContentPlaceHolder1_AccordionPane2_content_WUCROSN_PersonaJuridica1_fileTarjetas juridica choose file
# ctl00_ContentPlaceHolder1_AccordionPane2_content_WUCROSN_PersonaJuridica1_btnImportar_btnBoton cargar click

# NATURAL
# ctl00_ContentPlaceHolder1_AccordionPane3_header click
# ctl00_ContentPlaceHolder1_AccordionPane3_content_WECPersonaNatural_fileTarjetas natural choose file
# ctl00_ContentPlaceHolder1_AccordionPane3_content_WECPersonaNatural_btnImportar_btnBoton cargar click

# DETALLES
# ctl00_ContentPlaceHolder1_AccordionPane4_header click
# ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha1 text inicio fecha on change
# ctl00_ContentPlaceHolder1_AccordionPane4_content_txtPeriodo_txtFecha2 text fin fecha on change

# ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_DescripcionOperacionSospechosa_txtTexto pegar texto largo
# ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOOPERACION_ID select tipo de operacion option sea igual

# ctl00_ContentPlaceHolder1_AccordionPane4_content_txtSenalesAlerta_txtTexto senal de alerta
# ctl00_ContentPlaceHolder1_AccordionPane4_content_btnAgregarSennalesAlerta_btnBoton boton agregar senal de alerta

# ctl00_ContentPlaceHolder1_AccordionPane4_content_ddlTIPOMONEDA_ID moneda select value 1 o pesos
# ctl00_ContentPlaceHolder1_AccordionPane4_content_txtROSN_ValorTransaccion_txtTexto valor transaccion
