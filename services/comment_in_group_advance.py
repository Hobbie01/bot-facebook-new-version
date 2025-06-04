from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore

from services.excel import read_comment_in_group_advance_sheet
from utils.commands.image import upload_image
from utils.commands.scroll import scroll_post
import time
import hashlib
import random



seen_posts = set()

def start_comment_in_group_advance(driver):
    try:
        print("Commenting in the group...")
        data = read_json_by_type("comment")
        for _, row in data:
            link = row['ลิงค์กลุ่ม']
            comment = row['คอมเมนต์']
            image = row['รูปภาพ']
            count = row['จำนวนครั้งในการหาโพสต์']
            text_keywords = row['คำที่ต้องกาาค้นหา']
            text_exclude_keywords = row['คำที่ไม่ต้องการ']
            keywords = text_keywords.split(',')
            exclude_keywords =  text_exclude_keywords.split(',')

            
            driver.get(f"{link}/?sorting_setting=CHRONOLOGICAL")
            time.sleep(10)

            
            for _ in range(int(count)):
                scroll_post(driver)
                time.sleep(5)  # รอให้โหลดข้อมูลเพิ่ม

                # สร้างเงื่อนไขสำหรับ keywords
                # กำหนดพื้นที่ค้นหาเฉพาะ div ที่เป็นโพสต์
                # กำหนดพื้นที่ค้นหาโพสต์ (รวม 2 เงื่อนไข)
                base_xpath = (
                    '//div[contains(@data-ad-comet-preview, "message")] '
                    '| '
                    '//div[contains(@class, "x6s0dn4") and contains(@class, "x78zum5") and contains(@class, "xdt5ytf") and contains(@class, "x5yr21d") and contains(@class, "xl56j7k") and contains(@class, "x10l6tqk") and contains(@class, "x17qophe") and contains(@class, "x13vifvy") and contains(@class, "xh8yej3")]'
                    '| '
                    '//div[contains(@class,"x6s0dn4 x78zum5 xdt5ytf x1a7vs8u xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3")]'
                )

                # ค้นหาเฉพาะโพสต์ที่มีคำที่ต้องการ
                keywords_condition = " or ".join([f'contains(string(.), "{kw}")' for kw in keywords])

                # กรองโพสต์ที่มีคำที่ไม่ต้องการ
                exclude_condition = " and ".join([f'not(contains(string(.), "{kw}"))' for kw in exclude_keywords])

                # ไม่เอาโพสต์ที่มี emoji
                exclude_icons = "not(descendant::img[contains(@src, 'emoji.php')])"

                # ไม่เอาโพสต์ที่มีปุ่ม "ดูเพิ่มเติม"
                exclude_view_more = 'not(descendant::div[@role="button" and text()="ดูเพิ่มเติม"])'

                # ไม่เอาโพสต์ที่มีลิงก์ https:// 
                exclude_https = "not(contains(string(.), 'https://'))"

                # ไม่เอาโพสต์ที่อยู่ภายใต้ div[@class='html-div x11i5rnm xat24cr ...']
                exclude_under_html_div = "not(ancestor::div[@class='html-div x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1y332i5'])"

                # รวม XPath ทุกเงื่อนไขเข้ากับพื้นที่เป้าหมาย
                xpath_query = f"({base_xpath})[({keywords_condition}) and ({exclude_condition}) and ({exclude_icons}) and ({exclude_view_more}) and ({exclude_https}) and ({exclude_under_html_div})]"

                # print(xpath_query)

                # ค้นหาโพสต์ที่ตรงตามเงื่อนไข
                posts = driver.find_elements(By.XPATH, xpath_query)
                # แสดงผลโพสต์ที่เจอและเลื่อนหน้าจอไปยังตำแหน่งโพสต์
                for post in posts:
                    if not post.text.strip():
                            continue  # ข้ามโพสต์นี้ไป
                    post_hash = hashlib.sha256(post.text.encode('utf-8')).hexdigest()

                        # ถ้าโพสต์นี้เคยเจอมาก่อนแล้ว (เช็คจาก hash)
                    if post_hash in seen_posts:
                        continue  # ข้ามโพสต์นี้ไป
                    try :
                        contain = post.find_element(By.XPATH, 'ancestor::div[@role="article" and @class="x1a2a7pz"]')
                        aria_describedby = contain.get_attribute("aria-describedby")
                        print(f"Find Post aria-describedby: {aria_describedby}")  
                    except Exception as e:
                        print(f"Cant find aria-describedby")
                        continue                  

                    try:
                        # ค้นหาภาพ
                        driver.find_element(By.XPATH, f"//div[contains(normalize-space(@aria-describedby), '{aria_describedby}')]//div[contains(@class, 'x6s0dn4 x1jx94hy x78zum5 xdt5ytf x6ikm8r x10wlt62 x1n2onr6 xh8yej3')]")
                        continue
                    except Exception as e: 
                        pass

                    try:
                        driver.find_element(By.XPATH, f"//div[contains(normalize-space(@aria-describedby), '{aria_describedby}')]//div[@class='html-div x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1y332i5']")
                        continue
                    except Exception as e: 
                        pass

                    # เพิ่ม hash ของโพสต์ลงในเซต
                    seen_posts.add(post_hash)
                    # แสดงข้อความโพสต์
                    y_offset = post.location["y"] - 100  # ขยับขึ้นไปอีก 100px เพื่อให้เห็นโพสต์ชัดขึ้น
                    driver.execute_script(f"window.scrollTo(0, {y_offset});")
                    time.sleep(5)
                    try:

                        comment_button = driver.find_element(By.XPATH, f'//div[contains(normalize-space(@aria-describedby), "{aria_describedby}")]//span[@data-ad-rendering-role="comment_button"]')
                        time.sleep(1)
                        
                        comment_button.click()

                        time.sleep(10)


                        actions = ActionChains(driver)
                        time.sleep(10)
                        sub_images = image.split("||")
                        
                        lines = comment.split("||")
                        for i,line in enumerate(lines):
                            if i < len(sub_images):
                                upload_image(driver,sub_images[i])
                            sub_lines = line.split("\n")
                            for sub_line in sub_lines:
                                actions.send_keys(sub_line)
                                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                            time.sleep(random.uniform(3, 10))  
                            # ส่ง RETURN (Enter) และ ESCAPE เพื่อปิดช่องคอมเมนต์
                            actions.send_keys(Keys.RETURN).perform()
                        print("comment success")
                        time.sleep(random.uniform(3, 10))  
                        actions.send_keys(Keys.ESCAPE).perform()
                        break
                    except Exception as e:
                        print(f"Could not find the 'Comment' button or unable to click: {e}")
                    sleep_time = random.uniform(1, 10)
                    time.sleep(sleep_time)  # รอเวลาที่สุ่ม

            time.sleep(5)

    except Exception as e:
        print(f"Error occurred: {e}")
