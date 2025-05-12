
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore

from utils.commands.is_displayed import is_displayed
from utils.print_log import print_log

import time
import random
def like(driver):
    try:
        like_buttons = driver.find_elements(By.XPATH, '//span[@data-ad-rendering-role="ถูกใจ_button" and not(@style)]')
        for button in like_buttons:
                if is_displayed(driver, button):
                    button.click()
                    time.sleep(1)
                    print_log("Like Success")
                    break  
    except:
        print_log("Like False")
        
def random_like(driver):
    if random.random() < 0.3:  # 30% โอกาสที่จะเรียก like()
        like(driver)
        