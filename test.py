import requests

url = "https://n8n.xn--12cmi3bhufp3kwcifc4hsgtdec.com/webhook-test/2589ac8f-7edb-4816-a560-4349f8d954e1"

payload = {
    "message": """เพราะเราเชื่อว่า ทีวี...ต้องเป็นได้มากกว่าทีวีที่คุณเคยรู้จัก‼️
ทีวี AI ตัวจริงจาก Samsung ✨ ครั้งแรกของทีวี! ที่คิดมาเพื่อตอบโจทย์ทุกโมเมนต์ของคุณ
.
ด้วย Samsung Vision AI เทคโนโลยีใหม่ล่าสุด! ที่พร้อมอัปทั้งภาพ เสียง และประสบการณ์ต่างๆ อย่างที่คุณไม่เคยเจอมาก่อน
.
📌 ให้ AI ในทีวี อัปความสนุกทุกปาร์ตี้ 🥳🎉 เปลี่ยน Wallpaper ในจอได้ตามมู้ดที่คุณชอบ
📌 ไม่ทำให้โมเมนต์หน้าทีวีของคุณต้องสะดุด จะมือเลอะ หารีโมตไม่เจอ แค่ขยับมือไปมาก็ควบคุมทีวีได้
📌 และสิ่งสำคัญที่สุดของ AI คือการอัปภาพความทรงจำ ไม่ว่าจะเก่าแค่ไหน...ให้กลับมาคมชัดอีกครั้ง สูงสุดถึง 8K
.
สัมผัสประสบการณ์อีกมากมาย ที่คิดมาเพื่อทุกรายละเอียดของคุณ และคนที่คุณรัก (รวมถึงน้อนๆ 🐶🐱 ด้วย ) เพื่อให้คุณ...เป็นคุณได้สุดกับทีวี AI ตัวจริง
สนใจรายละเอียดเพิ่มเติม คลิกที่นี่เลย 👉🏻 https://bit.ly/4kjsj9E
#เป็นคุณได้สุดกับทีวีAIตัวจริง​ #SamsungVisionAI #LiveANewDay #Samsung""",
    "link": "https://bit.ly/4kjsj9E"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
