from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from services.login_facebook import login_cookies
from services.read_settings import read_json_by_type
from utils.commands.image import upload_image


import time
import pyperclip
import random
import math
import platform
from utils.print_log import print_log

is_mac = platform.system() == "Darwin"

# เลือก Key ตาม OS
key_cmd = Keys.COMMAND if is_mac else Keys.CONTROL
def start_post_in_group(driver):
   
        print_log("Post In Group...")
        data = read_json_by_type("post")
        for row in data:
            try:
                # print_log(row)
                link = row['group']
                comment = row['comment']
                image = row['image']
                cooikies = row['cookies']
                status_login = login_cookies(driver, cooikies)
                if not status_login:
                    continue
                driver.get(link)
                print_log(f"ไปที่กลุ่ม {link}")
                post = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe")]')
                )
        )
                # 
                # คลิกที่ span
                post.click()
                time.sleep(10)
                actions = ActionChains(driver)
                sub_lines = comment.split("\n")
                for sub_line in sub_lines:
                    actions.send_keys(sub_line)
                    actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                time.sleep(random.uniform(3, 10))  
                # ส่ง RETURN (Enter) และ ESCAPE เพื่อปิดช่องคอมเมนต์
                actions.send_keys(Keys.RETURN).perform()
                if not (isinstance(image, float) and math.isnan(image) or image == "-"):
                    image_files = image.replace(",", "\n")
                    try:
                            time.sleep(5)
                            upload_image(driver,image_files)
                    except Exception as e:
                            print_log(f"ไม่พบ input file ใน div นี้ {e}")
                # ✅ กดปุ่มโพสต์
                time.sleep(5)
                post_button = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @aria-label="โพสต์"]'))
                )
                post_button.click()
                time.sleep(20)
                print_log("Post success")

            except Exception as e:
                print_log(f"Error Something went wrong: {e}")
                continue
