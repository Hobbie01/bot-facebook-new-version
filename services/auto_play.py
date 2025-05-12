from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from utils.print_log import print_log

from utils.commands.scroll import scroll
from utils.commands.like import random_like


import time
import random

def auto(driver,time_count):
        print_log("auto playing...")
        driver.get("https://www.facebook.com/")
        start_time = time.time()  # เวลาที่เริ่มต้น
        time_limit = 60*time_count  # 1 นาที (60 วินาที)
        vdo = False
        while (time.time() - start_time) < time_limit:
            scroll(driver)
            if vdo: 
                sleep_time = random.randint(1, 30)
            else:
                sleep_time = random.randint(1, 5)

            time.sleep(sleep_time)
            random_like(driver)
            if random.random() < 0.05:
                driver.get("https://www.facebook.com/")
                vdo = False
            if random.random() < 0.05:
                driver.get("https://www.facebook.com/watch/?ref=tab")
                vdo = True
            if random.random()< 0.05:
                driver.get("https://www.google.com")
                time.sleep(random.uniform(60, 300))
            if random.random()< 0.05:
                time.sleep(random.uniform(60, 300))
                