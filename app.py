# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Disciplined Trader",
    page_icon="📊",
    layout="wide"
)

# 2. Professional Dark Theme CSS (Binance & TradingView Style)
st.markdown("""
    <html lang="ar" dir="rtl">
    <head>
        <meta name="google" content="notranslate">
    </head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #0B0E11 !important;
        color: #EAECEF !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    * { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
    
    .main-title {
        color: #F0B90B;
        text-align: center !important;
        font-weight: 700;
        margin-bottom: 25px;
        border-bottom: 2px solid #2B3139;
        padding-bottom: 15px;
    }
    
    .badge-box {
        background-color: #181A20 !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2B3139;
        border-right: 5px solid #F0B90B;
        margin-top: 15px;
    }
    
    div[data-testid="stMarkdownContainer"] p { color: #EAECEF !important; }
    .stSelectbox, .stNumberInput, .stRadio {
        background-color: #181A20 !important;
        border-radius: 8px;
    }
    
    .stButton>button {
        background-color: #F0B90B !important;
        color: #0B0E11 !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 8px !important;
        border: none !important;
    }
    </style>
    </html>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📊 منصة المتداول المنضبط الذكية</h1>", unsafe_allow_html=True)

# 3. Session State Management
if 'journal' not in st.session_state:
    st.session_state.journal = pd.DataFrame(columns=[
        "ID", "Asset", "Type", "Result ($)", "Behavior Note", "Waste ($)"
    ])

# 4. Psychological Health Score (Buttons optimized for Mobile)
st.markdown("### 🩺 1. مؤشر الجاهزية النفسية والصحية")
st.write("قيم حالتك الآن بسرعة عبر الأزرار المخصصة لشاشة الجوال:")

col_h1, col_h2 = st.columns(2)
with col_h1:
    sleep_opt = st.radio("جودة النوم والراحة اليوم:", ["5 - ممتاز", "4 - جيد", "3 - متوسط", "2 - سيء", "1 - منعدم"], horizontal=True)
    focus_opt = st.radio("مستوى التركيز الذهني حالياً:", ["5 - صافي تماماً", "4 - مركّز", "3 - مشتت قليلاً", "2 - مرهق", "1 - غائب تماماً"], horizontal=True)
with col_h2:
    calm_opt = st.radio("الهدوء النفسي والابتعاد عن التوتر:", ["5 - مستقر جداً", "4 - هادئ", "3 - قلق بعض الشيء", "2 - متوتر", "1 - معصب/منتقم"], horizontal=True)
    discipline_opt = st.radio("الالتزام المسبق بخطة التداول اليوم:", ["5 - ملتزم بالكامل", "4 - خطة واضحة", "3 - تردد", "2 - بدون خطة واضحة", "1 - عشوائي"], horizontal=True)

# Parsing values safely
sleep = int(sleep_opt[0])
focus = int(focus_opt[0])
calm = int(calm_opt[0])
discipline = int(discipline_opt[0])

health_score = (sleep + focus + calm + discipline) / 4

if health_score >= 4.0:
    health_status, risk_modifier = "🟢 تداول ممتاز (انضباط كامل ومخاطرة كاملة)", 1.0
elif health_score >= 2.5:
    health_status, risk_modifier = "🟡 حذر: مخاطرة منخفضة بالنصف (حسابك في أمان)", 0.5
else:
    health_status, risk_modifier = "🔴 خطر: توقف عن التداول فوراً اليوم واغلق الشارت", 0.0

st.info(f"حالة النظام السلوكي الحالية: **{health_status}**")

st.markdown("---")

# 5. Safe Lot Size Calculator (Fixed for Mobile arrows)
st.markdown("### 🛡️ 2. حاسبة حجم العقد (Lot Size) الذكية")
col_c1, col_c2 = st.columns(2)
with col_c1:
    capital = st.number_input("رأس مال الحساب الكلي ($)", min_value=10.0, value=10000.0, step=100.0)
    risk_pct = st.number_input("المخاطرة المطلوبة للصفقة القياسية (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1) / 100
with col_c2:
    stop_loss = st.number_input("وقف الخسارة بالنقاط المتوقعة (SL Pips)", min_value=1, value=30, step=5)
    pip_value = st.number_input("قيمة النقطة لعقد 1 لوت كامل ($)", min_value=0.1, value=10.0, step=0.5)

# Calculate Risk and Lot size
allowed_risk_usd = capital * (risk_pct * risk_modifier)
calculated_lot = allowed_risk_usd / (stop_loss * pip_value) if stop_loss > 0 and pip_value > 0 else 0.0

st.markdown(f"""
    <div class="badge-box">
        <p style='margin:0; font-size:16px; color:#EAECEF;'>حجم العقد الآمن المسموح به فوراً بناءً على حالتك النفسية:</p>
        <h2 style='margin:10px 0; color:#F0B90B; font-weight:bold; font-size: 32px; text-align: center !important;'>➡️ {calculated_lot:.2f} Lot</h2>
        <p style='margin:0; font-size:13px; color:#848E9C;'>المخاطرة المالية الفعلية المعتمدة حالياً لهذه الصفقة: ${allowed_risk_usd:.2f}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 6. Trade Logging & Behavioral Analytics
st.markdown("### 📝 3. سجل الصفقات الفوري ورصد الأخطاء السلوكية")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    asset = st.selectbox("الأصل المالي المتداول", ["XAUUSD (الذهب)", "NASDAQ100", "US30", "USOIL"])
    trade_type = st.selectbox("نوع أمر التداول", ["BUY", "SELL"])
with col_f2:
    result_usd = st.number_input("صافي نتيجة الصفقة المحققة ($)", value=0.0, step=10.0)
with col_f3:
    reason = st.selectbox("السبب السلوكي وراء النتيجة", [
        "Plan Discipline (التزام بالخطة)", 
        "Revenge Trading (انتقام من السوق)", 
        "Greed (طمع وزيادة لوت)", 
        "FOMO (خوف من فوات الفرصة)",
        "Fear (خروج مبكر بسبب الخوف)"
    ])

if st.button("💾 حفظ وتدوين الصفقة في سجل النظام"):
    waste_usd = abs(result_usd) if result_usd < 0 and "Plan Discipline" not in reason else 0.0
    new_trade = {
        "ID": len(st.session_state.journal) + 1,
        "Asset": asset,
        "Type": trade_type,
        "Result ($)": result_usd,
        "Behavior Note": reason,
        "Waste ($)": waste_usd
    }
    st.session_state.journal = pd.concat([st.session_state.journal, pd.DataFrame([new_trade])], ignore_index=True)
    st.rerun()

# 7. Visual Analytics & Tables
if not st.session_state.journal.empty:
    st.markdown("### 📊 4. لوحة التحليل البصري التفاعلية")
    df = st.session_state.journal
    
    chart_data = pd.DataFrame({
        'Result ($)': df['Result ($)'],
        'Behavioral Waste ($)': df['Waste ($)']
    })
    st.bar_chart(chart_data)
    
    st.markdown("#### 📋 تفاصيل سجل البيانات")
    st.dataframe(st.session_state.journal, use_container_width=True, hide_index=True)
    
    if st.button("🔄 تصفير مساحة تدوين البيانات"):
        st.session_state.journal = pd.DataFrame(columns=[
            "ID", "Asset", "Type", "Result ($)", "Behavior Note", "Waste ($)"
        ])
        st.rerun()
