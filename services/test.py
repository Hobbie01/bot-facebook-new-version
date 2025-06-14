import hashlib
import re
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore



import time

from utils.print_log import print_log

def chat_bot(driver):
    try:
        print_log("Starting Chat Bot")
        driver.get('https://business.facebook.com/latest/inbox/')
        messager = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[contains(@aria-label, "Messenger")]')
                ))
        driver.execute_script("arguments[0].click();", messager)
        time.sleep(5)
        dont_read = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@aria-label, "ยังไม่ได้อ่าน")]')
                ))
        driver.execute_script("arguments[0].click();", dont_read)
        while True:
            message = WebDriverWait(driver, 3600).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "_a6ag _a6ah clearfix _ikh")]')
                ))
            driver.execute_script("arguments[0].click();", message)
            send_boxs = driver.find_elements(By.XPATH, '//div[contains(@class, "xuk3077 x78zum5 xdt5ytf x2lwn1j xeuugli xdl72j9 x1c4vz4f x2lah0s x16fdfms x161msgk x1s9ed0f x1eapu41 x1r944mn")]')
            print(len(send_boxs))
            if(len(send_boxs)>1):
                continue
            chat_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//textarea[@placeholder="ตอบกลับใน Messenger..."]')
    )
)

            text = "สวัสดีครับ หมายเลข 0001"

            # Inject แบบ native React-compatible
            driver.execute_script("""
                const textarea = arguments[0];
                const text = arguments[1];

                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                ).set;

                nativeInputValueSetter.call(textarea, text);
                
                const ev = new Event('input', { bubbles: true });
                textarea.dispatchEvent(ev);
            """, chat_box, text)

            # Enter
            driver.execute_script("""
                arguments[0].dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter', keyCode: 13, which: 13, bubbles: true
                }));
            """, chat_box)
            # input('asdasd')
    except Exception as e:
        print_log(f"เกิดข้อผิดพลาด: {e}")
    finally:
        print_log("จบการทำงานของฟังก์ชัน คอมเมนต์ในเพจ")