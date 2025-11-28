from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from modify_links import modify_links

def get_links():
    service = Service("D:/python practice/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service = service)

    cities =  ["peshawar", "islamabad", "karachi", "lahore"]
    links = { }
    
    for city in cities:
        links[city] = []
        page = 0

        while True:
            if page == 0:
              url = f"https://houstel.pk/pakistan/{city}/hostels"
            else: url = f"https://houstel.pk/pakistan/{city}/hostels/page/{page}0"

            driver.get(url)
            try:
                load_more = driver.find_element(By.CLASS_NAME, "load-more-btn")
                load_more.click()
                time.sleep(10)
                WebDriverWait(driver, 6).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "load-more-btn"))
                )
            except: print("no more hostels to load.")
                
                
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            hostel_names = []

            for i in soup.find_all('a', "hostel-name"):
                h_name = i.text.strip()
                h_name = h_name.replace(" ", "-")
                print(h_name)
                hostel_names.append(h_name)
            
            if not hostel_names:
                print("loaded all hostels!")
                break

            for hostel_name in hostel_names:
                link = f"https://houstel.pk/pakistan/{city}/hostels/{hostel_name}-{city}"
                links[city].append(link)

                for l in links[city]:
                    print(l)

            page += 1
    
    with open("links.json",'w') as f:
       json.dump(links, f, indent=4)  
    
    links = modify_links()
    
    return links

get_links()