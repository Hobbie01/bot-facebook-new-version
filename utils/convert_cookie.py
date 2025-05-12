import json
from datetime import datetime

def convert_cookie_string(cookie_string):
    cookies = []
    # แยกแต่ละ cookie ตามเครื่องหมาย semicolon (;) แล้วลบช่องว่าง
    cookie_list = cookie_string.split(';')
    
    for cookie in cookie_list:
        cookie = cookie.strip()
        if '=' in cookie:
            name, value = cookie.split('=', 1)  # แยกชื่อกับค่า

            # ตรวจสอบถ้ามีเครื่องหมาย '|' ในชื่อ cookie
            if '|' in name:
                name = name.split('|')[-1]  # ตัดเอาค่าหลังสุดจากชื่อ cookie
            
            cookie_dict = {
                'name': name,
                'value': value,
                'domain': '.facebook.com',  # กำหนด domain เป็น facebook
                'path': '/',                # ใช้ path '/' ของ Facebook
                'secure': True,             # กำหนดว่า cookie นี้ต้องใช้ https
                'httpOnly': True            # กำหนดว่า cookie นี้ไม่สามารถเข้าถึงได้จาก JavaScript
            }
            cookies.append(cookie_dict)
    
    return cookies