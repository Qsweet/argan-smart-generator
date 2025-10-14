# ============================================
# 🌿 Argan Package Smart CMS v6
# الكاتب: د. محمد القضاه
# الإصدار: تصميم واجهة UX/UI فاخرة
# ============================================

import streamlit as st
import pandas as pd
import openai
import datetime
import json
import csv
from pathlib import Path

# ----------------------------- #
# إعداد الصفحة
# ----------------------------- #
st.set_page_config(page_title="Argan Smart CMS", page_icon="🌿", layout="wide")

# ----------------------------- #
# تخصيص الستايل العام (CSS)
# ----------------------------- #
st.markdown("""
    <style>
        body {
            background-color: #FAF7F0;
            font-family: 'Tajawal', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #2F3E2F;
            font-weight: 700;
        }
        .stButton button {
            background-color: #2F3E2F;
            color: white;
            border-radius: 10px;
            padding: 0.7rem 1.5rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #C5A572;
            color: #2F3E2F;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div>select {
            border-radius: 10px;
            border: 1px solid #C5A572;
        }
        .main-title {
            text-align: center;
            font-size: 2.2rem;
            color: #2F3E2F;
            margin-top: 40px;
        }
        .subtitle {
            text-align: center;
            color: #C5A572;
            font-size: 1.1rem;
            margin-bottom: 40px;
        }
        .card {
            background-color: white;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #888;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------- #
# تحميل البيانات
# ----------------------------- #
with open("users.json", "r", encoding="utf-8") as f:
    USERS = json.load(f)

with open("options.json", "r", encoding="utf-8") as f:
    options = json.load(f)

openai.api_key = st.secrets["OPENAI_API_KEY"]
Path("scenarios_log.csv").touch(exist_ok=True)

# ----------------------------- #
# وظائف مساعدة
# ----------------------------- #
def get_user_role(username):
    data = USERS.get(username)
    if isinstance(data, dict):
        return data.get("role", "user")
    return "user"

def log_scenario(user, product, scenario, platform):
    with open("scenarios_log.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, product, scenario, platform, "جديد", "جديد", "", "", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def get_scenarios(user):
    try:
        df = pd.read_csv("scenarios_log.csv", names=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])
        return df[df["user"] == user]
    except:
        return pd.DataFrame(columns=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])

# ----------------------------- #
# شاشة الدخول
# ----------------------------- #
def login_screen():
    st.markdown("<h1 class='main-title'>🌿 نظام أرجان الذكي</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>يرجى إدخال بيانات الدخول</p>", unsafe_allow_html=True)

    username = st.text_input("👤 اسم المستخدم")
    password = st.text_input("🔑 كلمة المرور", type="password")

    if st.button("تسجيل الدخول"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["user"] = username
            st.session_state["page"] = "home"
            st.success(f"مرحباً {username} 👋")
            st.rerun()
        else:
            st.error("❌ بيانات الدخول غير صحيحة.")

# ----------------------------- #
# الصفحة الرئيسية
# ----------------------------- #
def home_screen():
    st.markdown("<h1 class='main-title'>نظام إدارة المحتوى الذكي لشركة أرجان باكيج</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>إعداد: د. محمد القضاه</p>", unsafe_allow_html=True)

    st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
    if st.button("🚀 إنتاج السيناريوهات", use_container_width=True):
        st.session_state["page"] = "generator"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- #
# صفحة توليد السيناريوهات
# ----------------------------- #
def generator_screen():
    st.markdown("<h2>🧠 إنتاج السيناريوهات التسويقية</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        offer = st.selectbox("🎁 العرض الخاص:", options["offer"])
        product = st.selectbox("🧴 المنتج:", options["product"])
        platform = st.selectbox("📱 المنصة:", options["platform"])
        scenario = st.selectbox("🎬 نوع السيناريو:", options["scenario"])
    with col2:
        shipping = st.selectbox("🚚 التوصيل:", options["shipping"])
        gift = st.selectbox("🎁 الهدية:", options["gift"])
        cashback = st.selectbox("💸 الكاش باك:", options["cashback"])
        tone = st.selectbox("🎤 نبرة النص:", options["tone"])

    custom_inst = st.text_area("📝 تعليمات إضافية:")

    if st.button("✨ توليد السكربت الآن"):
        with st.spinner("جارٍ توليد النص..."):
            prompt = f"""
اكتب سكربت باللهجة السعودية لمنتج {product} على منصة {platform}.
السيناريو: {scenario}.
نبرة النص: {tone}.
العرض: {offer} | التوصيل: {shipping} | الهدية: {gift} | الكاش باك: {cashback}.
تعليمات إضافية: {custom_inst}.
"""
            try:
                res = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت كاتب محتوى تسويقي سعودي محترف."},
                        {"role": "user", "content": prompt}
                    ]
                )
                script = res.choices[0].message.content.strip()
                st.text_area("📜 النص الناتج:", script, height=250)
                log_scenario(st.session_state["user"], product, scenario, platform)
                st.success("✅ تم حفظ السيناريو في حسابك.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# ----------------------------- #
# صفحة حسابي
# ----------------------------- #
def account_screen():
    st.markdown("<h2>👤 حسابي</h2>", unsafe_allow_html=True)
    df = get_scenarios(st.session_state["user"])
    if df.empty:
        st.info("لم تنتج أي سيناريوهات بعد.")
        return
    st.dataframe(df, use_container_width=True)

# ----------------------------- #
# واجهة التنقل
# ----------------------------- #
if "user" not in st.session_state:
    login_screen()
    st.stop()

top1, top2, top3 = st.columns([6,1,1])
with top2:
    if st.button("👤 حسابي"):
        st.session_state["page"] = "account"
        st.rerun()
with top3:
    if get_user_role(st.session_state["user"]) == "admin":
        if st.button("📊 لوحة التحكم"):
            st.session_state["page"] = "admin"
            st.rerun()
    if st.button("🚪 خروج"):
        st.session_state.clear()
        st.rerun()

page = st.session_state.get("page", "home")
if page == "home": home_screen()
elif page == "generator": generator_screen()
elif page == "account": account_screen()
