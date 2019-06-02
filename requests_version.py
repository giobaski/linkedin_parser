import random
import requests
import typing
from bs4 import BeautifulSoup
from multiprocessing import Pool
from time import sleep



def get_html(url:str, proxy = None, useragent=None)->str:
    """Returns page sources"""
    html = requests.get(url, headers=useragent, proxies=proxy).text
    print(url)
    return html


def what_is_my_ip(proxy=None)->str:
    """prints my current proxy IP address"""

    html = requests.get('https://www.whatismybrowser.com/detect/ip-address-location', proxies=proxy).text
    soup = BeautifulSoup(html, 'lxml')
    my_ip = soup.find('div', class_="content").find('strong').text
    print('your current IP: ',my_ip)
    return my_ip


def what_is_my_useragent()->str:
    """prints my current User-Agent"""

    html = requests.get('https://www.whatismybrowser.com/detect/what-is-my-user-agent').text
    soup = BeautifulSoup(html, 'lxml')
    my_user_agent = soup.find('div', class_="value").find('a').text
    print('your current User-Agent: ',my_user_agent)
    return my_user_agent


profile_links = ['www.1.com','www.2.com']

def main():
    useragents = open('useragents_list.txt').read().split('\n') # returns list of useragents
    proxies = open('proxy_ip_list.txt').read().split('\n') # returns list of proxies

    url = 'https://duckduckgo.com'
    for i in range(1):
        sleep(random.uniform(1,5))
        proxy = {'http': 'https://' + random.choice(proxies)}
        useragent = {'User-Agent': random.choice(useragents)}

        print("prox", proxy)
        try:
            html = get_html(url, proxy, useragent)
            what_is_my_ip(proxy)
            # what_is_my_useragent()
            print(i, '-done')
        except:
            print("can't get html")


if __name__ == '__main__':
    main()



