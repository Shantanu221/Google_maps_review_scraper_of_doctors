from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElementhttps://www.edhacare.com/doctors?page=1
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import json
import pandas as pd

options = Options()
options.headless = True
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

website = 'https://www.edhacare.com/doctors?page=1'

driver.get(website)
driver.maximize_window()
result = []
curr_page = 1

while curr_page <= 80:
    time.sleep(4)
    doctors = driver.find_elements(by='xpath', value='//div[@class="row doctorlist my-5 p-lg-5 p-2"]')

    for doc in doctors:
        time.sleep(5)
        name = doc.find_element(by='xpath', value='./div/h2').text
        print(name)
        place = doc.find_element(by='xpath',value='./div[2]/div/div[4]/div/div[2]/p').text
        print(place)
        link = doc.find_element(by='xpath', value='./div/a').get_attribute('href')
        spec = doc.find_element(by='xpath', value='./div/p').text
        spec = spec.strip("()")
        hospital = doc.find_element(by='xpath', value='./div[2]/div/div[3]/div/div[2]/p').text
        img_src = doc.find_element(by='xpath',value='./div/a/img').get_attribute('src')
        expe = doc.find_element(by='xpath',value='./div[2]/div/div[2]/div/div[2]/p').text
        ratings=""
        try:
            r = doc.find_element(by='xpath',value='./div[2]/div[3]/div[3]/div/p').text
        except:
            r = doc.find_element(by='xpath', value='./div[2]/div[3]/div[4]/div/p').text
        for s in r:
            ratings+=s
            if(s==" "):
                break
        reviews_link=""
        try:
            reviews_link = doc.find_element(by='xpath', value='./div[2]/div[3]/div[3]/div/p/a').get_attribute('href')
        except:
            reviews_link=""
        reviews=[]
        try:
            reviews_link = doc.find_element(by='xpath',value='./div[2]/div[3]/div[3]/div/p/a').get_attribute('href')
            if(reviews_link=='http://drkmedhioncology.in/'):
                raise Exception("Not reachable")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(reviews_link)

            try:

                time.sleep(3)
                more_rev_btn = driver.find_element(by='xpath',value='//button[contains(@aria-label,"More reviews")]')
                driver.execute_script("arguments[0].click();", more_rev_btn)
                time.sleep(5)

                text = ""

                t_revs = driver.find_elements(by='xpath', value='//div[@class="MyEned"]')
                # time.sleep(3)
                for t in t_revs:
                    try:
                        more_btn = t.find_element(by='xpath',value='./span[2]/button')
                        driver.execute_script("arguments[0].click();", more_btn)
                        time.sleep(2)
                    except:
                        pass
                    te = t.find_element(by='xpath',value='./span').text
                    disp = {'text':te}
                    reviews.append(disp)
                # print(reviews)
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                # time.sleep(3)
        except:
            reviews=[]
            # reviews_link=""
            # print(reviews)
        descp = {'name':name,'location':place,'profile_link':link,'speciality':spec,'hospital':hospital,'img_src':img_src,'experience':expe,'ratings':ratings,'reviews_link':reviews_link,'reviews':reviews}
        result.append(descp)

    curr_page += 1

    try:
        element = driver.find_element(by='xpath',value='//a[@rel="next"]')
        driver.execute_script("arguments[0].click();", element)
    except:
        break

result_json = json.dumps(result)

with open('result.json','w') as file:
    file.write(result_json)


driver.quit()
