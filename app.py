import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة المتداول المنضبط",
    page_icon="📊",
    layout="wide"
)

# تعطيل محاولات الترجمة التلقائية وتنسيق الواجهة
st.markdown("""
    <html lang="ar" dir="rtl">
    <head>
        <meta name="google" content="notranslate">
    </head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; }
    .stMetric, .stMarkdown, div[data-testid="stMetricValue"] { text-align: right !important; }
    .main-title { color: #1A2332; text-align: center !important; font-weight: 700; margin-bottom: 25px; }
    .badge-box { background-color: #FFF2E6; padding: 15px; border-radius: 8px; border-right: 5px solid #FF8000; margin-top: 15px; }
    </style>
    </html>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📊 منصة المتداول المنضبط الذكية</h1>", unsafe_allow_html=True)

# 1. إدارة البيانات
if 'trade_journal' not in st.session_state:
    st.session_state.trade_journal = pd.DataFrame(columns=[
        "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "النزيف السلوكي ($)"
    ])

# 2. مؤشر الصحة النفسية (في الواجهة الرئيسية لسهولة الاستخدام على الجوال)
st.markdown("### 🩺 1. مؤشر الجاهزية النفسية والصحية (قبل التداول)")
col_h1, col_h2 = st.columns(2)
with col_h1:
    sleep = st.slider("جودة النوم والراحة (1-5)", 1, 5, 5)
    focus = st.slider("التركيز الذهني والوعي (1-5)", 1, 5, 4)
with col_h2:
    calm = st.slider("الهدوء النفسي والابتعاد عن التوتر (1-5)", 1, 5, 4)
    discipline = st.slider("الالتزام المسبق بالخطة (1-5)", 1, 5, 5)

health_score = (sleep + focus + calm + discipline) / 4

if health_score >= 4.0:
    health_status, risk_modifier, color = "🟢 تداول ممتاز (انضباط كامل)", 1.0, "green"
elif health_score >= 2.5:
    health_status, risk_modifier, color = "🟡 مخاطرة منخفضة بالنصف (حذر)", 0.5, "orange"
else:
    health_status, risk_modifier, color = "🔴 توقف عن التداول اليوم (خطر نفسي)", 0.0, "red"

st.write(f"حالة الجاهزية النفسية الحالية: **{health_status}**")

st.markdown("---")

# 3. حاسبة إدارة المخاطر وحجم العقد (Lot Size)
st.markdown("### 🛡️ 2. حاسبة حجم العقد (Lot Size) الآمن")
col_c1, col_c2 = st.columns(2)
with col_c1:
    capital = st.number_input("رأس مال الحساب ($)", min_value=100.0, value=10000.0, step=100.0)
    risk_pct = st.number_input("المخاطرة المطلوبة للصفقة (%)", min_value=0.1, max_value=5.0, value=1.0, step=0.1) / 100
with col_c2:
    stop_loss = st.number_input("وقف الخسارة بالنقاط (SL Pips)", min_value=1, value=30)
    pip_value = st.number_input("قيمة النقطة لعقد 1 لوت قياسي ($)", min_value=0.1, value=10.0)

# الحساب الذكي
allowed_risk_usd = capital * (risk_pct * risk_modifier)
calculated_lot = allowed_risk_usd / (stop_loss * pip_value) if stop_loss > 0 else 0.0

st.markdown(f"""
    <div class="badge-box">
        <p style='margin:0; font-size:16px; color:#1A2332;'>حجم العقد المسموح به فوراً (Lot Size):</p>
        <h2 style='margin:5px 0 0 0; color:#FF8000; font-weight:bold;'>➡️ {calculated_lot:.2f} Lot</h2>
        <small style='color:#555;'>المخاطرة المالية المعتمدة حالياً: ${allowed_risk_usd:.2f}</small>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. سجل الصفقات والرسومات البيانية
st.markdown("### 📝 3. رصد الصفقات والنزيف السلوكي")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    asset = st.selectbox("الأصل المالي", ["XAUUSD (الذهب)", "NASDAQ100", "US30", "USOIL"])
    trade_type = st.selectbox("نوع الصفقة", ["BUY", "SELL"])
with col_f2:
    result_usd = st.number_input("صافي نتيجة الصفقة ($)", value=0.0, step=10.0)
with col_f3:
    reason = st.selectbox("السبب السلوكي الكامن", [
        "التزام كامل بالخطة", 
        "انتقام من السوق (Revenge Trading)", 
        "طمع وزيادة لوت (Greed)", 
        "خوف من فوات الفرصة (FOMO)"
    ])

if st.button("💾 حفظ الصفقة في النظام"):
    waste_usd = abs(result_usd) if result_usd < 0 and reason != "التزام كامل بالخطة" else 0.0
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

# 5. عرض الرسومات البيانية وجدول البيانات (إذا وُجدت صفقات)
if not st.session_state.trade_journal.empty:
    st.markdown("### 📊 التحليل البصري والرسومات البيانية")
    
    # تجهيز بيانات الرسم البياني
    df = st.session_state.trade_journal
    chart_data = pd.DataFrame({
        'الأرباح/الخسائر المباشرة ($)': df['النتيجة ($)'],
        'النزيف السلوكي المتراكم ($)': df['النزيف السلوكي ($)']
    })
    
    # رسم بياني مدمج وتفاعلي يعرض الأداء والنزيف السلوكي جنبًا إلى جنب
    st.bar_chart(chart_data)
    
    st.markdown("#### 📋 سجل الصفقات المفصل")
    st.dataframe(st.session_state.trade_journal, use_container_width=True, hide_index=True)
    
    if st.button("🔄 تصفير السجل"):
        st.session_state.trade_journal = pd.DataFrame(columns=[
            "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "النزيف السلوكي ($)"
        ])
        st.rerun()
