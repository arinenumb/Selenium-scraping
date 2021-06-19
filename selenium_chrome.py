from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.by import By

import csv
from time import sleep

# url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'
# url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
url = 'https://www.nseindia.com'

ua = UserAgent()
useragent = ua.ie

options = webdriver.ChromeOptions()
options.add_argument('user-agent=' + useragent)
# options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(executable_path='assets/chromedriver',
                          options=options)

try:
    driver.get(url)

    market = driver.find_element_by_css_selector('#main_navbar > '
                                                  'ul > '
                                        'li:nth-child(3) > a')
    pre_op = driver.find_element_by_xpath('//*['
                                          '@id="main_navbar"]/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a')
    action = ActionChains(driver)
    action.move_to_element(market).perform()
    action.click(pre_op).perform()
    sleep(2)

    html = driver.find_element_by_tag_name('html')

    n = 0
    while n < 14:
        html.send_keys(Keys.ARROW_DOWN)
        n = n + 1
        sleep(0.2)

    table = driver.find_elements_by_xpath('//*['
                                          '@id="livePreTable"]/tbody/tr')
    len_row = len(table)
    l = []
    for i in range(1, len_row + 1):
        e = []
        d = driver.find_element_by_xpath('//*['
                                              f'@id="livePreTable"]/tbody/tr[{str(i)}]/td[2]')
        e.append(d.text)
        c = driver.find_element_by_xpath(f'//*['
                                              f'@id="livePreTable"]/tbody/tr[{str(i)}]/td[7]')
        e.append(c.text)
        l.append(e)


    with open('data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ('Имя', 'Цена')
        )

    for rec in l:
        with open('data.csv', 'a') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                rec
            )

    sleep(6)

    # Действия пользователя
    y = 0
    while y < 16:
        html.send_keys(Keys.ARROW_UP)
        y = y + 1
        sleep(0.2)

    sleep(2)

    driver.find_element_by_xpath('//*[@id="main_navbar"]/ul/li['
                                 '1]/a').click()

    home_html = driver.find_element_by_tag_name('html')
    while True:
        home_html.send_keys(Keys.ARROW_DOWN)
        try:
            nifty_bank = driver.find_element_by_xpath(
                '//*[@id="nse-indices"]/div['
                '2]/div/div/nav/div/div/a[4]')
        except Exception as e:
            continue

        nifty_bank.click()
        break

    # button_html = driver.find_element_by_tag_name('html')
    while True:
        home_html.send_keys(Keys.ARROW_DOWN)
        sleep(0.2)
        try:
            button = driver.find_element_by_xpath(
                '//*[@id="tab4_gainers_loosers"]/div[3]/a')
        except ElementClickInterceptedException as e:
            continue

        button.click()
        break


    sleep(4)

    select_element = driver.find_element(By.ID, 'equitieStockSelect')
    select_object = Select(select_element)
    select_object.select_by_value('NIFTY ALPHA 50')

    sleep(3)

    win = driver.find_element_by_tag_name('html')
    for i in range(15):
        win.send_keys(Keys.ARROW_DOWN)



    sleep(3)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


