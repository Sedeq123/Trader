# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 1. إعدادات النظام وتفعيل الوضع الداكن تلقائياً
st.set_page_config(
    page_title="منصة المتداول المنضبط",
    page_icon="📊",
    layout="wide"
)

# عنوان رئيسي آمن برمجياً
st.title("📊 منصة المتداول المنضبط الذكية")
st.write("---")

# 2. إدارة الجلسة وحفظ البيانات
if 'journal' not in st.session_state:
    st.session_state.journal = pd.DataFrame(columns=[
        "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "النزيف السلوكي ($)"
    ])

# 3. مؤشر الجاهزية النفسية بأزرار خيارات مريحة للجوال
st.markdown("### 🩺 1. مؤشر الجاهزية النفسية والصحية")
st.write("قيم حالتك الآن بسرعة قبل فتح الشارت:")

col_h1, col_h2 = st.columns(2)
with col_h1:
    sleep_opt = st.radio("جودة النوم والراحة اليوم:", ["5 - ممتاز", "4 - جيد", "3 - متوسط", "2 - سيء", "1 - منعدم"], horizontal=True)
    focus_opt = st.radio("مستوى التركيز الذهني حالياً:", ["5 - صافي تماماً", "4 - مركّز", "3 - مشتت قليلاً", "2 - مرهق", "1 - غائب تماماً"], horizontal=True)
with col_h2:
    calm_opt = st.radio("الهدوء النفسي والابتعاد عن التوتر:", ["5 - مستقر جداً", "4 - هادئ", "3 - قلق بعض الشيء", "2 - متوتر", "1 - معصب/منتقم"], horizontal=True)
    discipline_opt = st.radio("الالتزام المسبق بخطة التداول اليوم:", ["5 - ملتزم بالكامل", "4 - خطة واضحة", "3 - تردد", "2 - بدون خطة واضحة", "1 - عشوائي"], horizontal=True)

# حساب النقاط
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

st.success(f"حالة النظام السلوكي الحالية: {health_status}")
st.write("---")

# 4. حاسبة حجم العقد (Lot Size) المرنة
st.markdown("### 🛡️ 2. حاسبة حجم العقد (Lot Size) الذكية")
col_c1, col_c2 = st.columns(2)
with col_c1:
    capital = st.number_input("رأس مال الحساب الكلي ($)", min_value=10.0, value=10000.0, step=100.0)
    risk_pct = st.number_input("المخاطرة المطلوبة للصفقة القياسية (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1) / 100
with col_c2:
    stop_loss = st.number_input("وقف الخسارة بالنقاط المتوقعة (SL Pips)", min_value=1, value=30, step=5)
    pip_value = st.number_input("قيمة النقطة لعقد 1 لوت كامل ($)", min_value=0.1, value=10.0, step=0.5)

# الحسابات
allowed_risk_usd = capital * (risk_pct * risk_modifier)
calculated_lot = allowed_risk_usd / (stop_loss * pip_value) if stop_loss > 0 and pip_value > 0 else 0.0

# عرض النتيجة بدون صناديق معقدة تسبب مشاكل
st.warning(f"حجم العقد الآمن المسموح به فوراً بناءً على حالتك النفسية: {calculated_lot:.2f} Lot")
st.write(f"المخاطرة المالية الفعلية المعتمدة حالياً لهذه الصفقة: ${allowed_risk_usd:.2f}")
st.write("---")

# 5. سجل الصفقات ورصد النزيف السلوكي المتراكم
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
    waste_usd = abs(result_usd) if result_usd < 0 and "التزام" not in reason else 0.0
    new_trade = {
        "رقم الصفقة": len(st.session_state.journal) + 1,
        "الأصل المالي": asset,
        "نوع الصفقة": trade_type,
        "النتيجة ($)": result_usd,
        "السبب السلوكي للخسارة": reason,
        "النزيف السلوكي ($)": waste_usd
    }
    st.session_state.journal = pd.concat([st.session_state.journal, pd.DataFrame([new_trade])], ignore_index=True)
    st.rerun()

# 6. التقرير البصري للرسومات والبيانات
if not st.session_state.journal.empty:
    st.write("---")
    st.markdown("### 📊 4. لوحة التحليل البصري التفاعلية")
    df = st.session_state.journal
    
    chart_data = pd.DataFrame({
        'أرباح وخسائر الصفقات ($)': df['النتيجة ($)'],
        'النزيف السلوكي المهدور ($)': df['النزيف السلوكي ($)']
    })
    st.bar_chart(chart_data)
    
    st.markdown("#### 📋 تفاصيل سجل البيانات")
    st.dataframe(st.session_state.journal, use_container_width=True, hide_index=True)
    
    if st.button("🔄 تصفير مساحة تدوين البيانات"):
        st.session_state.journal = pd.DataFrame(columns=[
            "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "النزيف السلوكي ($)"
        ])
        st.rerun()
