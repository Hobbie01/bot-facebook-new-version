from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

from utils.commands.scroll import scroll
from utils.commands.is_displayed import is_displayed
from utils.commands.like import random_like
from services.excel import read_comment_in_group_sheet
from utils.commands.image import upload_image
from utils.print_log import print_log

import time
import re  
import math
import platform
import pyperclip
from utils.print_log import print_log

is_mac = platform.system() == "Darwin"

# เลือก Key ตาม OS
key_cmd = Keys.COMMAND if is_mac else Keys.CONTROL
def start_comment_in_group(driver,sort):
    try:
        print_log("comment in group...")
        df_comment_in_group = read_comment_in_group_sheet()
        print_log(df_comment_in_group)
        for _, row in df_comment_in_group.iterrows():
            link = row['ลิงค์กลุ่ม']
            comment = row['คอมเมนต์']
            image = row['รูปภาพ']
            min_comment = row['จำนวนคอมเมนต์']
            count = row['จำนวนครั้ง']
            time.sleep(5)
            if sort:
                driver.get(f"{link}/?sorting_setting=CHRONOLOGICAL")
            else:
                driver.get(link)  # ใส่ Group ID

            i = 0
            
            while i<=count:
                comment_buttons = driver.find_elements(
                By.CSS_SELECTOR, 
                '.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x1sur9pj.xkrqix3'
            )
                scroll(driver)
                time.sleep(1)
                # ตรวจสอบแต่ละปุ่มว่าแสดงผลอยู่หรือไม่
                for button in comment_buttons:
                    if is_displayed(driver, button):
                        random_like(driver)
                        text = button.text 
                        number_match = re.search(r'\d+', text)  
                        if number_match:
                            comment_count = int(number_match.group())  
                            if "แชร์" not in text and comment_count >= min_comment:
                                time.sleep(1)
                                button.click()
                                time.sleep(5)  
                                if not (isinstance(image, float) and math.isnan(image) or image == "-"):

                                    upload_image(driver,image) 
                                # ส่งข้อความคอมเมนต์
                                actions = ActionChains(driver)
                                pyperclip.copy(comment)
                                actions.key_down(key_cmd).send_keys("v").key_up(key_cmd).perform()
                                time.sleep(3)  # หน่วงเวลา 3 วินาที
                                
                                # ส่ง RETURN (Enter) และ ESCAPE เพื่อปิดช่องคอมเมนต์
                                actions.send_keys(Keys.RETURN).send_keys(Keys.ESCAPE).perform()
                                time.sleep(1)  
                                i+=1
                                break 
            
    except Exception as e:
        print_log(f"Error Something went wrong: {e}")
