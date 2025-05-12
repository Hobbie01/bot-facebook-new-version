import pandas as pd # type: ignore

file_path = "setting.xlsx"
# อ่านไฟล์ Excel
def read_excel_file():
    return pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

# ฟังก์ชันสำหรับการอ่านข้อมูลจากชีท "ค้นหาและคอมเมนต์"
def read_search_and_comment_sheet():
    # อ่านเฉพาะชีท "ค้นหาและคอมเมนต์"
    df = pd.read_excel(file_path, sheet_name="ค้นหาและคอมเมนต์", engine="openpyxl")
    return df

# ฟังก์ชันสำหรับการอ่านข้อมูลจากชีท "คอมเมนต์ในกลุ่ม"
def read_comment_in_group_sheet():
    # อ่านเฉพาะชีท "คอมเมนต์ในกลุ่ม"
    df = pd.read_excel(file_path, sheet_name="คอมเมนต์ในกลุ่ม", engine="openpyxl")
    return df

# ฟังก์ชันสำหรับการอ่านข้อมูลจากชีท "คอมเมนต์ในโพสต์"
def read_comment_in_post_sheet():
    # อ่านเฉพาะชีท "คอมเมนต์ในโพสต์"
    df = pd.read_excel(file_path, sheet_name="คอมเมนต์ในโพสต์", engine="openpyxl")
    return df

# ฟังก์ชันสำหรับการอ่านข้อมูลจากชีท "โพสต์ในกลุ่ม"
def read_post_in_group_sheet():
    # อ่านเฉพาะชีท "โพสต์ในกลุ่ม"
    df = pd.read_excel(file_path, sheet_name="โพสต์ในกลุ่ม", engine="openpyxl")
    return df
