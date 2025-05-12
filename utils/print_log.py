import webview

def print_log(message):
    webview.windows[0].evaluate_js(f"addLog('{message}')")