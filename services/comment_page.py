import hashlib
import re
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from services.login_facebook import login
from services.read_settings import read_json_by_type
from utils.commands.image import upload_image


import time

from utils.commands.scroll import scroll, scroll_post
from utils.print_log import print_log
from utils.save_log import clean_facebook_link, is_limit_reached, save_link_log


def start_comment_in_page(driver, config=None):
    try:
        seen_posts = set()
        print_log("Comment In Page...")
        data = read_json_by_type("comment")
        daily_limit = config.get('dailyLimit', 30) if config else 30

        for row in data:
            if is_limit_reached(daily_limit):
                print_log(f"ถึงขีดจำกัด {daily_limit} ครั้งต่อวันแล้ว")
                break
            i = 0
            link_page = row["link"]
            count = row["count"]
            contents = row["content"]  # array ของ {keyword, comment}
            if not login(driver):
                print_log("เข้าสู่ระบบไม่สำเร็จ")
                return 
            driver.get(link_page)
            # input("กด Enter เพื่อเริ่มการคอมเมนต์ในเพจ...")
            while i < count:
                scroll(driver)
                time.sleep(5)  # รอให้โหลดข้อมูลเพิ่ม
                try:
                    posts = WebDriverWait(driver, 60).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, '//*[contains(@class, "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa x1yc453h")]')
                            )
                        )
                    for _, post in enumerate(posts):
                        if i >= count:
                            break
                        link_element = post.find_element(By.XPATH, './/a')
                        link = clean_facebook_link(link_element.get_attribute('href'))
                        link_hash = hashlib.sha256(link.encode('utf-8')).hexdigest()
                        if link_hash in seen_posts:
                            continue  # ข้ามโพสต์นี้ไป
                        seen_posts.add(link_hash)
                        i += 1
                        print_log(f"กำลังอ่านโพสต์ที่ {i} จาก {count}")
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post)
                        time.sleep(3)

                        container = post.find_element(
                            By.XPATH,
                            'ancestor::div[contains(@class, "html-div") and contains(@class, "xdj266r") and contains(@class, "x11i5rnm") and contains(@class, "xkhd6sd")]'
                        )

                        try:
                            see_more_button = container.find_element(By.XPATH,
                                'descendant::div[@role="button" and text()="ดูเพิ่มเติม"]'
                            )
                            driver.execute_script("arguments[0].click();", see_more_button)
                            time.sleep(1)
                        except:
                            pass

                        text = container.text
                        clean_text = re.sub(r"ตัวบ่งชี้สถานะออนไลน์.*?·\n?", "", text, flags=re.DOTALL)
                        clean_text = clean_text.split("ความรู้สึกทั้งหมด")[0]
                        if not clean_text.strip():
                            print_log("ไม่เจอข้อความโพสต์")
                            continue
                        print_log(f"ข้อความโพสต์: {clean_text}")
                        for content in contents:
                            keyword = content["keyword"]
                            comment = content["comment"]
                            image = content["imagePath"]
                            # print_log(f"กำลังตรวจสอบ keyword: '{keyword}'")
                            if keyword in clean_text:
                                try:
                                    
                                    if not save_link_log(link, daily_limit):
                                        continue
                                    print_log(f"ข้อความโพสต์: {clean_text}")
                                    print_log(f"เจอ keyword: '{keyword}' ในโพสต์")
                                    print_log(f"link: {link}")
                                    print_log(f"คอมเมนต์: {comment}")

                                    # คลิกปุ่มคอมเมนต์
                                    comment_button = container.find_element(By.XPATH, './/span[@data-ad-rendering-role="comment_button"]')
                                    # comment_button.click()
                                    driver.execute_script("arguments[0].click();", comment_button)

                                    time.sleep(2)
                                    comment_boxs = WebDriverWait(driver, 20).until(
                                                EC.presence_of_all_elements_located((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
                                            )
                                    comment_boxs[-1].click()   
                                    time.sleep(3)
                                    actions = ActionChains(driver)
                                    print_log("กำลังพิมพ์คอมเมนต์...")
                                    if image and image.strip():
                                                    upload_image(driver, image)
                                    sub_lines = comment.split("\n")
                                    for sub_line in sub_lines:
                                            actions.send_keys(sub_line).perform()
                                            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                                    time.sleep(1)
                                    actions.send_keys(Keys.RETURN).perform()
                                    print_log("ส่งคอมเมนต์เรียบร้อยแล้ว")
                                    time.sleep(10)
                                    actions.send_keys(Keys.ESCAPE).perform()  # ปิดกล่องคอมเมนต์

                                except Exception as e:
                                    print_log(f"คอมเมนต์ไม่สำเร็จ: {e}")
                                break  # เจอ keyword แล้ว ไม่ต้องวนเช็ค keyword ถัดไป
                        else:
                            print_log("ไม่พบ keyword ที่ต้องการในโพสต์นี้")  
                except:
                     continue
    except Exception as e:
        print_log(f"เกิดข้อผิดพลาด: {e}")
    finally:
        print_log("จบการทำงานของฟังก์ชัน คอมเมนต์ในเพจ")