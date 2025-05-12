from selenium import webdriver # type: ignore

from selenium.webdriver.chrome.service import Service # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
import undetected_chromedriver as uc
import chromedriver_autoinstaller
from utils.print_log import print_log
from datetime import datetime
from services.login_facebook import login

# from services.comment_in_post import start_comment_in_post
from services.post_in_group import start_post_in_group
import time

def bot_start(selected,config): 
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-infobars')
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-translate")  # ปิดการแปลภาษาอัตโนมัติ
    options.add_argument("--disable-popup-blocking")  # ปิดการบล็อกป็อปอัพ
    if config['show']: 
        options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model

    # ติดตั้ง ChromeDriver ให้ตรงกับเวอร์ชันของ Chrome อัตโนมัติ
    chromedriver_autoinstaller.install()

    driver = uc.Chrome(options=options)
    driver.set_window_size(600, 800)
    print_log("Starting the bot...")
    login(driver)
    status = True
    try:
        while status:
            # if selected == "push":
            #     start_comment_in_post(driver)
            # elif selected == 'post':
            start_post_in_group(driver)
            if config['repeat']:
                hour = int(config['hour'])
                minute = int(config['minute'])
                set_time = (hour * 60 + minute) * 60  # หน่วยเป็นวินาที
                print_log(f"Waiting for {hour} hours and {minute} minutes before starting the bot again...")
                time.sleep(set_time)

            else:
                print_log("Stopping the bot...")
                status = False
    except KeyboardInterrupt:
        print_log("\n🛑 Program stopped!")
        driver.quit()  # Close the browser

