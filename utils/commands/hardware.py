import subprocess
import platform
import hashlib
import hmac

# ฟังก์ชันดึง Hardware ID
def get_hardware_id():
    """ดึง Hardware ID ขึ้นอยู่กับระบบปฏิบัติการ"""
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



SECRET_KEY = "mysecretkey"  # Secret Key ที่ใช้ในการสร้าง HMAC

# ฟังก์ชันสำหรับการสร้างรหัสจาก Hardware ID
def generate_code(hardware_id):
    if not hardware_id:
        raise ValueError("Hardware ID cannot be empty")
    
    # ใช้ HMAC เพื่อสร้างรหัส
    secret_key_bytes = SECRET_KEY.encode()  # แปลง secret key ให้เป็น bytes
    hardware_id_bytes = hardware_id.encode()  # แปลง Hardware ID ให้เป็น bytes
    hmac_object = hmac.new(secret_key_bytes, hardware_id_bytes, hashlib.sha256)  # ใช้ HMAC กับ SHA256
    generated_code = hmac_object.hexdigest()[:10]  # เอาแค่ 10 ตัวแรกจากผลลัพธ์ของ HMAC
    return generated_code

# ฟังก์ชันสำหรับตรวจสอบรหัส
def verify_code(hardware_id, input_code):
    # สร้างรหัสจาก Hardware ID ที่ให้มา
    generated_code = generate_code(hardware_id)
    
    # เปรียบเทียบรหัสที่ได้รับกับรหัสที่สร้างขึ้น
    if generated_code == input_code:
        return True  # รหัสถูกต้อง
    else:
        return False  # รหัสไม่ถูกต้อง