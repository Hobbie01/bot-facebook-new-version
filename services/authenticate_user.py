import hashlib
import uuid

def get_hardware_id():
    """ สร้าง Hardware ID ตามเครื่องของผู้ใช้ """
    return hashlib.sha256(uuid.getnode().to_bytes(6, 'big')).hexdigest()

