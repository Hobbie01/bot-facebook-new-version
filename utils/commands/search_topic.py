from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time
from utils.print_log import print_log

def search_topic(driver, keyword):
        # รอจนกว่า input ค้นหาจะโหลด
        driver.get("https://www.facebook.com/")
        time.sleep(5)
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@aria-label="ค้นหาบน Facebook"]'))
        )
        # เคลียร์ข้อความเดิมใน input และพิมพ์ keyword
        search_box.clear()
        search_box.send_keys(keyword)
        print_log(f"ทำการค้นหา {keyword}")
        time.sleep(1)  # รอ 1 วินาที
        search_box.send_keys(Keys.RETURN)
        
        # รอจนกว่าจะเจอโพสต์
        post_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "x1qjc9v5")]/descendant::span[text()="โพสต์"]')
            )
        )
        # คลิกที่โพสต์
        post_div.click()
        print_log("เลือกหัวข้อเป็นโพสต์")
        time.sleep(5)  # รอ 5 วินาที