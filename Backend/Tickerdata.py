#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

website = 'https://www.niftyindices.com/market-data/equity-stock-watch'

path = r'D:\Downloads\chromedriver-win64\chromedriver.exe'

service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)
print('Extracting data from NSE')

wait = WebDriverWait(driver, 10)

locator = (
    By.XPATH,
    "//a[contains(@class,'btn') and contains(@class,'btn-select')]" #Not 'btn btn-select active', active brought only after dropdown accessed.
)
dropdown_trigger = wait.until(EC.element_to_be_clickable(locator))
dropdown_trigger.click()

all_options = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul#ddlStocks .mCSB_container li"))
)


for option in all_options:
    driver.execute_script("arguments[0].scrollIntoView({ block: 'center' });", option)
    time.sleep(0.1) 
    if option.text.strip() == "Nifty 200":
        wait.until(EC.element_to_be_clickable(option))
        option.click()
        break
  
else:
    print("Loop completed without finding 'Nifty 200'")

time.sleep(1)
table = driver.find_element(By.CLASS_NAME, "equityTable")
rows = table.find_elements(By.TAG_NAME, "tr")  
time.sleep(0.5)

dataset = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells:
        dataset.append(cells[0].text)

pd.set_option('display.max_rows',10)
df = pd.DataFrame(dataset)
df = df.rename(columns = { 0:'Ticker'})
df.to_csv("Tickers_NSE200")

driver.close()
print('Completed')



