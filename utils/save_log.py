import json
import os
from datetime import datetime
from urllib.parse import urlparse

from utils.print_log import print_log

LOG_PATH = "log.json"
DAILY_LIMIT = 30

def load_log(log_path=LOG_PATH):
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return json.load(f)
    return {}

def save_log(log, log_path=LOG_PATH):
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def get_today_key():
    return datetime.now().strftime("%Y-%m-%d")

def is_limit_reached():
    log = load_log()
    today = get_today_key()
    return len(log.get(today, [])) >= DAILY_LIMIT


def is_duplicate_across_days(log, link):
    for day_links in log.values():
        if link in day_links:
            return True
    return False

def save_link_log(link):
    log = load_log()
    today = get_today_key()

    if today not in log:
        log[today] = []

    if is_duplicate_across_days(log, link):
        print_log(f"ข้ามลิงก์นี้ (เคยบันทึกไว้ในวันก่อนๆ แล้ว): {link}")
        return False

    if not is_limit_reached():
        log[today].append(link)
        save_log(log)
        print_log(f"บันทึกลิงก์แล้ว: {link}")
        return True
    else:
        print_log(f"ถึงขีดจำกัด 20 ลิงก์แล้วสำหรับวันนี้: {link}")
        return False

def clean_facebook_link(link: str) -> str:
    parsed = urlparse(link)
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return clean_url
