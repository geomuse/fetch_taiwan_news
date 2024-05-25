import requests , time
from bs4 import BeautifulSoup
import os , pickle
from selenium import webdriver
from selenium.common.exceptions import WebDriverException , TimeoutException
from datacollection_bot.selenium_ import selenium_

from notification_bot.loguru_notification import loguru_notf

current_dir = os.path.dirname(os.path.abspath(__file__))
logger = loguru_notf(current_dir)
logger.add('news')

if __name__ == '__main__' : 

    url = 'https://news.ltn.com.tw/list/breakingnews/world'

    try : 
        selenium = selenium_()
        options = selenium.init_browser_display_headless()

        browser = webdriver.Firefox(options=options)
        browser.get(url)
        respone = browser.page_source

        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        soup = BeautifulSoup(browser.page_source,'html.parser')

        # soup h3 select.
        # soup = soups.select('h3',class_='title')
        # for element in soup : 
            # print(element.text)
        # print(soup.text)

        # soup a href.
        for element in soup.select('a',class_='title') :
            e = element.select('h3',class_='title')
            # span = element.select('span',class_='time')
            if e != []:
                logger.info(f"{e[0].text} : {element['href']}")

    except TimeoutException as e :
        print(f'{e}')

    except WebDriverException as e :
        print(f'{e}')

    except Exception as e : 
        print(f'{e}')

    finally : 
       browser.close()