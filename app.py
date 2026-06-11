import streamlit as st
import pandas as pd

# إعدادات الصفحة والهوية البصرية
st.set_page_config(
    page_title="منصة المتداول المنضبط الذكية",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التنسيق باللغة العربية (RTL) والألوان المخصصة (Stardust Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: RTL;
        text-align: right;
    }
    .main-title {
        color: #1A2332;
        text-align: center;
        font-weight: 700;
        margin-bottom: 30px;
    }
    .section-header {
        color: #1A2332;
        border-right: 5px solid #FF8000;
        padding-right: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📊 منصة المتداول المنضبط — نظامك الذكي لتفكيك الأخطاء السلوكية</h1>", unsafe_allow_html=True)

# --- 1. بناء الجلسة لتخزين البيانات التفاعلية ---
if 'trade_journal' not in st.session_state:
    st.session_state.trade_journal = pd.DataFrame(columns=[
        "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "العائد المفقود ($)"
    ])

# --- 2. الشريط الجانبي: تقييم مؤشر الصحة الصباحي ---
st.sidebar.markdown("## 🩺 1. مؤشر الصحة التداولي الصباحي")
st.sidebar.write("أجب بصدق قبل فتح الشارت لتقييم جاهزيتك الذهنية:")

sleep = st.sidebar.slider("جودة النوم والراحة (1-5)", 1, 5, 5)
focus = st.sidebar.slider("التركيز الذهني والوعي (1-5)", 1, 5, 4)
calm = st.sidebar.slider("الهدوء النفسي والابتعاد عن التوتر (1-5)", 1, 5, 4)
discipline = st.sidebar.slider("الالتزام المسبق بالخطة (1-5)", 1, 5, 5)

# حساب معدل الجاهزية الحالي
health_score = (sleep + focus + calm + discipline) / 4

st.sidebar.markdown("---")
st.sidebar.write(f"**معدل الجاهزية الحالي:** {health_score:.1f} / 5.0")

# تحديد حالة التداول بناءً على المعدل السلوكي المبرمج
if health_score >= 4.0:
    health_status = "🟢 تداول ممتاز (انضباط كامل)"
    risk_modifier = 1.0
elif health_score >= 2.5:
    health_status = "🟡 مخاطرة منخفضة بالنصف (حذر)"
    risk_modifier = 0.5
else:
    health_status = "🔴 توقف عن التداول اليوم (خطر نفسي)"
    risk_modifier = 0.0

st.sidebar.info(f"حالة النظام الحالية:\n**{health_status}**")

# --- 3. لوحة تحكم علوية لعرض النزيف المالي (KPIs) ---
st.markdown("<h3 class='section-header'>🏆 لوحة التحكم الفورية</h3>", unsafe_allow_html=True)
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

total_trades = len(st.session_state.trade_journal)
net_profit = st.session_state.trade_journal["النتيجة ($)"].sum() if total_trades > 0 else 0.0
behavioral_waste = st.session_state.trade_journal["العائد المفقود ($)"].sum() if total_trades > 0 else 0.0

with col_kpi1:
    st.metric(label="مؤشر الجاهزية النفسية اليومي", value=f"{health_score:.1f} / 5", delta=health_status.split()[0])
with col_kpi2:
    st.metric(label="صافي أرباح/خسائر الصفقات ($)", value=f"${net_profit:,.2f}")
with col_kpi3:
    st.metric(label="إجمالي النزيف والعائد السلوكي المفقود ($)", value=f"${behavioral_waste:,.2f}", delta=f"-${behavioral_waste:,.2f}" if behavioral_waste > 0 else None, delta_color="inverse")

# --- 4. حاسبة المخاطرة المرنة واللوت الذكي ---
st.markdown("<h3 class='section-header'>🛡️ 2. درع حاسبة المخاطرة المرنة واللوت الدقيق</h3>", unsafe_allow_html=True)
col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    capital = st.number_input("حجم رأس المال الكلي الحسابي ($)", min_value=1.0, value=10000.0, step=100.0)
    standard_risk_pct = st.number_input("المخاطرة القياسية المسموحة للصفقة (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1) / 100

with col_calc2:
    stop_loss_pips = st.number_input("عدد نقاط وقف الخسارة المستهدفة (SL Pips)", min_value=1, value=30, step=1)
    pip_value_standard = st.number_input("قيمة النقطة لعقد 1 لوت قياسي ($)", min_value=0.1, value=10.0, step=0.5)

# تطبيق التعديل السلوكي البرمجي تلقائياً بناءً على مؤشر الصحة
adjusted_risk_pct = standard_risk_pct * risk_modifier
allowed_risk_usd = capital * adjusted_risk_pct

# حساب حجم العقد المسموح برمجياً مع تجنب خطأ القسمة على صفر
if stop_loss_pips > 0 and pip_value_standard > 0 and allowed_risk_usd > 0:
    calculated_lot = allowed_risk_usd / (stop_loss_pips * pip_value_standard)
else:
    calculated_lot = 0.0

# عرض النتيجة للمستخدم بصندوق ملون ومميز
st.markdown(f"""
    <div style="background-color: #FFF2E6; padding: 15px; border-radius: 5px; border-right: 5px solid #FF8000; text-align: center; margin-top: 15px;">
        <h4 style="margin: 0; color: #1A2332;">المخاطرة المعدلة سلوكياً: <b>{adjusted_risk_pct*100:.2f}%</b> | حجم العقد الآمن المسموح به فوراً:</h4>
        <h2 style="margin: 10px 0 0 0; color: #FF8000;">➡️ {calculated_lot:.2f} Lot</h2>
    </div>
""", unsafe_allow_html=True)

# --- 5. سجل صفقات المتداول ورصد الأخطاء النفسية حياً ---
st.markdown("<h3 class='section-header'>📝 3. سجل الصفقات اليومي ورصد الأخطاء السلوكية</h3>", unsafe_allow_html=True)

col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    asset = st.selectbox("الأصل المالي", ["XAUUSD (الذهب)", "NASDAQ100", "US30 (الداو جونز)", "USOIL (النفط)", "EURUSD", "GBPUSD"])
with col_f2:
    trade_type = st.selectbox("نوع الصفقة", ["BUY", "SELL"])
with col_f3:
    result_usd = st.number_input("النتيجة النهائية للصفقة ($)", value=0.0, step=10.0)
with col_f4:
    behavior_reason = st.selectbox("السبب السلوكي الكامن وراء النتيجة", [
        "التزام كامل وصارم بالخطة والاستراتيجية",
        "انتقام من السوق بسبب خسارة سابقة (Revenge Trading)",
        "طمع وإفراط في حجم اللوت المتفق عليه (Greed)",
        "دخول متأخر ناتج عن الخوف من فوات الفرصة (FOMO)",
        "خروج مبكر جداً بسبب الخوف والتردد"
    ])

# زر إدراج وتخزين الصفقة ديناميكياً داخل البرنامج
if st.button("➕ تسجيل وحفظ الصفقة في النظام التفاعلي"):
    # حساب العائد السلوكي المفقود تلقائياً
    # إذا كانت الصفقة خاسرة والسبب ليس الالتزام، نعتبر كامل الخسارة نزيفاً سلوكياً
    waste_usd = abs(result_usd) if result_usd < 0 and behavior_reason != "التزام كامل وصارم بالخطة والاستراتيجية" else 0.0
    
    new_trade = {
        "رقم الصفقة": total_trades + 1,
        "الأصل المالي": asset,
        "نوع الصفقة": trade_type,
        "النتيجة ($)": result_usd,
        "السبب السلوكي للخسارة": behavior_reason,
        "العائد المفقود ($)": waste_usd
    }
    
    st.session_state.trade_journal = pd.concat([st.session_state.trade_journal, pd.DataFrame([new_trade])], ignore_index=True)
    st.success("تم تسجيل الصفقة بنجاح وتحديث لوحة التحكم الفورية!")
    st.rerun()

# عرض جدول البيانات التفاعلي المحدث للعميل
if len(st.session_state.trade_journal) > 0:
    st.dataframe(st.session_state.trade_journal, use_container_width=True, hide_index=True)
    
    # زر إعادة تصفير البيانات للتجربة من جديد
    if st.button("🔄 إعادة تعيين وتطهير سجل البيانات"):
        st.session_state.trade_journal = pd.DataFrame(columns=[
            "رقم الصفقة", "الأصل المالي", "نوع الصفقة", "النتيجة ($)", "السبب السلوكي للخسارة", "العائد المفقود ($)"
        ])
        st.rerun()
else:
    st.info("لا توجد صفقات مسجلة اليوم حتى الآن. قم بإدخال صفقتك التجريبية الأولى في الأعلى لرؤية النظام يعمل حياً!")
