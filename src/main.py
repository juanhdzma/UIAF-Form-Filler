from app.initialize.config import env_loader
from app.initialize.service_manager import SeleniumDriver
from app.controllers.login_manager import perform_login
from app.controllers.redirect_ros_manager import redirect_new
from app.controllers.redirect_type_manager import redirect_entity
from app.controllers.fill_manager import (
    fill_general_information,
    upload_legal_entity_file,
    upload_natural_person_file,
    fill_ros_details,
    fill_try_details,
)
from app.util.read_data import read_directory_data
from app.util.read_file import load_excel_file
from app.util.read_user import read_user_data
from app.util.relations_manager import process_relation_df
from time import sleep


environment = env_loader()
driver = SeleniumDriver(environment.OS)

cached_excel = load_excel_file()
report_directory = read_directory_data(cached_excel)

perform_login(driver, environment)

sleep(1231232213)

for branch, kind_dict in report_directory.items():
    redirect_entity(driver, branch)

    for report_type, df in kind_dict.items():
        for _, row in df.iterrows():
            redirect_new(driver, report_type)
            data = read_user_data(cached_excel, row["CLIENTE"])

            if report_type == "ROS":
                fill_general_information(driver, row["Consecutivo UIAF"], True)
            else:
                fill_general_information(driver, row["Consecutivo UIAF"])

            process_relation_df(data["related"], "NATURAL")
            process_relation_df(data["related"], "JURIDICA")

            upload_legal_entity_file(driver)
            upload_natural_person_file(driver)

            if report_type == "ROS":
                fill_ros_details(driver, data)
            elif report_type == "Reputacional":
                fill_ros_details(driver, data)
            elif report_type == "Intentadas":
                fill_try_details(driver, data)
            sleep(231232)
