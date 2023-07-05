from datetime import datetime
import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

result = 0

while result == 0:

    driver = webdriver.Firefox()
    driver.get("https://rdv-etrangers-94.interieur.gouv.fr/eAppointmentpref94/element/jsp/specific/pref94.jsp")
    elem = driver.find_element(By.ID, 'CPId')
    elem.clear()
    elem.send_keys("94200")
    elem.send_keys(Keys.RETURN)

    delay = 3  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'selectedMotiveKeyList')))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    ## Page changed
    elem2 = driver.find_element(By.NAME, 'selectedMotiveKeyList')
    ## click button
    driver.execute_script("arguments[0].click();", elem2)

    elem3 = driver.find_element(By.ID, 'nextButtonId')
    driver.execute_script("arguments[0].click();", elem3)
    now = datetime.now()
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       "Aucun rendez-vous n'est possible pour les motifs selectionnnés ou le créneau "
                                       "horaire séléctionné.")
        ## Switching to Alert
        alert = driver.switch_to.alert
        alertMessage = alert.text
        alert.accept()
        print(now, ":", alertMessage)

    except TimeoutException:
        print(now, ":", "no alert. RDV available")
        result = 1

    ##    if alertMessage is not None:
    ##        if "Aucun rendez-vous" in alertMessage

    driver.close()

    ## Sleep 90 seconds
    time.sleep(90)
