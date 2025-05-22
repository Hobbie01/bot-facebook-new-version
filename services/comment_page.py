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
from utils.save_log import clean_facebook_link, is_limit_reached, save_link_log

def start_comment_in_page(driver):
    print_log("Comment In Page...")
    data = read_json_by_type("comment")

    for row in data:
        if is_limit_reached():
            print_log("ถึงขีดจำกัดการบันทึกในวันนี้แล้ว")
            break

        link_page = row["link"]
        count = row["count"]
        contents = row["content"]  # array ของ {keyword, comment}
        driver.get(link_page)
        if not login(driver):
            print_log("เข้าสู่ระบบไม่สำเร็จ")
            return 

        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        print_log("ทำการโหลดหน้าเพจ สำเร็จ")

        posts = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@class, "html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1q0g3np")]')
            )
        )

        for i, post in enumerate(posts):
            if i >= count:
                break

            print_log(f"กำลังอ่านโพสต์ที่ {i+1} จาก {count}")
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
                see_more_button.click()
                time.sleep(1)
            except:
                pass

            text = container.text
            if not text.strip():
                print_log("ไม่เจอข้อความโพสต์")
                continue

            for content in contents:
                keyword = content["keyword"]
                comment = content["comment"]
                image = content["imagePath"]
                if keyword in text:
                    try:
                        link_element = post.find_element(By.XPATH, './/a')
                        link = clean_facebook_link(link_element.get_attribute('href'))
                        if not save_link_log(link):
                            print_log(f"โพสต์นี้เคยคอมเมนต์แล้ว: {link}")
                            continue

                        print_log(f"เจอ keyword: '{keyword}' ในโพสต์")
                        print_log(f"link: {link}")
                        print_log(f"คอมเมนต์: {comment}")

                        # คลิกปุ่มคอมเมนต์
                        comment_button = container.find_element(By.XPATH, './/span[@data-ad-rendering-role="comment_button"]')
                        comment_button.click()
                        time.sleep(2)

                        actions = ActionChains(driver)
                        print_log("กำลังพิมพ์คอมเมนต์...")
                        upload_image(driver,image)
                        sub_lines = comment.split("\n")
                        for sub_line in sub_lines:
                                actions.send_keys(sub_line).perform()
                                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                        time.sleep(1)
                        input("กด Enter เพื่อส่งคอมเมนต์...")
                        actions.send_keys(Keys.RETURN).perform()
                        print_log("ส่งคอมเมนต์เรียบร้อยแล้ว")
                        time.sleep(10)
                        actions.send_keys(Keys.ESCAPE).perform()  # ปิดกล่องคอมเมนต์

                    except Exception as e:
                        print_log(f"คอมเมนต์ไม่สำเร็จ: {e}")
                    break  # เจอ keyword แล้ว ไม่ต้องวนเช็ค keyword ถัดไป
            else:
                print_log("ไม่พบ keyword ที่ต้องการในโพสต์นี้")

