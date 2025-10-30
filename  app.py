from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Secure API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

MEDICAL_DISCLAIMER = """
⚠️ **ข้อควรระวังทางการแพทย์**: นี่เป็นเพียงคำแนะนำเบื้องต้นเท่านั้น 
หากมีอาการรุนแรง เช่น เจ็บหน้าอก หายใจลำบาก มีเลือดออกมาก ควรไปพบแพทย์ทันที
🚨 เบอร์ติดต่อฉุกเฉิน: 1669 (EMS ประเทศไทย)
"""

def call_gemini_api(user_text):
    try:
        medical_prompt = f"""
        คุณเป็นผู้ช่วยทางการแพทย์ที่ให้คำแนะนำเบื้องต้นเกี่ยวกับอาการป่วยทั่วไป
        
        กฎ:
        1. ให้คำแนะนำสุขภาพทั่วไปและข้อมูลเกี่ยวกับโรงพยาบาลเท่านั้น
        2. ไม่อนุญาตให้วินิจฉัยโรคหรือแนะนำยารักษาโรค
        3. หากอาการรุนแรง ให้แนะนำให้ไปพบแพทย์
        4. ตอบเป็นภาษาไทยแบบเป็นมิตร
        
        ข้อความจากผู้ใช้: {user_text}
        
        คำตอบ:
        """
        
        response = model.generate_content(medical_prompt)
        return f"{response.text}\n\n{MEDICAL_DISCLAIMER}"
    except Exception as e:
        return f"ขออภัย เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}"

@app.route("/api/chat", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        user_text = data.get("message", "").strip()
        
        if not user_text:
            return jsonify({"error": "ไม่มีข้อความ"}), 400
        
        # Basic symptom analysis
        emergency_keywords = ['เจ็บหน้าอก', 'หายใจไม่ออก', 'หมดสติ', 'เลือดออกมาก', 'หัวใจ']
        if any(keyword in user_text for keyword in emergency_keywords):
            return jsonify({
                "response": f"🚨 **กรณีฉุกเฉิน**: อาการดังกล่าวอาจรุนแรง กรุณาติดต่อหน่วยแพทย์ฉุกเฉิน 1669 ทันที\n\n{MEDICAL_DISCLAIMER}",
                "emergency": True
            })
        
        reply = call_gemini_api(user_text)
        return jsonify({"response": reply, "emergency": False})
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")