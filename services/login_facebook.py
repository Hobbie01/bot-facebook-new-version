from urllib.parse import urlparse
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import time
import json
import os
from utils.print_log import print_log
from utils.print_log import print_log

def login(driver):
    # Go to the Facebook login page
    driver.get('https://www.facebook.com/login')

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
        # If no cookies exist, log in manually
        print_log("Please log in to Facebook manually")
        input("Enter Any Key For Save Cookie")

        print_log("Logged in successfully!")
        
        # Save cookies
        cookies = driver.get_cookies()
        with open('facebook_cookies.json', 'w') as file:
            json.dump(cookies, file)
        print_log("Cookies have been saved!")
