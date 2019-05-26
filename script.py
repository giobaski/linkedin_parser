#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from time import sleep
from data import persons
import json, random, os
from pymongo.mongo_client import MongoClient
import fake_credentials

base_dir = os.getcwd()
# logout = 'https://www.linkedin.com/uas/login/m/logout'


""" შევქმნათ ვებბრაუზერის ობიექტი და დავუკავშირდეთ ჩვენთვის საჭირო ლინკს """
driver = webdriver.Chrome(os.path.join(base_dir, 'chromedriver'))
driver.get('https://www.linkedin.com/uas/login')


def login(username, password):
    """ აუთენთიფიკაციის ფუნქცია """
    user = driver.find_element_by_name('session_key').send_keys(username)
    sleep(1)
    password = driver.find_element_by_name('session_password').send_keys(password)
    sleep(1)
    log_in_button = driver.find_element_by_class_name('btn__primary--large').click()
    print('you are logged in successfully')



""" რენდომად ამოვირჩიოთ ყალბი მომხმარებელი json ფაილში შენახული ექაუნთებიდან """
with open('fake_credentials.json') as file:
     accounts = json.load(file)
user = random.choice(accounts['accounts'])

# random.choice(credentials)
username = user['username']
password = user['password']

try:
    login(username, password)
except:
    print("can't login now, try another credentials")
print(driver.current_url)




""" data ფაილისგან შედგენილი ქვაერების მიხედვით წამოვიღოთ პროფილის ინფორმაციები: """

queries = [person["person_name"] + " " + person['title'] + " " + person['city'] for person in persons]
print(queries)

profile_urls = []
for query in queries:
    try:
        # მოვნიშნოთ შიდა ძებნის html ელემენტი
        search = driver.find_element_by_css_selector('#ember33 > input[type=text]')
        # გადავცეთ შესაბამისი ქვაერი
        search.send_keys(query)
        # გავუშვათ ძებნა
        search.send_keys(Keys.ENTER)
        sleep(3)

        # შიდა ძებნის შედეგი
        result = driver.find_element_by_class_name('EntityPhoto-circle-4-ghost-person')
        # გადავიდეთ პროფილის გვერდზე
        result.click()
        sleep(5)

        print(driver.current_url)
        profile_urls.append(driver.current_url)
    except:
        # driver.back()
        # გავასუფთავოთ ძებნის ელემენტი წარუმატებელი ქვაერისგან
        search.clear()
        sleep(5)
        print("add later!!!!")
    sleep(3)
print(driver.current_url)
print ("profiles:", profile_urls)



final_results = {}
single_profile_dict={}
for url in profile_urls:
    """მოძებნილი პროფილებიდან დეტალური ინფორმაციის წამოღება"""
    profile = driver.get(url)
    print('URL: ', driver.current_url)
    sleep(5)

    # შევინახოთ პროფილის html სორსი ცალკე ცვლადში
    profile_selector = Selector(text=driver.page_source)
    print(profile_selector)
    sleep(random.randint(2, 5))



    # full name of user
    person_name = profile_selector.xpath('// *[ @ id = "ember43"] / div[2] / div[2] / div[1] / ul[1] / li[1]/text()').get()
    if person_name:
        person_name = person_name.strip()
    print("Person_name", person_name)

    # working experience (Where he/she worked)
    experience = profile_selector.xpath("// div[2] / h3/ text()").getall()
    print("Experiense: ", experience)

    # current position or job title (CTO, CEO, Senior Engineer, etc)
    position = profile_selector.xpath('//*[@id="ember43"]/div[2]/div[2]/div[1]/h2/text()').get()
    if position:
        position = position.strip()
    print("Position: ", position)

    # list of companies where he/she worked at
    companies = profile_selector.xpath("// div[2] / h4 / span[2]/ text()").getall()
    print("Companies: ", companies)


    single_profile_dict = {}
    single_profile_dict['_id'] = url
    single_profile_dict['person_name'] =  person_name
    single_profile_dict['experience'] = experience
    single_profile_dict['position'] = position
    single_profile_dict['companies'] = companies


    final_results[url] = single_profile_dict

driver.quit()




"""საბოლოო შედეგების ბაზაში შენახვა"""

#connect MongoDB local machine
client = MongoClient('localhost', 27017)
#db

db = client.linkedin

#collection
collection = db.user_info

# Insert
collection.insert_many(final_results.values())

print("final results:", final_results)