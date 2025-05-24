import json
import os
from datetime import datetime
from urllib.parse import urlparse

from utils.print_log import print_log

LOG_PATH = "log.json"
DAILY_LIMIT = 20

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

def save_link_log(link):
    today = get_today_key()
    log = load_log()

    if today not in log:
        log[today] = []

    if link not in log[today] and not is_limit_reached():
        log[today].append(link)
        save_log(log)
        print_log(f"บันทึกลิงก์แล้ว: {link}")
        return True
    else:
        print_log(f"ข้ามลิงก์นี้ (อาจจะดูครบแล้วหรือซ้ำ): {link}")
        return False
    
def clean_facebook_link(link: str) -> str:
    parsed = urlparse(link)
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return clean_url