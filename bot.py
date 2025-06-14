from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from services.comment_page import start_comment_in_page
from services.test import chat_bot
from utils.print_log import print_log
import os
import time

def bot_start( config):
    # สร้าง path profile ใหม่ไว้ในโฟลเดอร์โปรเจกต์
    profile_path = os.path.join(os.path.dirname(__file__), "chrome-profile")

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    if not config['show']: 
            options.add_argument("--headless")
    # setup driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    print_log("Starting the bot...")
    status = True

    try:
        while status:
            print_log("start")
            chat_bot(driver)


    except KeyboardInterrupt:
        print_log("🛑 Bot stopped by user.")
        driver.quit()
