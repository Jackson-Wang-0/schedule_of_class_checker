from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time

meeting_types = ['DI', 'LE', 'LA', 'ST', 'SE', 'AC', 'CL', 'FI', 'FM',
                 'FW', 'IN', 'IT', 'MU', 'OT', 'PB', 'PR', 'RE']


def scrape(driver, class_name):
    for name in class_name:
        driver.get("https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm")
        # click on 'by code(s)'
        elements = driver.find_element_by_link_text('by code(s)')
        elements.click()

        element = driver.find_element_by_id('courses')
        element.send_keys(name)

        element = driver.find_element_by_id('socFacSubmit')
        element.click()

        element = driver.find_elements_by_class_name('sectxt')
        html_doc = ''
        for elem in element:
            html_doc += elem.get_attribute('innerHTML')

        soup = BeautifulSoup(html_doc, 'lxml').text
        arr = soup.split()

        total_arr = []
        curr_arr = []

        for elem in arr:
            if elem.isnumeric() and int(elem) > 10000:
                continue
            if elem in meeting_types:
                if len(curr_arr) != 0:
                    total_arr.append(curr_arr)
                else:
                    pass
                curr_arr = [elem]
            else:
                curr_arr.append(elem)
        total_arr.append(curr_arr)
        df = pd.DataFrame(total_arr)
        df = df.replace('FULL', 0)
        avail_seats = sum(map(lambda x: float(x) if str(x).isnumeric() else 0, np.array(df[9].dropna())))

        if avail_seats > 0:
            print(f'There are {int(avail_seats)} seats left in {name}.')
        else:
            print(f'There is no remaining seat left in {name}.')

        element = driver.find_element_by_link_text('Start a new search')
        element.click()


driver = webdriver.Chrome(ChromeDriverManager().install())
codes = input("Enter class codes, separated by commas, followed by ENTER: ")
codes = codes.split(sep=',')

while True:
    scrape(driver, codes)
    time.sleep(60)

