from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from utils.print_log import print_log

from services.excel import read_comment_in_post_sheet

import time
import math  
import platform
import pyperclip

is_mac = platform.system() == "Darwin"

# เลือก Key ตาม OS
key_cmd = Keys.COMMAND if is_mac else Keys.CONTROL
def start_comment_in_post(driver):
    try:
        print_log("คอมเมนต์ในกลุ่ม...")
        df_comment_in_group = read_comment_in_post_sheet()
        print_log(df_comment_in_group)
        for _, row in df_comment_in_group.iterrows():
            link = row['ลิงค์โพสต์']
            comment = row['คอมเมนต์']
            image = row['รูปภาพ']
            time.sleep(5)
            driver.get(link)
            comment_box = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
                    )
            comment_box.click()                    
            if not (isinstance(image, float) and math.isnan(image) or image == "-"):
                file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
                file_input.send_keys(image)
                time.sleep(10)
                # ใช้ ActionChains เพื่อพิมพ์ข้อความและส่ง
            actions = ActionChains(driver)
            pyperclip.copy(comment)
            actions.key_down(key_cmd).send_keys("v").key_up(key_cmd).perform()
            time.sleep(1)
            actions.send_keys(Keys.RETURN).perform()
            time.sleep(5)

            
    except Exception as e:
        print_log(f"Error Something went wrong: {e}")
