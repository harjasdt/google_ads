import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Set up Chrome options
options = Options()
options.headless = True  # Run Chrome in headless mode (no GUI)

# Initialize WebDriver
chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the URL
url = 'https://adstransparency.google.com/advertiser/AR01871034538939908097?region=20471&start-date=2024-06-01&end-date=2024-06-21&topic=political'
chrome_driver.get(url)

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(7)  # Wait for the page to load new content
    print("SCROLLED!!!!")

# Collect all hrefs
hrefs = set()
lst=[]
try:
    last_height = chrome_driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll to the bottom
        scroll_to_bottom(chrome_driver)

        # Wait for new elements to load
        try:
            WebDriverWait(chrome_driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//creative-preview"))
            )
        except TimeoutException:
            break
        # Check if we've reached the bottom of the page
        new_height = chrome_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract hrefs from <a> tags within each creative-preview element
    profile_elements = chrome_driver.find_elements(By.XPATH, "//creative-preview")
    for element in profile_elements:
        
        a_tags = element.find_elements(By.TAG_NAME, 'div')
        l=[]
        all_a = element.find_elements(By.TAG_NAME, 'a')
        for a in a_tags:
            href = a.text.strip()
            l.append(href)
            # print(href)
            # if href:
            
            #     lst.append(dic)
        
        
        # print(l[-1],l[-2],l[-3],all_a[0].get_attribute('href'))
        dic={'spent':l[-1],
             'date':l[-2],
             'shown':l[-3],
             'link':all_a[0].get_attribute('href')}
        # hrefs.add(dic)
        # print(a.get_attribute('href'))
        with open('./monthlyads/jun24.txt', 'a',encoding='utf-8') as f:
            f.write(f"{dic},\n")
finally:
    # Close the WebDriver
    chrome_driver.quit()
    # pass
    # print(hrefs)

# # Save hrefs to a text file
# with open('links.txt', 'w') as f:
#     for href in hrefs:
#         f.write(f"{href}\n")

# print(f"Saved {len(hrefs)} links to links.txt")
