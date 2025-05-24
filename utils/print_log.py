import webview
import json
import os


def print_log(message):
    message_str = json.dumps(str(message))  # escape ให้ JS ใช้งานได้ปลอดภัย
    webview.windows[0].evaluate_js(f"addLog({message_str})")
    # # Ensure the log file exists
    # log_file_path = "log_output.text"
    # if not os.path.exists(log_file_path):
    #     with open(log_file_path, "w") as log_file:
    #         pass  # Create the file if it doesn't exist

    # # Save the log message to the file
    # with open(log_file_path, "a") as log_file:
    #     log_file.write(f"{message}\n")

    # # Push the log message to a list for further processing
    # log_messages = getattr(print_log, "_log_messages", [])
    # log_messages.append(message)
    # setattr(print_log, "_log_messages", log_messages)