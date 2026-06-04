import streamlit as str_layout
import google.generativeai as genai
from pathlib import Path

# 1. ตั้งค่าหน้าแอปพลิเคชัน (Page Configuration)
str_layout.set_page_config(
    page_title="คลังสมองกฎหมาย อัจฉริยะ", 
    page_icon="🔮", 
    layout="wide"
)

# 2. ดึงรหัส API Key จากตู้เซฟหลังบ้าน Streamlit Cloud
try:
    genai.configure(api_key=str_layout.secrets["GUIDE_API_KEY"] if "GUIDE_API_KEY" in str_layout.secrets else str_layout.secrets["GEMINI_API_KEY"])
except Exception:
    pass

# 3. ส่วนหัวของหน้าเว็บ
str_layout.title("🔮 ระบบวิเคราะห์กลยุทธ์คดีความและคลังสมองกฎหมาย")
str_layout.write("ระบบพร้อมรันสูตรคดีและดึงข้อมูลจากคลังความรู้ 02_Knowledge แล้วเจ้าค่ะ")

str_layout.markdown("---")

# 🌟 4. เสกกล่องเลือกสถานะผู้ใช้งาน 3 ระดับที่คุณพี่ออกแบบ!
user_role = str_layout.selectbox(
    "กรุณาเลือกสถานะของผู้ใช้งาน เพื่อปรับระดับการวิเคราะห์หลังบ้านเจ้าค่ะ:",
    ["🏡 ระดับชาวบ้าน (เน้นเข้าใจง่าย เข้าถึงพึ่งพาได้)", 
     "📰 ระดับนักข่าว (เน้นข้อเท็จจริง สรุปประเด็น คมชัด รวดเร็ว)", 
     "💼 ระดับทนายความ (เน้นกลยุทธ์คดีความเชิงลึก เข้มข้นสะใจ)"]
)

# 5. ช่องสำหรับป้อนเรื่องราวร่องทุกข์
user_input = str_layout.text_area(
    "ป้อนพฤติการณ์คดี หรือเรื่องราวร่องทุกข์ที่ต้องการให้วิเคราะห์:",
    height=200,
    placeholder="พิมพ์เรื่องราวคดีความที่นี่ได้เลยเจ้าค่ะ..."
)

# 6. ปุ่มวิเศษสั่งรันสมอง AI
if str_layout.button("เริ่มวิเคราะห์กลยุทธ์คดี"):
    if user_input.strip() == "":
        str_layout.warning("กรุณากรอกพฤติการณ์คดีก่อนกดปุ่มวิเคราะห์นะเจ้าคะคุณพี่ขา")
    else:
        with str_layout.spinner("หุ่นยนต์กำลังรันสูตรกลยุทธ์ตามคลังสมองกฎหมาย..."):
            try:
                # ตั้งค่าคำสั่งควบคุมสมอง AI (System Instruction) ตามระดับผู้ใช้ที่คุณพี่ออกแบบ
                if "ชาวบ้าน" in user_role:
                    role_instruction = "คุณคือที่พึ่งกฎหมายของชาวบ้าน จงอธิบายด้วยภาษาชาวบ้านที่ง่ายที่สุด อบอุ่น สรุปสิทธิ์และสิ่งเสี่ยงที่เขาต้องรู้เหมือนญาติมิตรเตือนกัน ไม่ใช้ศัพท์กฎหมายยากๆ"
                elif "นักข่าว" in user_role:
                    role_instruction = "คุณคือที่ปรึกษากฎหมายสำหรับสื่อมวลชน จงสรุปประเด็นข้อเท็จจริงให้คมชัด แบ่งเป็นข้อๆ แยกแยะส่วนที่เป็นข้อเท็จจริงและข้อกฎหมายให้ชัดเจน เพื่อนำไปรายงานข่าวได้อย่างถูกต้องแม่นยำ"
                else:
                    role_instruction = "คุณคือที่ปรึกษากฎหมายอาวุโส (Senior Legal Consultant) วิเคราะห์กลยุทธ์คดีความเชิงลึกสำหรับทนายความ อ้างอิงหลักกฎหมาย องค์ประกอบความผิด และแนวทางการสู้คดีหรือตั้งฟ้องอย่างรัดกุม"

                # สั่งงานหุ่นยนต์ Gemini
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=role_instruction
                )
                
                response = model.generate_content(user_input)
                
                # โชว์ผลลัพธ์ความปังบนหน้าเว็บ
                str_layout.success(f"✨ ผลการวิเคราะห์สำหรับ {user_role.split(' ')[1]}")
                str_layout.write(response.text)
                
            except Exception as e:
                str_layout.error(f"อุ๊ย ระบบขัดข้องเกี่ยวกับการต่อสาย Gemini API Key เจ้าค่ะ: {e}")from pathlib import Path
import google.generativeai as genai
import streamlit as str_layout

# =============================================================================
# ตั้งค่าหน้าตาแอปพลิเคชัน (Page Configuration) - ต้องอยู่บนสุดหลัง import เจ้าค่ะ
# =============================================================================
str_layout.set_page_config(
    page_title="สมาคมพลังสื่อ มิตรสัมพันธ์", page_icon="⚖️", layout="wide"
)

# =============================================================================
# 🔐 กล่องเซฟนิรภัย: วิ่งไปดึงรหัส API Key จากหลังบ้าน Streamlit Cloud (ปลอดภัย 100%)
# =============================================================================
try:
    genai.configure(api_key=str_layout.secrets["GEMINI_API_KEY"])
except Exception:
    # เผื่อกรณีรันในเครื่องตัวเองแล้วยังไม่ได้ตั้งค่าเซฟหลังบ้าน จะได้ไม่ล่มไปก่อนเจ้าค่ะ
    pass

str_layout.title("🔮 ระบบวิเคราะห์กลยุทธ์คดีความและคลังสมองกฎหมาย")
str_layout.write(
    "ระบบพร้อมชันสูตรคดีและดึงข้อมูลจากตู้ความรู้ 02_Knowledge แล้วเจ้าค่ะ"
)

# =============================================================================
# 📦 การตั้งค่าคลังข้อมูลหลังบ้าน (จัดระเบียบใหม่ไม่ให้ตีกัน)
# =============================================================================
# สร้างตัวแปร Path ชี้ไปที่โฟลเดอร์คลังข้อมูลของคุณพี่
KNOWLEDGE_DIR = Path("02_คลังฎีกา_อัพเดท")

# ดึงข้อมูลจากไฟล์ข้อความทั้งหมดในโฟลเดอร์มารวมกันดักทาง Fact-First
deka_context = ""

if KNOWLEDGE_DIR.exists():
    # สแกนหาไฟล์ .txt ทั้งหมดในโฟลเดอร์โดยอัตโนมัติ
    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        try:
            deka_context += f"\n--- เนื้อหาจากไฟล์: {file_path.name} ---\n"
            deka_context += file_path.read_text(encoding="utf-8") + "\n"
        except Exception:
            pass
else:
    deka_context = "ไม่มีข้อมูลในคลัง"

# =============================================================================
# ส่วนหน้าบ้านรับข้อมูลจากผู้ใช้งาน (โชว์เด่นค้างฟ้าถาวร)
# =============================================================================
user_input = str_layout.text_area(
    "ป้อนพฤติการณ์คดี หรือเรื่องราวร้องทุกข์ที่ต้องการให้วิเคราะห์:",
    height=200,
)
click_analyze = str_layout.button("เริ่มวิเคราะห์กลยุทธ์คดี")

# ส่วนประมวลผลเมื่อกดปุ่ม
if click_analyze:
    if user_input:
        with str_layout.spinner(
            "หนุ่มน้อย Gemini กำลังวิ่งสแกนคลังกฎหมาย... โปรดรอสักครู่นะเจ้าคะ"
        ):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")

                final_prompt = f"""
                คุณคือทนายความผู้เชี่ยวชาญและที่ปรึกษากฎหมายขั้นสูงของสมาคมพลังสื่อ มิตรสัมพันธ์
                จงวิเคราะห์ข้อเท็จจริงที่ผู้ใช้งานให้มา โดยต้องใช้กฎเหล็ก Fact-First Protocol 
                สแกนหาหลักเกณฑ์และแนวคิดจากคลังข้อมูลหลังบ้านที่ให้ไปด้านล่างนี้มาตอบอย่างเคร่งครัด
                
                [คลังข้อมูลกฎหมายและแนวทางพิจารณา (ฐานความรู้หลังบ้าน)]:
                {deka_context}
                
                [ข้อเท็จจริงคดีที่ต้องวิเคราะห์]:
                {user_input}
                
                จงตอบแยกประเด็นให้ชัดเจนสลอนตา: องค์ประกอบความผิด, จุดตายของคดี, อายุความ และคำแนะนำกลยุทธ์
                """

                response = model.generate_content(final_prompt)

                # แสดงผลลัพธ์ด้านล่างกล่องรับข้อมูลทันที สะอาดตา
                str_layout.success("วิเคราะห์เสร็จสิ้นแล้วเจ้าค่ะคุณพี่ประธาน!")
                str_layout.markdown(response.text)

            except Exception as e:
                str_layout.error(f"เกิดข้อผิดพลาดทางเทคนิค: {e}")
    else:
        str_layout.warning("คุณพี่โปรดพิมพ์ข้อเท็จจริงคดีก่อนกดปุ่มนะเจ้าคะ")