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
        self.authenticated = False
        self.config_file = "configs.json"
        self.data = self._load()
        self.cookie = None
        self.secret = "your_secret_key"
        self.hardware_id = get_hardware_id()
        self.config = load_config()
        
    
    def check_login(self, code):
        ok = verify_code(self.hardware_id, code)
        if ok:
            save_code(code)
        return ok


    def _load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def save_config(self, item):
        self.data.append(item)
        self._save()
        webview.windows[0].evaluate_js(f"addLog('✅ Config saved: {json.dumps(item)}')")
        return True

    def get_all(self):
        return self.data

    def delete_config(self, id, type):
        webview.windows[0].evaluate_js(f"addLog('🗑️ Deleting config with id: {id} and type: {type}')")
        self.data = [
            item for item in self.data 
            if not (str(item.get("id")) == str(id) and str(item.get("type")) == str(type))
        ]
        self._save()
        webview.windows[0].evaluate_js(f"addLog('✅ Config with id: {id} and type: {type} deleted')")
    def get_hardware_id(self):
        return get_hardware_id()
    


    def start(self,selected,config):
        print_log("✅ API has started")
        bot_start(selected,config)
        
    def save_cookie(self, cookie):
        print_log("Saving cookie...")
        if cookie == '' and not os.path.exists('facebook_cookies.json'):
            webview.windows[0].evaluate_js("addLog('❌ No cookie provided')")
            return False
        cookies = convert_cookie_string(cookie)
        if cookies:  # Ensure cookies are valid before saving
            with open('facebook_cookies.json', 'w') as file:
                json.dump(cookies, file)
            webview.windows[0].evaluate_js("addLog('✅ Cookies have been saved!')")
            return True
        elif os.path.exists('facebook_cookies.json'):
            return True
        else:
            webview.windows[0].evaluate_js("addLog('❌ Invalid cookie format')")
            return False
   
    def upload_image(self, data):
        try:
            if not data or 'filename' not in data or 'data' not in data:
                print_log("Invalid image data received")
                raise ValueError("Invalid image data")

            filename = data['filename']
            base64_data = data['data']
            
            print_log(f"Received image: {filename}")

            # Generate unique filename using timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(filename)[1]
            new_filename = f"{timestamp}{file_ext}"
            
            # Full path where the image will be saved
            save_path = os.path.join(os.path.abspath(IMAGE_DIR), new_filename)
            print_log(f"Attempting to save image to: {save_path}")
            
            # Ensure the images directory exists
            if not os.path.exists(IMAGE_DIR):
                os.makedirs(IMAGE_DIR)
                print_log(f"Created images directory at: {os.path.abspath(IMAGE_DIR)}")
            
            # Decode and save the file
            try:
                image_data = base64.b64decode(base64_data)
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                print_log(f"Successfully wrote image to: {save_path}")
            except Exception as write_error:
                print_log(f"Error writing file: {str(write_error)}")
                raise
            
            # Verify the file was saved
            if not os.path.exists(save_path):
                print_log("File was not saved successfully")
                raise ValueError("Failed to save image file")
            
            # Return the absolute path using resource_path
            absolute_path = resource_path(os.path.join(IMAGE_DIR, new_filename))
            print_log(f"Image saved successfully. Absolute path: {absolute_path}")
            
            return {"path": absolute_path}
        except Exception as e:
            print_log(f"Error in upload_image: {str(e)}")
            return None

api = Api()



if __name__ == '__main__':
    hardware_id = get_hardware_id()
    saved_code = load_code()
    page = 'login.html'

    if saved_code and verify_code(hardware_id, saved_code):
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