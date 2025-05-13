import json
from typing import List, Dict
file_path = "configs.json"

def read_json_by_type( target_type: str) -> List[Dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # กรองตาม type ที่ต้องการ
        filtered_data = [item for item in data if item.get("type") == target_type]
        return filtered_data
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        return []

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    result = read_json_by_type("data.json", "post")
    print(json.dumps(result, indent=2, ensure_ascii=False))
