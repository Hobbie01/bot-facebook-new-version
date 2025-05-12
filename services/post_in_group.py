from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from utils.commands.image import upload_image

from services.excel import read_post_in_group_sheet

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
    try:
        print_log("Post In Group...")
        df_comment_in_group = read_post_in_group_sheet()
        print_log(len(df_comment_in_group))
        for _, row in df_comment_in_group.iterrows():
            link = row['ลิงค์กลุ่ม']
            comment = row['คอมเมนต์']
            image = row['รูปภาพ']
            driver.get(link)
            post = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "x1i10hfl x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xmjcpbm x107yiy2 xv8uw2v x1tfwpuw x2g32xy x78zum5 x1q0g3np x1iyjqo2 x1nhvcw1 x1n2onr6 xt7dq6l x1ba4aug x1y1aw1k xn6708d xwib8y2 x1ye3gou")]')
            )
        )
            # 
            # คลิกที่ span
            post.click()
            time.sleep(5)
            actions = ActionChains(driver)
            pyperclip.copy(comment)
            actions.key_down(key_cmd).send_keys("v").key_up(key_cmd).perform()
            time.sleep(random.uniform(3, 10))  
            actions.send_keys(Keys.RETURN).perform()
            image_buttons = WebDriverWait(driver, 100).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//div[contains(@class, "x6s0dn4") and contains(@class, "x78zum5") and contains(@class, "xl56j7k") and contains(@class, "x1n2onr6") and contains(@class, "x5yr21d") and contains(@class, "xh8yej3")]')
    )
)

            if image_buttons:
                image_buttons[1].click()
            if not (isinstance(image, float) and math.isnan(image) or image == "-"):
                image_files = image.replace(",", "\n")
                try:
                        time.sleep(5)
                        upload_image(driver,image_files)
                except Exception as e:
                        print_log(f"ไม่พบ input file ใน div นี้ {e}")
                # upload_image(image_files)
            # ✅ กดปุ่มโพสต์
            post_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @aria-label="โพสต์"]'))
            )
            post_button.click()
            print_log("Post success")

    except Exception as e:
        print_log(f"Error Something went wrong: {e}")
