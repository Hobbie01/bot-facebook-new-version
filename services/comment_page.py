import re
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from services.login_facebook import login, login_cookies
from services.read_settings import read_json_by_type
from utils.commands.image import upload_image


import time

from utils.print_log import print_log

def start_comment_in_page(driver):
        print_log("Comment In Page...")
        data = read_json_by_type("comment_page")
        for row in data:
                link_page = row['group']
                comment = row['comment']
                image = row['image']
                driver.get(link_page)
                login(driver)
                post = WebDriverWait(driver, 120).until(
                        EC.presence_of_element_located(
                        (By.XPATH, '//div[contains(@class, "html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1q0g3np")]')
                        ))
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post)
                time.sleep(5)
                link_element = post.find_element(By.XPATH, './/a[contains(@href, "/posts/")]')
                link = link_element.get_attribute('href')
                print_log(link)
                # เดินย้อนขึ้นไป 4 tag
                container = post.find_element(
        By.XPATH,
        'ancestor::div[contains(@class, "html-div") and contains(@class, "xdj266r") and contains(@class, "x11i5rnm") and contains(@class, "xkhd6sd")]'
        )

                # พยายามหาปุ่ม "ดูเพิ่มเติม"
                try:
                        see_more_button = container.find_element(By.XPATH,
                                'descendant::div[@role="button" and text()="ดูเพิ่มเติม"]'
                        )
                        see_more_button.click()
                        time.sleep(1)
                        print_log("คลิกปุ่มดูเพิ่มเติม")
                except:
                        print_log("ไม่มีปุ่มดูเพิ่มเติม")

                # หา div ที่มีข้อความโพสต์
                try:
                # สมมุติว่า keyword_condition ถูกสร้างมาแล้ว
                        keywords = ["Smart Service", "SmartThings","Samsung"]
                        keywords_condition = " or ".join([f'contains(string(.), "{kw}")' for kw in keywords])
                        message_text = container.find_element(
                        By.XPATH,
                        f'.//div[{keywords_condition}]'
                        )
                        text = message_text.text
                        clean_text = re.sub(r"ตัวบ่งชี้สถานะออนไลน์.*?·\n?", "", text, flags=re.DOTALL)
                        clean_text = clean_text.split("ความรู้สึกทั้งหมด")[0]
                        matched_keywords = [kw for kw in keywords if kw in clean_text]
                        print(clean_text)
                        print_log(f"ข้อความ: {clean_text}")
                        print_log(f"พบ keyword: {matched_keywords}")
                        print_log(f"link: {link}")
                except:
                        print_log("ไม่เจอข้อความโพสต์ตาม key ที่ระบุ")


