from selenium.webdriver.common.by import By

ROS_PAGE = "https://reportes.uiaf.gov.co/ReportesFSMCif64/Modules/Reportes/html/WFRROSNConsulta.aspx"
TRY_PAGE = "https://reportes.uiaf.gov.co/ReportesFSMCif64/Modules/Reportes/html/WFRROSNConsultaIntentadas.aspx"
REPUTATIONAL_PAGE = "https://reportes.uiaf.gov.co/ReportesFSMCif64/Modules/Reportes/html/WFRROSNConsultaNoticiasPrensa.aspx"


def redirect_new(driver, kind):
    pages = {"ROS": ROS_PAGE, "Intentadas": TRY_PAGE, "Reputacional": REPUTATIONAL_PAGE}
    if kind in pages:
        if kind == "ROS":
            redirect_new_ros(driver)
        else:
            redirect_new_generic(driver, pages[kind])


def redirect_new_ros(driver) -> None:
    open_page(driver, ROS_PAGE)
    click_create_button(driver)
    click_confirmation_button(driver)


def redirect_new_generic(driver, URL) -> None:
    open_page(driver, URL)
    click_create_button(driver)


def open_page(driver, url) -> None:
    driver.get(url)
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_btnNuevo")


def click_create_button(driver) -> None:
    driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_btnNuevo").click()
    driver.wait_for_element("#ctl00_ContentPlaceHolder1_rbtROS_Positivo")


def click_confirmation_button(driver) -> None:
    radio_button = driver.find_element(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_rbtROS_Positivo")
    driver.execute_script("arguments[0].click();", radio_button)
