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


def crawling_method(driver):

    wait_page_load(driver=driver)

    title_Xpath = '//h3/a'
    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_all_elements_located((By.XPATH, title_Xpath))
    # )
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1

    article_links = driver.find_elements(By.XPATH, title_Xpath)

    processed_urls = set()  # avoid twice open article!

    for idx, article in enumerate(article_links):
        link = article.get_attribute('href')
        
        if link in processed_urls:
            continue
        processed_urls.add(link)  # Add URL to processed set

        driver.switch_to.new_window('tab')
        driver.get(link)

        # wait to fully load page, use time.sleep(xxx) if it wasted to time
        wait_page_load(driver=driver)

        time.sleep(2)




        """TODO"""
        """example:"""
        article_title = driver.find_element(By.XPATH, '//h1').text
        print("Title:", article_title)





        driver.close()
        driver.switch_to.window(original_window)

    return driver


def wait_page_load(driver):
    """wait until 'Feedbak' button appeared"""
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'usabilla_live_button_container'))
    )

if __name__ == "__main__":
    try:
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")
        search_Xpath = '//*[@id="LayoutWrapper"]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[1]/xpl-typeahead-migr/div/input'
        element = driver.find_element(By.XPATH, search_Xpath)
        element.send_keys("Blockchain")
        element.send_keys(Keys.RETURN)
        
        wait_page_load(driver=driver)

        driver = crawling_method(driver=driver)

        print("hey")

        # //*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul/li[2]/button
        next_page_buttons_xpath = '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul/li'
        next_page_buttons = driver.find_elements(By.XPATH, next_page_buttons_xpath)

        # iterate over pages
        for i in range(0,5):
            ActionChains(driver).move_to_element(next_page_buttons[i]).perform()
            next_page_buttons[i].click()

            wait_page_load(driver=driver)

            driver = crawling_method(driver=driver)

    except Exception as e:
        print('error:\n', e)  

    driver.quit()



