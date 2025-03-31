from app.initialize.config import EnvLoader
from app.initialize.service_manager import SeleniumDriver
from app.controllers.login_manager import login
from app.controllers.redirect_manager import redirect
from app.controllers.ros_fill_manager import fill_general_info
from app.util.read_directory import read_directory_data
from app.util.read_file import read_excel_file
from app.util.read_user import read_user_data
import time

env = EnvLoader()

driver = SeleniumDriver(env.OS)

login(driver, env)
redirect(driver)
fill_general_info(driver, "123")


time.sleep(5000)


# cached_file = read_excel_file()
# data = read_directory_data(cached_file)
# read_user_data(cached_file, "ESTHER MILENA DE LEON BERRIO")
