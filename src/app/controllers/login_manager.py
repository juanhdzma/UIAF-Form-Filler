from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from app.util.convert import string_to_matrix


def login(driver, env):
    """Realiza el proceso de inicio de sesión en la plataforma."""

    abrir_pagina(driver, env.URL)
    ingresar_credenciales(driver, env.USERNAME, env.PASSWORD)
    resolver_matriz(driver, env)
    seleccionar_entidad(driver, "SCOTIABANK COLPATRIA")


def abrir_pagina(driver, url):
    """Carga la página de inicio de sesión."""
    driver.get(url)


def ingresar_credenciales(driver, username, password):
    """Ingresa el usuario y la contraseña y hace login."""
    driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_usuario"
    ).send_keys(username)
    driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_password"
    ).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".clsButton").send_keys(Keys.ENTER)

    driver.wait_for_element("#ctl00_ContentPlaceHolder1_labelIdentityFSM")


def resolver_matriz(driver, env):
    """Resuelve el desafío de la matriz de seguridad."""
    requested_matrix = driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_labelIdentityFSM"
    ).text
    requested_matrix_number, item_matrix = string_to_matrix(requested_matrix)

    for index, item in enumerate(item_matrix):
        field_selector = f"#ctl00_ContentPlaceHolder1_tb{item}"
        value = env.MATRIX[requested_matrix_number[index][1]][
            requested_matrix_number[index][0]
        ]
        driver.find_element(By.CSS_SELECTOR, field_selector).send_keys(value)

    driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Button1"
    ).send_keys(Keys.ENTER)

    driver.wait_for_element("#ctl00_ContentPlaceHolder1_cbxEntidad")


def seleccionar_entidad(driver, entidad):
    """Selecciona la entidad en el dropdown y espera a que cargue la información."""
    select_element = driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_cbxEntidad"
    )
    Select(select_element).select_by_visible_text(entidad)

    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change'))", select_element
    )

    driver.wait_for_element("#ctl00_templateEntity")
