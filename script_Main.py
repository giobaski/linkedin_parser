
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from time import sleep
from data import persons
import json, random, os
from pymongo.mongo_client import MongoClient
from selenium.webdriver.chrome.options import Options
import multiprocessing
from fake_useragent import UserAgent



def create_proxy_driver(proxy=None, useragent=None):
    chrome_option = Options()
    # chrome_option.add_argument(f'--proxy-server={proxy}')
    # chrome_option.add_argument(f'--user-agent={useragent}')
    # chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_option)

    driver.delete_all_cookies()

    # driver.getSessionStorage().clear()
    # driver.getLocalStorage().clear()
    # Session_id = driver.session_id
    # print("Session_ID: ", Session_id)

    homepage = 'https://www.linkedin.com'
    driver.get(homepage)

    return driver

# driver.set_page_load_timeout(60)


def login(driver, username, password):
    login_url = 'https://www.linkedin.com/uas/login'
    driver.get(login_url)

    username = driver.find_element_by_name('session_key').send_keys(username)
    sleep(2)
    password = driver.find_element_by_name('session_password').send_keys(password)
    sleep(10)
    log_in_button = driver.find_element_by_class_name('btn__primary--large').click()
    print('you are logged in successfully')
    return driver

def logout(driver):
    # logout = 'https://www.linkedin.com/uas/login/m/logout'
    pass

def what_is_my_ip():
    pass

proxy_and_credentials=[
                            {
                                'proxy': '168.81.216.74:41477',
                                'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                                'username': 'user111',
                                'password': 'pass111'
                            },
                            {
                                'proxy': '168.81.216.74:41477',
                                'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                                'username': 'user222',
                                'password': 'pass222'
                            }
                        ]

def random_proxy_and_credential():
    random_proxy_and_credential = random.choice(proxy_and_credentials)
    result = {}
    result['proxy'] = random_proxy_and_credential['proxy']
    result['useragent'] = random_proxy_and_credential['useragent']
    result['username'] = random_proxy_and_credential['username']
    result['password'] = random_proxy_and_credential['password']
    return result

helper = {
    'first': [1,2,3,4,5,6,7,8,9,10],
    'second': [1,2,3,4,5,6,7,8,9,10],
    'third': [1,2,3,4,5,6,7,8,9,10]
    }

# TEST MULTIPORCCESSING
def scrape_only_20(driver, all_links, counter):
    for i in range(3):
        link = driver.get(all_links[counter])
        ### SCRAPE IT HERE ###
        counter+=1 #ar izrdeba?

        print( "Counter from 20 function ", counter)
        sleep(2)



all_profiles = ['https://duckduckgo.com/1','https://duckduckgo.com/2','https://duckduckgo.com/3','https://duckduckgo.com/4']

def main():

    """ Changes IP address after scraping 20 profiles"""
    counter = 0
    for key, value in helper.items():
        r = random_proxy_and_credential()
        driver = create_proxy_driver(r['proxy'], r['useragent'])
        login(driver,r['username'],r['password'])

        for i in value:
            """ scraping function from old script """
            profile = driver.get(all_profiles[counter])

            print("COUNTER: ",counter)
            sleep(2)
            logout(driver)
            counter+=1

        driver.quit()

if __name__=='__main__':
    main()



# Multiprocessing
urls = ['https://developer.mozilla.org', 'https://duckduckgo.com']
def opendriver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(5)
# multiprocessing
pool = multiprocessing.Pool(2)
pool.map(opendriver, urls)
