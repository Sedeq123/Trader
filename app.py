# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منصة المتداول المنضبط",
    page_icon="📊",
    layout="wide"
)

# 2. تصميم الواجهة الاحترافية (خلفية داكنة متوافقة مع لغة المتصفح)
st.markdown("""
    <html lang="ar" dir="rtl">
    <head>
        <meta name="google" content="notranslate">
    </head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* الخلفية العامة للتطبيق ونمط الشارت الداكن */
    .stApp {
        background-color: #0B0E11 !important;
        color: #EAECEF !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* توجيه النصوص والخطوط للعربية */
    * { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
    
    /* العناوين الرئيسية */
    .main-title {
        color: #F0B90B;
        text-align: center !important;
        font-weight: 700;
        margin-bottom: 25px;
        border-bottom: 2px solid #2B3139;
        padding-bottom: 15px;
    }
    
    /* صناديق النتائج والحاسبة */
    .badge-box {
        background-color: #181A20 !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2B3139;
        border-right: 5px solid #F0B90B;
        margin-top: 15px;
    }
    
    /* تعديل عناصر المدخلات לתناسب الثيم الداكن */
    div[data-testid="stMarkdownContainer"] p { color: #EAECEF !important; }
    .stSelectbox, .stNumberInput, .stRadio {
        background-color: #181A20 !important;
        border-radius: 8px;
    }
    
    /* تخصيص الأزرار */
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

# 3. إدارة الجلسة لحفظ البيانات دون مسحها عند التحديث
if 'trade_journal' not in st.session_state:
    st.session_state.trade_journal = pd.DataFrame(columns=[
        "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "النزيف السلوكي ($)"
    ])

# 4. مؤشر الجاهزية النفسية بأزرار خيارات مريحة للجوال
st.markdown("### 🩺 1. مؤشر الجاهزية النفسية والصحية")
st.write("قيم حالتك الآن بسرعة عبر الأزرار المخصصة لشاشة الجوال:")

col_h1, col_h2 = st.columns(2)
with col_h1:
    sleep_opt = st.radio("جودة النوم والراحة اليوم:", ["ممتاز (5)", "جيد (4)", "متوسط (3)", "سيء (2)", "منعدم (1)"], horizontal=True)
    focus_opt = st.radio("مستوى التركيز الذهني حالياً:", ["صافي تماماً (5)", "مركّز (4)", "مشتت قليلاً (3)", "مرهق (2)", "غائب تماماً (1)"], horizontal=True)
with col_h2:
    calm_opt = st.radio("الهدوء النفسي والابتعاد عن التوتر:", ["مستقر جداً (5)", "هادئ (4)", "قلق بعض الشيء (3)", "متوتر (2)", "معصب/منتقم (1)"], horizontal=True)
    discipline_opt = st.radio("الالتزام المسبق بخطة التداول اليوم:", ["ملتزم بالكامل (5)", "خطة واضحة (4)", "تردد (3)", "بدون خطة واضحة (2)", "عشوائي (1)"], horizontal=True)

# استخراج القيم الرقمية من النص المختار للأزرار تلقائياً
sleep = int(sleep_opt[-2])
focus = int(focus_opt[-2])
calm = int(calm_opt[-2])
discipline = int(discipline_opt[-2])

health_score = (sleep + focus + calm + discipline) / 4

# تحديد التعديل البرمجي للمخاطرة بناء على الحالة النفسية
if health_score >= 4.0:
    health_status, risk_modifier = "🟢 تداول ممتاز (انضباط كامل ومخاطرة كاملة)", 1.0
elif health_score >= 2.5:
    health_status, risk_modifier = "🟡 حذر: مخاطرة منخفضة بالنصف (حسابك في أمان)", 0.5
else:
    health_status, risk_modifier = "🔴 خطر: توقف عن التداول فوراً اليوم واغلق الشارت", 0.0

st.info(f"حالة النظام السلوكي الحالية: **{health_status}**")

st.markdown("---")

# 5. حاسبة حجم العقد (Lot Size) المرنة
st.markdown("### 🛡️ 2. حاسبة حجم العقد (Lot Size) الذكية")
col_c1, col_c2 = st.columns(2)
with col_c1:
    capital = st.number_input("رأس مال الحساب الكلي ($)", min_value=10.0, value=10000.0, step=100.0)
    risk_pct = st.number_input("المخاطرة المطلوبة للصفقة القياسية (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1) / 100
with col_c2:
    stop_loss = st.number_input("وقف الخسارة بالنقاط المتوقعة (SL Pips)", min_value=1, value=30, step=5)
    pip_value = st.number_input("قيمة النقطة لعقد 1 لوت كامل ($)", min_value=0.1, value=10.0, step=0.5)

# الحساب الرياضي الديناميكي المربوط تلقائياً بمؤشر الصحة النفسية
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

# 6. سجل الصفقات ورصد النزيف السلوكي المتراكم
st.markdown("### 📝 3. سجل الصفقات الفوري ورصد الأخطاء السلوكية")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    asset = st.selectbox("الأصل المالي المتداول", ["XAUUSD (الذهب)", "NASDAQ100", "US30 (الداو جونز)", "USOIL (النفط)"])
    trade_type = st.selectbox("نوع أمر التداول", ["BUY", "SELL"])
with col_f2:
    result_usd = st.number_input("صافي نتيجة الصفقة المحققة ($)", value=0.0, step=10.0)
with col_f3:
    reason = st.selectbox("السبب السلوكي وراء النتيجة", [
        "التزام كامل وصارم بالاستراتيجية والخطة", 
        "انتقام من السوق بسبب خسارة سابقة (Revenge Trading)", 
        "طمع وإفراط غير مبرر في حجم اللوت (Greed)", 
        "دخول متأخر بسبب الخوف من فوات الفرصة (FOMO)",
        "خروج مبكر جداً ناتج عن الخوف والتردد"
    ])

if st.button("💾 حفظ وتدوين الصفقة في سجل النظام"):
    waste_usd = abs(result_usd) if result_usd < 0 and reason != "التزام كامل وصارم بالاستراتيجية والخطة" else 0.0
    new_trade = {
        "رقم الصفقة": len(st.session_state.trade_journal) + 1,
        "الأصل المالي": asset,
        "نوع الصفقة": trade_type,
        "النتيجة ($)": result_usd,
        "السبب السلوكي للخسارة": reason,
        "النزيف السلوكي ($)": waste_usd
    }
    st.session_state.trade_journal = pd.concat([st.session_state.trade_journal, pd.DataFrame([new_trade])], ignore_index=True)
    st.rerun()

# 7. التقرير البصري للرسومات والبيانات
if not st.session_state.trade_journal.empty:
    st.markdown("### 📊 4. لوحة التحليل البصري التفاعلية")
    df = st.session_state.trade_journal
    chart_data = pd.DataFrame({
        'أرباح وخسائر الصفقات ($)': df['النتيجة ($)'],
        'النزيف السلوكي المهدور ($)': df['النزيف السلوكي ($)']
    })
    st.bar_chart(chart_data)
    st.markdown("#### 📋 تفاصيل سجل البيانات المسجل اليوم")
    st.dataframe(st.session_state.trade_journal, use_container_width=True, hide_index=True)
    if st.button("🔄 تصفير مساحة تدوين البيانات"):
        st.session_state.trade_journal = pd.DataFrame(columns=[
            "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "النزيف السلوكي ($)"
        ])
        st.rerun()
