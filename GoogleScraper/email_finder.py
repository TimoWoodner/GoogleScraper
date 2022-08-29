import sys
import threading
import time
import re
from unittest import result
from functools import reduce

try:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from selenium.common.exceptions import ElementNotVisibleException
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
    from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
except ImportError as ie:
    print(ie)
    sys.exit('You can install missing modules with `pip3 install [modulename]`')

from GoogleScraper.selenium_mode import SelScrape
from GoogleScraper.user_agents import random_user_agent
from GoogleScraper.scrape_config import chromedriver_path

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_valid_email(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

class EmailFinder():
    "Find email of person by browsing all links"
    results = []
    links = []
    browser_mode = "headless" 
    

    def __init__(self, links, info = {}):
        self.links = links
        self.info = info
        self.user_agent = random_user_agent()
        self.webdriver = self._get_Chrome()

    def _get_Chrome(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = ""

            # save resouces, options are experimental
            # See here:
            # https://news.ycombinator.com/item?id=14103503
            # https://stackoverflow.com/questions/49008008/chrome-headless-puppeteer-too-much-cpu
            # https://engineering.21buttons.com/crawling-thousands-of-products-using-aws-lambda-80332e259de1
            chrome_options.add_argument("test-type")
            chrome_options.add_argument('--js-flags="--expose-gc --max-old-space-size=500"')
            chrome_options.add_argument(
                'user-agent={}'.format(self.user_agent))
            chrome_options.add_argument('--enable-precise-memory-info')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--incognito')
            chrome_options.add_argument('--disable-application-cache')


            if self.browser_mode == 'headless':
                chrome_options.add_argument('headless')
                #chrome_options.add_argument('window-size=1200x600') # optional

            return webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

        except WebDriverException as e:
            # we don't have a chrome executable or a chrome webdriver installed
            raise

    def run(self):

        if not self.webdriver:
            raise Exception('{}: Aborting: No available selenium webdriver.'.format(self.name))

        for link in self.links:
            self.enter_link(link)
    
    def enter_link(self, link):
        print("Enter", link)
        self.webdriver.get(link)
        els = self.webdriver.find_elements(By.XPATH,"//*[contains(text(),'@')]")
        for el in els:
            text = str(el.text).lower()
            if text != "": 
                for word in text.split(" "):
                    if self.mail_validate(word): 
                        self.results.append(self.mail_validate(word))
        
    def get_result(self):
        return self.results

    def mail_validate(self, possible_email):
        if not check_valid_email(possible_email):
            return False

        email_name = possible_email.split('@')[0]
        domain_name = possible_email.split('@')[1]
        accuracy = 0

        if self.info.get('name', False):
            # split firt name, last name
            name = self.info.get('name').split(" ")
            # find the overlap of person name with the email
            accuracy = reduce(lambda a, b: a + 1 if b in email_name else 0, name)
            if accuracy < 1:
                return False

        if "gmail" in domain_name:
            pass
        elif "yahoo" in domain_name:
            pass
        elif self.info.get('company', False):
            company_short_name = self.info.get('company').split(" ")[0]
            if company_short_name in domain_name:
                accuracy += 1
            
        if accuracy < 1:
            return False 
        return True



            
            
                
                    

    
