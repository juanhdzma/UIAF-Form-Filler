from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from app.util.convert import string_to_matrix


def perform_login(driver, env):
    open_login_page(driver, env.URL)
    enter_credentials(driver, env.USERNAME, env.PASSWORD)
    solve_matrix_challenge(driver, env.MATRIX)
    select_entity(driver, "SCOTIABANK COLPATRIA")


def open_login_page(driver, url):
    driver.get(url)


def enter_credentials(driver, username, password):
    driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_usuario").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".clsButton").send_keys(Keys.ENTER)
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_labelIdentityFSM")


def solve_matrix_challenge(driver, matrix):
    requested_matrix = driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_labelIdentityFSM").text
    requested_matrix_number, item_matrix = string_to_matrix(requested_matrix)

    for index, item in enumerate(item_matrix):
        field_selector = f"#ctl00_ContentPlaceHolder1_tb{item}"
        value = matrix[requested_matrix_number[index][1]][requested_matrix_number[index][0]]
        driver.find_element(By.CSS_SELECTOR, field_selector).send_keys(value)

    driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Button1").send_keys(Keys.ENTER)
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_cbxEntidad")


def select_entity(driver, entity):
    select_element = driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_cbxEntidad")
    Select(select_element).select_by_visible_text(entity)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", select_element)
    driver.wait_for_element("#ctl00_templateEntity")
