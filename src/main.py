from app.initialize.config import EnvLoader
from app.initialize.service_manager import SeleniumDriver
from app.controllers.login_manager import perform_login
from app.controllers.redirect_manager import redirect_new_ros
from app.controllers.fill_manager import (
    fill_general_information,
    upload_legal_entity_file,
    upload_natural_person_file,
    fill_transaction_details,
)
from app.util.read_data import read_directory_data
from app.util.read_file import load_excel_file
from app.util.read_user import read_user_data
from app.util.relations_manager import process_relation_df
from time import sleep


ENTIDADES = {
    "Comisionista": "SCOTIA SECURITIES (COLOMBIA) SA SOCIEDAD COMISIONISTA DE BOLSA",
    "Fiduciaria": "FIDUCIARIA COLPATRIA S.A. - FIDUCOLPATRIA",
    "Banco": "SCOTIABANK COLPATRIA",
}


env = EnvLoader()
driver = SeleniumDriver(env.OS)

perform_login(driver, env)
redirect_new_ros(driver)

cached_file = load_excel_file()
directory = read_directory_data(cached_file)

# for filial, decisiones in directory.items():

#     driver.wait_for_element("#ctl00_CambiarEntidad1_ddlEntities")

#     select_element = driver.find_element(By.CSS_SELECTOR, "#ctl00_CambiarEntidad1_ddlEntities")
#     Select(select_element).select_by_visible_text(ENTIDADES[filial])

#     try:
#         alert = driver.switch_to.alert
#         alert.accept()
#     except:
#         pass

#     driver.get("https://reportes.uiaf.gov.co/ReportesFSMCif64/Modules/Home/html/home.aspx")

#     print(f"\nFilial: {filial}")
#     sleep(5)

#     for tipo, df in decisiones.items():
#         print(f"  {tipo}: {df.shape[0]} filas")


for filial, kind_dict in directory.items():
    for tipo, df in kind_dict.items():
        for _, row in df.iterrows():
            data = read_user_data(cached_file, row["CLIENTE"])
            fill_general_information(driver, row["Consecutivo UIAF"])
            process_relation_df(data["related"], "NATURAL")
            process_relation_df(data["related"], "JURIDICA")
            upload_legal_entity_file(driver)
            upload_natural_person_file(driver)
            fill_transaction_details(driver, data)
            sleep(231232)
