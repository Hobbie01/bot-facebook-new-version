import jwt
from jwt.exceptions import InvalidTokenError
import subprocess
import platform

def  check_token(token, secret_key):
    try:
        # Decode and verify the JWT token
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token  # Return the decoded payload
    except InvalidTokenError:
        return {"error": "Invalid token"}
    
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