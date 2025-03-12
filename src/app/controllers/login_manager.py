from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.util.convert import string_to_matrix
from time import sleep


def login(driver, env):
    driver.get(env.URL)

    driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_usuario"
    ).send_keys(env.USERNAME)
    driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_password"
    ).send_keys(env.PASSWORD)
    driver.find_element(By.CSS_SELECTOR, ".clsButton").send_keys(Keys.ENTER)

    sleep(1)

    requested_matrix = driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_labelIdentityFSM"
    ).text

    requested_matrix_number, item_matrix = string_to_matrix(requested_matrix)

    print(item_matrix)

    fields = ["#ctl00_ContentPlaceHolder1_tb" + item for item in item_matrix]

    for index, item in enumerate(fields):
        driver.find_element(By.CSS_SELECTOR, item).send_keys(
            env.MATRIX[requested_matrix_number[index][1]][
                requested_matrix_number[index][0]
            ]
        )
        print(
            env.MATRIX[requested_matrix_number[index][1]][
                requested_matrix_number[index][0]
            ]
        )

    driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Button1"
    ).send_keys(Keys.ENTER)

    sleep(2)
