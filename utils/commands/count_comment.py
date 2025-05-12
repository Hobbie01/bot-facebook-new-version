from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore

from utils.commands.is_displayed import is_displayed
from utils.commands.scroll import scroll
import time
import random

def count_comment(driver,min_comment):
    comment_buttons = driver.find_elements(
        By.CSS_SELECTOR, 
        '.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs.x1sur9pj.xkrqix3'
    )
    scroll(driver)
    # ตรวจสอบแต่ละปุ่มว่าแสดงผลอยู่หรือไม่
    for button in comment_buttons:
        if is_displayed(driver, button):
            text = button.text 
            parts = text.split(' ') 
            if int(parts[0]) >= min_comment and parts[1] == 'ความคิดเห็น':
                return button
            