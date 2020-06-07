# Trial
import sys
import pip
from pip._internal import main

def install(module):
    main(['install', module])

packages = ['pandas', 'selenium', 'numpy', 'mysql-connector', 'webdriver-manager']

# Check if modules exist

for module in packages:
    try:
        import module
    except ImportError:
        print(module + ' is not installed. Installing now')
        install(module)




import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import mysql.connector
import time

import sys
import pip



def install(package):
    pip.main(['install', package])


data = []
count = 1


class arthaScraper(object):

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        self.driver.get('https://new.solaramr.com/Login/Login')

        #         WebDriverWait(self.driver, 10).until(EC.find_element_by_id("UserName")
        username = self.driver.find_element_by_id("UserName")
        password = self.driver.find_element_by_id("Password")

        username.send_keys("ssi")
        password.send_keys("sheet@123")

        #         self.driver.find_element_by_id("submit")

        self.driver.find_element_by_xpath('/html/body/div/form/div/div/div[2]/div[4]/div/button').click()

        return

    def click_error_logs(self):

        self.driver.implicitly_wait(3)
        error_box = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="myModal"]/div[2]/div/div/button')))
        error_box.click()

        return

    def select_dates(self):

        Continue = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[10]/a')))
        Continue.click()

        self.driver.implicitly_wait(3)
        date_start = self.driver.find_element_by_id("datepicker1")
        date_start.clear()
        date_start.send_keys('01/12/2019')

        self.driver.implicitly_wait(3)
        date_end = self.driver.find_element_by_id("datepicker2")
        date_end.clear()
        date_end.send_keys('31/01/2020')

        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id('btnclickk').click()

        #         error_element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.link_text, '/html/body/app-root/app-inject-solar/div/div[2]/div[1]/app-header/div[2]/nav/nav/div/ul/li[6]/a')))
        #         error_element.click()

        return

    def pagination(self):

        try:
            page_num = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="table_i_paginate"]/span/a[7]')))
            page_num_total = page_num.text

        except:
            page_num = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="table_i_paginate"]/span/a[6]')))
            page_num_total = page_num.text

        return int(page_num_total)

    def get_table(self, page_num_total):

        global count

        self.driver.implicitly_wait(5)

        table_element = self.driver.find_element_by_xpath('//*[@id="table_i"]/tbody')
        rows = table_element.find_elements_by_tag_name("tr")

        for rnum in range(0, len(rows)):

            columns = rows[rnum].find_elements_by_tag_name("td")

            rnum += 1

            for cnum in range(0, len(columns)):
                #                 print(columns[cnum].text)
                data.append(columns[cnum].text)
                cnum += 1
        #         self.driver.implicitly_wait(5)

        next_page = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/div/div[4]/a[2]')))
        next_page.click()
        count = count + 1

        return

    def close_window(self):
        self.driver.quit()
        return


test = arthaScraper()
test.login()
test.click_error_logs()
test.select_dates()
page_num = int(test.pagination())

while count < page_num:
    test.get_table(page_num)
test.get_table(page_num)
test.close_window()

# print(page_num_total)
# print(data)

np_array = np.array(data)

reshaped = np.array(np.array_split(np_array, len(data)/8))

# print(reshaped.shape)

dataframe = pd.DataFrame(reshaped)




try:
    arthaDb = mysql.connector.connect(host="127.0.0.1", port=5500, user='root', passwd='Tsha@5755')

    arthaCursor = arthaDb.cursor()
    arthaCursor.execute("CREATE DATABASE solaramrdb")
    print('Creating Solaramrdb schema in MySQL')
    # arthaCursor.execute("Show databases")
    # for db in arthaCursor:
    #     print(db)
    arthaDb.close()
except:
    print('Database already exists! Moving on...')


try:
    arthaTableConnector = mysql.connector.connect(host="127.0.0.1", port=5500, user='root', passwd='yourMysqlPasswordhere',
                                                  database='SolarAmrDb')

    arthaTableCursor = arthaTableConnector.cursor()
    print('Creating solarvalues table in SolarAmrDb')
    arthaTableCursor.execute(
        "CREATE TABLE solarvalues(ID VARCHAR(8) NOT NULL, Date VARCHAR(28) NOT NULL, `Total Generation[kWh]` FLOAT(20), CUF FLOAT(20), `Peak Generation[kW]` FLOAT(20), `DateTime [MD]` VARCHAR(25), `Specific Power` FLOAT(20), `Specific Yield` FLOAT(20))")

except:
    print('Table already exists! Moving on...')



print('Pushing Data into the table')
for index, row_val in dataframe.iterrows():
    add_data = """INSERT INTO solarvalues
                (ID, DATE, `Total Generation[kWh]`, CUF, `Peak Generation[kW]`, `DateTime [MD]`, `Specific Power`, `Specific Yield`) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    column_vals = (row_val[0], row_val[1], row_val[2], row_val[3], row_val[4], row_val[5], row_val[6], row_val[7])
    arthaDb = mysql.connector.connect(host="127.0.0.1", port=5500, user='root', passwd='yourMysqlPasswordhere',
                                      database='SolarAmrdb')

    cursor_c = arthaDb.cursor()
    cursor_c.execute(add_data, column_vals)
    arthaDb.commit()
    cursor_c.close()
    arthaDb.close()

print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print('Display all values in MySQL')
arthaDb = mysql.connector.connect(host="127.0.0.1", port=5500, user='root', passwd='yourMysqlPasswordhere', database = 'SolarAmrdb')
# print(arthaDb)
cursor = arthaDb.cursor()
# print(cursor)

cursor.execute("""SELECT * FROM solarvalues""")

result = cursor.fetchall()

print(result)
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
