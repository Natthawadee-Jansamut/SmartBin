import streamlit as st
import cv2
import numpy as np
from PIL import Image

# --- 1. การตั้งค่าหน้าเว็บและการออกแบบ (CSS) ---
st.set_page_config(page_title="SmartBin", page_icon="📸", layout="centered")

st.markdown("""
    <style>
    /* พื้นหลังและ Font */
    .stApp {
        background-color: #f8faff;
    }
    
    /* ส่วนหัว (Header) */
    .main-header {
        display: flex;
        align-items: center;
        padding: 10px 0;
    }
    .logo-text {
        font-weight: bold;
        font-size: 24px;
        margin-left: 10px;
        color: #1e293b;
    }
    
    /* แถบเมนูบน (Tabs) */
    .nav-container {
        display: flex;
        background-color: #e2e8f0;
        border-radius: 15px;
        padding: 5px;
        margin-bottom: 20px;
    }
    .nav-item {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        cursor: pointer;
    }
    .active-nav {
        background-color: white;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }

    /* กล่องแสดงภาพ (Camera Placeholder) */
    .camera-box {
        background-color: #111827;
        border-radius: 20px;
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        margin-bottom: 20px;
    }

    /* ปุ่มเปิดกล้องด้านล่าง */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 50px;
        background: linear-gradient(90deg, #00c698 0%, #0072ff 100%);
        color: white;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ส่วนแสดงผล UI ---

# Header
st.markdown('''
    <div class="main-header">
        <div style="background-color: #00c698; padding: 8px; border-radius: 8px;">📸</div>
        <div class="logo-text">SmartBin <br><span style="font-size: 12px; font-weight: normal; color: gray;">AI Plastic Bottle Detector</span></div>
    </div>
    ''', unsafe_allow_html=True)

# Navigation Tabs
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="nav-item active-nav">📷 กล้องตรวจจับ</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="nav-item">ℹ️ ข้อมูลพลาสติก</div>', unsafe_allow_html=True)

# Camera Area
placeholder = st.empty()

# สถานะเริ่มต้นเมื่อยังไม่เปิดกล้อง
with placeholder.container():
    st.markdown('''
        <div class="camera-box">
            <div style="font-size: 50px; opacity: 0.5;">📷</div>
            <div style="font-size: 20px; font-weight: bold; margin-top: 10px;">กล้องยังไม่เปิด</div>
            <div style="font-size: 14px; opacity: 0.7;">กดปุ่มด้านล่างเพื่อเริ่มใช้งาน</div>
        </div>
        ''', unsafe_allow_html=True)

# --- 3. ส่วนควบคุมระบบกล้อง ---
if st.button("📷 เปิดกล้อง"):
    cap = cv2.VideoCapture(0) # 0 คือกล้องหลักของเครื่อง
    stop_button = st.button("🛑 ปิดกล้อง")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("ไม่สามารถเข้าถึงกล้องได้")
            break
            
        # แปลงสี BGR เป็น RGB สำหรับ Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # แสดงผลใน Placeholder
        placeholder.image(frame, channels="RGB", use_column_width=True)
        
        if stop_button:
            break
            
    cap.release()
    