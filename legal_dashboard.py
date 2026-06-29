import streamlit as st
import json
import datetime

# --- ฟังก์ชันจัดการข้อมูล ---
def load_data():
    try:
        with open("case_database.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except: return []

def save_data(data):
    with open("case_database.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()
total_cases = len(data)
closed_cases = len([d for d in data if d.get("status") == "ปิดเคสแล้ว"])
pending_cases = len([d for d in data if d.get("status") != "ปิดเคสแล้ว"])

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="สมาคมพลังสื่อฯ", layout="wide")

# CSS ตกแต่ง (แดงไล่เฉดทอง)
st.markdown("""
    <style>
    .hero { 
        background: linear-gradient(90deg, #B22222, #DAA520); 
        padding: 40px; border-radius: 10px; color: white; text-align: center; 
    }
    div.stButton > button { background-color: #DAA520; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- หน้าแสดงผล ---
tab1, tab2 = st.tabs(["🏠 หน้าแรก", "⚖️ ระบบจัดการภายใน"])

with tab1:
    st.markdown('<div class="hero"><h1>เพื่อความยุติธรรม เพื่อความทรงธรรม เพื่อประชาชน</h1><p>สมาคมพลังสื่อ มิตรสัมพันธ์ช่วยเหลือสังคม ตรวจสอบความทุจริต และยืนเคียงข้างผู้บริสุทธิ์</p></div>', unsafe_allow_html=True)
    st.write("##")
    col1, col2, col3 = st.columns(3)
    col1.metric("เรื่องร้องเรียนทั้งหมด", total_cases)
    col2.metric("ช่วยเหลือสำเร็จแล้ว", closed_cases)
    col3.metric("กำลังดำเนินการ", pending_cases)
    if st.button("📝 ยื่นเรื่องร้องเรียนออนไลน์"):
        st.info("กรุณาไปที่ Tab 'ระบบจัดการภายใน' เพื่อทำรายการค๊า")

with tab2:
    mode = st.radio("เลือกโหมดการใช้งาน:", ["ประชาชน (ยื่นเรื่อง)", "เจ้าหน้าที่ (แอดมิน/ผอ./ทนาย)"])
    if mode == "ประชาชน (ยื่นเรื่อง)":
        with st.form("citizen_form"):
            name = st.text_input("ชื่อ-นามสกุล"); age = st.number_input("อายุ", min_value=0); job = st.text_input("อาชีพ")
            address = st.text_area("ที่อยู่"); complaint = st.text_area("รายละเอียดปัญหา")
            if st.form_submit_button("ส่งเรื่อง"):
                data.append({"timestamp": str(datetime.datetime.now()), "citizen": {"name": name, "age": age, "job": job, "address": address}, "complaint": complaint, "status": "รอแอดมินสอบถาม", "admin_notes": "", "lawyer_analysis": "", "assigned_lawyer": "", "case_type": "รอระบุ"})
                save_data(data); st.success("บันทึกข้อมูลเรียบร้อยค๊า!")
    else:
        role = st.selectbox("เลือกบทบาท:", ["แอดมิน", "ผู้อำนวยการ", "ทนายความ"])
        if role == "แอดมิน":
            for i, d in enumerate(data):
                if d["status"] == "รอแอดมินสอบถาม":
                    with st.expander(f"เคส: {d['citizen']['name']}"):
                        st.write(d["complaint"]); notes = st.text_area("บันทึก:", d["admin_notes"], key=f"n{i}")
                        if st.button("ส่งให้ ผอ.", key=f"b{i}"): d["admin_notes"] = notes; d["status"] = "รอผู้อำนวยการวิเคราะห์"; save_data(data); st.rerun()
        elif role == "ผู้อำนวยการ":
            for i, d in enumerate(data):
                if d["status"] == "รอผู้อำนวยการวิเคราะห์":
                    with st.expander(f"วิเคราะห์: {d['citizen']['name']}"):
                        an = st.text_area("ผลวิเคราะห์:", key=f"an{i}"); ty = st.selectbox("ประเภท:", ["แพ่ง", "อาญา", "ปกครอง"], key=f"ty{i}"); lw = st.text_input("ทนาย:", key=f"lw{i}")
                        if st.button("ส่งให้ทนาย", key=f"bs{i}"): d.update({"lawyer_analysis": an, "case_type": ty, "assigned_lawyer": lw, "status": "กำลังดำเนินการ"}); save_data(data); st.rerun()
                elif d["status"] == "รอ ผอ. อนุมัติปิดเคส":
                    with st.expander(f"อนุมัติปิด: {d['citizen']['name']}"):
                        st.write(f"รายงานทนาย: {d.get('court_report')}")
                        if st.button("อนุมัติ", key=f"cl{i}"): d["status"] = "ปิดเคสแล้ว"; save_data(data); st.rerun()
        elif role == "ทนายความ":
            for i, d in enumerate(data):
                if d["status"] == "กำลังดำเนินการ":
                    with st.expander(f"คดีของคุณ: {d['citizen']['name']}"):
                        st.write(f"วิเคราะห์จาก ผอ.: {d['lawyer_analysis']}")
                        rpt = st.text_area("รายงาน:", key=f"rpt{i}")
                        if st.button("ส่งรายงาน", key=f"sr{i}"): d["court_report"] = rpt; d["status"] = "รอ ผอ. อนุมัติปิดเคส"; save_data(data); st.rerun()