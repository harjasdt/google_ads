import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re

def location(linkk,count):
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")
    # options.headless = True  # Run Chrome in headless mode (no GUI)
    options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking
    options.add_argument("--disable-notifications")   # Disable notifications


    # Initialize WebDriver
    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    url = linkk
    chrome_driver.get(url)

    # Wait for the page to load (adjust time as needed)
    time.sleep(2)

    # Get page source
    page_source = chrome_driver.page_source

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all <div> tags
    div_tags = soup.find_all('div')
    ls=[]
    # Print text content of each <div> tag
    # with open('waste.txt', 'w',encoding='utf-8') as f:
    for div in div_tags:
        # print(div.text.strip())
        with open(f'./ads_divs/{count}.txt', 'a',encoding='utf-8') as f:
            f.write(div.text.strip())
        if('Included regions selected for this ad' in div.text.strip()):
            ls.append(div.text.strip().replace('Included regions selected for this ad',''))


    with open('inc_locations.txt', 'a',encoding='utf-8') as f:
        try:
            f.write(f'{ls[-2]}\n')
        except:
            flag=0
            for div in div_tags:
                # print(div.text.strip())
                if('excludedLocationadd' in div.text.strip()):
                    # print(div.text)
                    match = re.search(r'excludedLocationadd(.*?)remove', div.text.strip())
                    # Check if a match is found
                    print(match)
                    if match:
                        print("Match found!")
                        flag=1
                        extracted_text = match.group(1).strip()
                        with open('inc_locations.txt', 'a',encoding='utf-8') as f:
                            f.write(f'{extracted_text}\n')
                            break
                        # print("Extracted text:", extracted_text)
            if(flag==0):
                with open('inc_locations.txt', 'a',encoding='utf-8') as f:
                    f.write(f'{linkk}\n')
                    # break
            else:
                print(flag)

    # Close the WebDriver
    chrome_driver.quit()


# location('https://adstransparency.google.com/advertiser/AR01871034538939908097/creative/CR18435799912923791361?region=20471&start-date=2023-06-23&end-date=2024-06-01&topic=political')
df=pd.read_csv('inc_final.csv')
for index,row in df.iterrows():
    if(index>=267):
        print(f'Processing {index}...')
        location(row['link'],index)
    # break
    # break