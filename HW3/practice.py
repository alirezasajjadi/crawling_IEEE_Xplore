import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import ActionChains


options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")
search_Xpath = '//*[@id="LayoutWrapper"]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[1]/xpl-typeahead-migr/div/input'
element = driver.find_element(By.XPATH, search_Xpath)
element.send_keys("Blockchain")
element.send_keys(Keys.RETURN)

try: 
    # //*[@id="8946141"]/xpl-results-item/div[1]/div[1]/div[2]
    list_Xpath = '//*[@id="xplMainContent"]/div[2]/div[2]'git 
    # wait = WebDriverWait(driver, 20)
    # wait.until(lambda driver: len(driver.find_elements(By.XPATH, list_Xpath)) == 25)

    # list = driver.find_elements(By.XPATH, list_Xpath)
    # # names = []
    # for article in list:
    title_Xpath = '//*[@id="8946141"]/xpl-results-item/div[1]/div[1]/div[2]/h3/a'
    title = driver.find_element(By.XPATH, title_Xpath).text
    print(title)
except Exception as e:
    print(e)

driver.quit()