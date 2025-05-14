import webview
import json


def print_log(message):
    message_str = json.dumps(str(message))  # escape ให้ JS ใช้งานได้ปลอดภัย
    webview.windows[0].evaluate_js(f"addLog({message_str})")