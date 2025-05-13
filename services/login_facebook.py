from urllib.parse import urlparse
from selenium.webdriver.common.by import By # type: ignore
import time
import json
import os
from utils.convert_cookie import convert_cookie_string
from utils.print_log import print_log
from utils.print_log import print_log

def login(driver):
    # If cookies exist, use them
    if os.path.exists('facebook_cookies.json'):
        print_log("Found saved cookies, loading...")
        with open('facebook_cookies.json', 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()  # Refresh to apply cookies
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        if  'login' in parsed_url.path:
            print_log("Login failed, please check your cookies.")
            return
        print_log("Logged in successfully from cookies!")
    else:
       print_log("Login failed, please check your cookies.")
       
def login_cookies(driver, cookie):
    driver.get("https://www.facebook.com/")
    cookies = convert_cookie_string(cookie)
    if not cookies:
        print_log("Login failed, please check your cookies.")
        return
    driver.delete_all_cookies()
    driver.refresh()
    for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()  # Refresh to apply cookies
    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    if  'login' in parsed_url.path:
        print_log("Login failed, please check your cookies.")            
        return False
    print_log("Logged in successfully from cookies!")
    return True
