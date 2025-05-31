from selenium.webdriver.common.by import By # type: ignore
from utils.print_log import print_log

import time
def upload_image(driver,image):
    try:
        print_log('Uploading...')
        file_inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')
        file_input = file_inputs[-1]
        file_input.send_keys(image)
        time.sleep(20)
        print_log("Upload image success")
    except:
        print_log("upload image fail")