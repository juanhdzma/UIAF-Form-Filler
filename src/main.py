from app.initialize.config import EnvLoader
from app.initialize.service_manager import SeleniumDriver
from app.controllers.login_manager import login

env = EnvLoader()

driver = SeleniumDriver(env.OS)

login(driver, env)
