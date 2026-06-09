from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions #as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time
from utils import write_file

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service,options=options)

driver.get("http://10.2.232.163:3000")
time.sleep(5)

login = input("user logged in ")

if login in ('y','1'):
    driver.get("http://10.2.232.163:3000/pcbb/global/reporting/page/?reportid=1")
    time.sleep(5)
    breakpoint()
    element_id = "report_tbl_data"  # Replace with the actual ID of the element you want to select

    element = driver.find_element(By.ID,value=element_id)
    # Extract the text from the element
    data = element.text
    print("Extracted text:", data)
    if data:
        write_file("report1.txt",data)

    time.sleep(5)