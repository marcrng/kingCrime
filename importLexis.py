import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

s = Service("C:\Program Files (x86)\msedgedriver.exe")
driver = webdriver.Edge(service=s)

# Launch the browser on below page

driver.get("https://www.communitycrimemap.com/")

# Bypass terms popup
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="mat-dialog-0"]/app-welcome-disclaimer/div/div/div[5]/button'))
    )
    element.click()
finally:
    time.sleep(4)
    search = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
    search.send_keys('federal way')
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[3]/app-navbar-actions/div/div[2]').click()

# Click Assault-Aggravated, Burglary from Motor vehicle, homicide/manslaughter, assault-simple,
# Burglary-residential, Kidnapping/human trafficking, Roberry-individual, theft,
# Vandalism, attempted homicide, sexual assault, theft-other, weapons violation,
# arson, drugs/narcotics violation, harassment/intimidation, motor vehicle theft,
# sexual offense
selFilter = driver.find_element(By.XPATH,
                                '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/button')
selFilter.click()

# Select filter categories
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-12"]/label/span[2]').click()  # Burglary from motor vehicle
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-9"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-25"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-25"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-37"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-10"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-34"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-38"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-19"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-23"]/label/span[2]').click()
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-31"]/label/span[2]').click()

# One month time period


# Apply Selection
# driver.find_element(By.XPATH,
#                     '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[3]/button[2]').click()

# Scrape data
# time.sleep(2)
# pageSource = driver.page_source
# soup = BeautifulSoup(pageSource, 'lxml')
# table = soup.find_all('table')
# df = pd.read_html(str(table))[0]

# Cycle through pages
nextPage = driver.find_element(By.XPATH,
                               '//*[@id="table-container"]/div/app-paginator/div/div[2]/mat-paginator/div/div/div[2]/button[3]/span[1]/svg')
nextPage.click()

# print(nextPageEC)

# Cycle through the months

# End the web session
# driver.close()
