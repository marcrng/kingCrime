import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
from dateutil import rrule
import time
from sqlalchemy import create_engine
import config
from playsound import playsound

s = Service("C:\Program Files (x86)\msedgedriver.exe")
driver = webdriver.Edge(service=s)

engine = create_engine(
    "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
        host=config.sql_host,
        db='kc_crime',
        user=config.sql_user,
        pw=config.sql_pass)
)

# Launch the browser on below page

driver.get("https://www.communitycrimemap.com/")

# Bypass terms popup
try:
    element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="mat-dialog-0"]/app-welcome-disclaimer/div/div/div[5]/button'
            )
        )
    )
    element.click()
finally:
    time.sleep(4)
    search = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
    search.send_keys('federal way')
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    buttonTables = driver.find_element(
        By.XPATH,
        '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[3]/app-navbar-actions/div/div[2]'
    )
    buttonTables.click()

# Call buttons
# Start Date field
field_dateStart = driver.find_element(
    By.XPATH,
    '//*[@id="mat-input-1"]'
)

# End Date field
field_dateEnd = driver.find_element(
    By.XPATH,
    '//*[@id="mat-input-2"]'
)

# Click Assault-Aggravated, Burglary from Motor vehicle, homicide/manslaughter, assault-simple,
# Burglary-residential, Kidnapping/human trafficking, Roberry-individual, theft,
# Vandalism, attempted homicide, sexual assault, theft-other, weapons violation,
# arson, drugs/narcotics violation, harassment/intimidation, motor vehicle theft,
# sexual offense
buttonFilter = driver.find_element(
    By.XPATH,
    '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/button'
)
buttonFilter.click()

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
driver.find_element(By.XPATH, '//*[@id="mat-checkbox-36"]/label/span[2]').click()

# One month time period

# Apply Selection
buttonApply = driver.find_element(
    By.XPATH,
    '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[3]/button[2]'
)
buttonApply.click()
# Scrape data
time.sleep(2)

df_list = []

# Cycle through pages -- May not be necessary when iterating daily
# while True:
#     try:
#         pageSource = driver.page_source
#         soup = BeautifulSoup(pageSource, 'lxml')
#         table = soup.find_all('table')
#
#         df_list.append(pd.read_html(pageSource)[0])
#
#         nextPage = WebDriverWait(driver, 3).until(
#             EC.element_to_be_clickable(
#                 (
#                     By.XPATH,
#                     '//*[@id="table-container"]/div/app-paginator/div/div[2]/mat-paginator/div/div/div[2]/button[3]'
#                 )
#             )
#         )
#         nextPage.click()
#     except selenium.common.exceptions.TimeoutException:
#         df = pd.concat(df_list, axis=0, ignore_index=True)
#         print(df)
#         break

# Cycle through the months
start_date = date(2017, 1, 1)
end_date = date(2022, 8, 2)

for date in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
    buttonFilter.click()  # Open the filter pane

    date2 = date + datetime.timedelta(days=1)

    field_dateStart.send_keys(Keys.CONTROL + 'a')
    field_dateStart.send_keys(Keys.DELETE)
    field_dateStart.send_keys(date.strftime('%m/%d/%Y'))

    field_dateEnd.send_keys(Keys.CONTROL + 'a')
    field_dateEnd.send_keys(Keys.DELETE)
    field_dateEnd.send_keys(date2.strftime('%m/%d/%Y'))

    buttonApply.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="UCRGroup"]'
            )
        )
    )
    pageSource = driver.page_source
    df_list.append(pd.read_html(pageSource)[0])

df = pd.concat(df_list, axis=0, ignore_index=True)
print(df.to_string())

df.to_sql('lex', engine, index=False)

# End the web session
# driver.quit()
