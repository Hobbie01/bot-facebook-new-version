from bot import bot_start
from utils.convert_cookie import convert_cookie_string
from utils.print_log import print_log
import webview
import json
import platform
import subprocess
import hmac
import hashlib
import os
import sys
import shutil
from datetime import datetime
import base64

SECRET_KEY = "mysecretkey"  # Secret Key ที่ใช้ในการสร้าง HMAC
CODE_FILE = 'login_code.json'
CONFIG_FILE = 'user_config.json'
IMAGE_DIR = 'images'  # Directory to store uploaded images

# Create images directory if it doesn't exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # ใช้ตอนรันจาก pyinstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # ตอนรันจาก python ปกติ
    return os.path.join(base_path, relative_path)


# ----- Hardware ID -----
def get_hardware_id():
    system = platform.system().lower()
    if system == "windows":
        command = 'wmic baseboard get serialnumber'
        try:
            result = subprocess.check_output(command, shell=True).decode().strip()
            return result.split("\n")[1].strip() if result else "Not Available"
        except Exception:
            return "Not Available"
    elif system == "darwin":
        command = 'system_profiler SPHardwareDataType | grep "Hardware UUID"'
        try:
            result = subprocess.check_output(command, shell=True).decode().strip()
            return result.split(":")[1].strip() if result else "Not Available"
        except Exception:
            return "Not Available"
    return "Not Available"

# ----- Code Gen/Verify -----
def generate_code(hardware_id):
    if not hardware_id:
        raise ValueError("Hardware ID cannot be empty")
    secret_key_bytes = SECRET_KEY.encode()
    hardware_id_bytes = hardware_id.encode()
    hmac_object = hmac.new(secret_key_bytes, hardware_id_bytes, hashlib.sha256)
    generated_code = hmac_object.hexdigest()[:10]
    return generated_code

def verify_code(hardware_id, input_code):
    generated_code = generate_code(hardware_id)
    return generated_code == input_code

def save_code(code):
    try:
        with open(CODE_FILE, 'w') as f:
            json.dump({'code': code}, f)
    except Exception as e:
        print_log('Error saving code:', e)

def load_code():
    if not os.path.exists(CODE_FILE):
        return None
    try:
        with open(CODE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('code')
    except Exception as e:
        print_log('Error loading code:', e)
        return None
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print_log('Error loading config:', e)
        return []
    
class Api:
    def __init__(self):
        self.authenticated = True

    def start(self,config):
        print_log("✅ API has started")
        bot_start(config)
        

api = Api()



if __name__ == '__main__':

    page = 'index.html'

    webview.create_window(
        title="Bot Facebook",
        url=resource_path(f"html/{page}"),
        js_api=api,
        width=600,
        height=600,
        resizable=True,
    )
    webview.start()