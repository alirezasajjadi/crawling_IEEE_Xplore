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

def extract_paper(paper_url):

    driver.get(paper_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'document-abstract')))

    title = driver.find_element(By.CLASS_NAME, 'document-title').text
    
    try:
        cites_in_papers = driver.find_element(By.XPATH, "//div[contains(text(),'Cited by Papers')]").text.split(':')[-1].strip()
    except:
        cites_in_papers = None

    try:
        cites_in_patent = driver.find_element(By.XPATH, "//div[contains(text(),'Cited by Patents')]").text.split(':')[-1].strip()
    except:
        cites_in_patent = None

    try:
        full_text_views = driver.find_element(By.XPATH, "//div[contains(text(),'Full Text Views')]").text.split(':')[-1].strip()
    except:
        full_text_views = None
        
    publisher = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/div/div[1]/xpl-publisher/span/span/span/span[2]').text
    
    try:
        DOI = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[3]/div[2]/div[1]/a').text
    except:
        DOI = None
    
    
    data_of_publication = None

    try:
        data_of_publication = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[3]/div[1]/div[1]').text.split(":")[-1]
    except:
        pass

    if data_of_publication is None:
        try:
            data_of_publication = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[4]/div[1]/div[2]').text.split(":")[-1]
        except:
            pass

    if data_of_publication is None:
        try:
            data_of_publication = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[2]/div[1]/div[1]').text.split(":")[-1]
        except:
            pass

    try:
        abstract = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[1]/div/div/div').text
    except:
        abstract = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[1]/div/div/div').text
    
    published_in = None
    try:
        published_in = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[2]/a')
    except:
        pass
    
    if published_in is None:
        try :
            published_in = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[3]/a')
        except:
            pass
    
    published_in_link = None
    published_in_text = None
    
    if published_in is not None:
        published_in_link = published_in.get_attribute('href')
        published_in_text = published_in.text


    authors = []
    try :
        accordion_header = driver.find_element(By.ID, 'authors-header')
        accordion_header.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'authors')))

            # Find all author elements
        try : 
            author_elements = driver.find_elements(By.CSS_SELECTOR, '.authors-accordion-container')


            # Iterate through each author element to extract name and university
            for author_element in author_elements:
                author_name_element = author_element.find_element(By.CSS_SELECTOR, 'a span')
                author_name = author_name_element.text.strip()
                
                university_element = author_element.find_element(By.CSS_SELECTOR, 'div:nth-child(2)')
                university = university_element.text.strip()
                author_info = {
                    "name": author_name,
                    "from": university
                }
                authors.append(author_info)
        except :
            authors = None
    except:
        authors = None

 
    tab_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'keywords-header'))
    )
    tab_element.click()
    
    keywords_container = driver.find_element(By.CLASS_NAME, 'doc-keywords-list')

    # Extract IEEE Keywords
    ieee_keywords = []
    ieee_keywords_elements = keywords_container.find_elements(By.XPATH, "//strong[text()='IEEE Keywords']/following-sibling::ul/li/a")
    ieee_keywords = [element.text.strip() for element in ieee_keywords_elements if element.text.strip() != '']

    # Extract Author Keywords
    author_keywords = []
    author_keywords_elements = keywords_container.find_elements(By.XPATH, "//strong[text()='Author Keywords']/following-sibling::ul/li/a")
    author_keywords = [element.text.strip() for element in author_keywords_elements if element.text.strip() != '']
    
    print(title)

    return {
        "title": title,
        # "Page(s)": pages,
        "Cites in Papers": cites_in_papers,
        "Cites in Patent": cites_in_patent,
        "Full Text Views": full_text_views,
        "Publisher": publisher,
        "DOI": DOI,
        "Date of Publication": data_of_publication,
        "Abstract": abstract,
        "published in" :[{"name": published_in_text, "link": published_in_link}],
        "Authors": authors,
        "IEEE keywords": ieee_keywords,
        "Author Keywords": author_keywords
    }   


def extract_from_multiple_pages(paper_urls):
    papers = []
    
    for page in paper_urls:
        for url in page:
            # Navigate to the paper URL
                driver.get(url)
                
                # Extract paper details (assuming this function exists)
                paper_details = extract_paper(url)
                papers.append(paper_details)
                
                # Go back to the previous page after extracting paper details
                driver.back()
    
    return papers


def get_urls(num_pages):
    paper_urls = []
    current_page = 1
    
    while current_page <= num_pages:
        print(current_page)
        # Find all paper elements on the current page
        paper_elements = driver.find_elements(By.XPATH, "//a[@class='fw-bold']")
        
        # Capture URLs of all papers on this page
        paper_urls.append([paper_element.get_attribute('href') for paper_element in paper_elements if "courses" not in paper_element.get_attribute('href')])
        # Check if there's a next page button
        try:
            next_button = driver.find_element(By.XPATH, "//*[contains(@class, 'stats-Pagination_arrow_next')]")
            next_button.click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'List-results-items')))
            current_page += 1
        except:
            print("No more pages or next button not found.")
            break
    
    return paper_urls

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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'List-results-items')))
        urls = get_urls(5)
        papers = extract_from_multiple_pages(urls)
        print(papers)
                
    except Exception as e:
        print('error:\n', e)  
        
    driver.quit()



