from urllib.parse import parse_qs, urlparse
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from services.login_facebook import login_cookies
from services.read_settings import read_json_by_type
from utils.commands.image import upload_image


import time
import random
from utils.print_log import print_log


def start_comment_in_post(driver):
   
        print_log("Comment In Post...")
        data = read_json_by_type("comment")
        for row in data:
            try:
                link = row['post']
                comment = row['comment']
                image = row['image']
                cooikies = row['cookies']
                driver.get(link)
                print_log(f"ไปที่กลุ่ม {link}")
                status_login = login_cookies(driver, cooikies)
                if not status_login:
                    continue
    
                # input("Press Enter to continue...")
                # time.sleep(10)
                # driver.refresh()
                time.sleep(10)
                current_url = driver.current_url
                parsed_url = urlparse(current_url)
                query = parse_qs(parsed_url.query)
                comment_buttons = WebDriverWait(driver, 120).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//span[@data-ad-rendering-role="comment_button"]')
                )
        )
                # 
                # คลิกที่ span
                comment_buttons[0].click()
                if 'comment_id' in query:
                    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.F5)
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.F5)
                    print_log("Refresh page")
                    time.sleep(10)
                actions = ActionChains(driver)
                sub_lines = comment.split("\n")  
                for sub_line in sub_lines:
                    actions.send_keys(sub_line)
                    actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                time.sleep(random.uniform(3, 10))
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(10)
                upload_image(driver,image)
                print_log("comment success")
            except Exception as e:
                print_log(f"Error Something went wrong: {e}")
                continue
