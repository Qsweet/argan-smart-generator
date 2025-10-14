# ============================================
# 🌿 Argan Package Smart Script Generator v4.0
# المطور: د. محمد القضاه
# وصف النسخة: نظام متكامل لإدارة إنتاج السكربتات
# ============================================

import streamlit as st
import openai
import json
import datetime
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="Argan Smart System", page_icon="🌿", layout="wide")

# ------------------------------
# 🧩 تحميل الملفات الأساسية
# ------------------------------
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

USERS = load_json("users.json")
OPTIONS = load_json("options.json")
LOGS = load_json("user_logs.json")

# مفتاح OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ------------------------------
# 🔐 شاشة تسجيل الدخول
# ------------------------------
def login_screen():
    st.markdown("<h1 style='text-align:center;'>🌿 نظام Argan Package</h1>", unsafe_allow_html=True)
    st.subheader("👋 يرجى تسجيل الدخول للوصول للنظام")
    username = st.text_input("اسم المستخدم:")
    password = st.text_input("كلمة المرور:", type="password")

    if st.button("تسجيل الدخول", use_container_width=True):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.user = username
            st.session_state.role = USERS[username]["role"]
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success(f"مرحبًا بك يا {username} 🌿")
            st.rerun()
        else:
            st.error("❌ بيانات الدخول غير صحيحة.")

# ------------------------------
# 🏠 الصفحة الرئيسية
# ------------------------------
def home():
    st.markdown("""
        <div style='text-align:center;'>
            <h1>🌿 نظام إدارة المحتوى الذكي لشركة Argan Package</h1>
            <p>تم تطويره بواسطة <b>د. محمد القضاه</b></p>
            <hr>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;'>اختر ما ترغب بالقيام به 👇</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 الدخول إلى إنتاج السيناريوهات", use_container_width=True):
            st.session_state.page = "generator"
            st.rerun()

# ------------------------------
# 🧠 صفحة توليد السكربتات
# ------------------------------
def generator():
    st.markdown("<h2>🧠 إنتاج السيناريوهات التسويقية</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        offer = st.selectbox("🎁 العرض:", OPTIONS["offer"])
        product = st.selectbox("🧴 المنتج:", OPTIONS["product"])
        platform = st.selectbox("📱 المنصة:", OPTIONS["platform"])
        scenario = st.selectbox("🎬 السيناريو:", OPTIONS["scenario"])
    with col2:
        shipping = st.selectbox("🚚 التوصيل:", OPTIONS["shipping"])
        gift = st.selectbox("🎁 الهدية:", OPTIONS["gift"])
        cashback = st.selectbox("💸 الكاش باك:", OPTIONS["cashback"])
        tone = st.selectbox("🎤 نبرة النص:", OPTIONS["tone"])

    inst = st.text_area("📝 تعليمات إضافية:")

    if st.button("✨ توليد النص", use_container_width=True):
        with st.spinner("جارٍ توليد النص..."):
            prompt = f"""
اكتب سكربت باللهجة السعودية لمنتج {product} على منصة {platform}.
السيناريو: {scenario}. النبرة: {tone}.
العرض: {offer}. التوصيل: {shipping}. الهدية: {gift}. الكاش باك: {cashback}.
تعليمات إضافية: {inst}.
"""
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت كاتب محتوى تسويقي سعودي محترف."},
                        {"role": "user", "content": prompt}
                    ]
                )
                script = response.choices[0].message.content.strip()
                st.success("✅ تم توليد السكربت بنجاح!")
                st.text_area("📜 النص الناتج:", script, height=250)
                save_log(st.session_state.user, product, scenario, platform)
            except Exception as e:
                st.error(f"حدث خطأ أثناء توليد النص: {e}")

# ------------------------------
# 💾 حفظ سجل النشاط
# ------------------------------
def save_log(user, product, scenario, platform):
    LOGS.append({
        "user": user,
        "product": product,
        "scenario": scenario,
        "platform": platform,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "جديد",
        "note": ""
    })
    with open("user_logs.json", "w", encoding="utf-8") as f:
        json.dump(LOGS, f, ensure_ascii=False, indent=2)

# ------------------------------
# 👤 صفحة حسابي
# ------------------------------
def account_page():
    st.markdown(f"<h2>👤 حسابي - {st.session_state.user}</h2>", unsafe_allow_html=True)
    user_logs = [x for x in LOGS if x["user"] == st.session_state.user]
    if not user_logs:
        st.info("لم تنتج أي سكربتات بعد.")
        return

    df = pd.DataFrame(user_logs)
    st.dataframe(df, use_container_width=True)

# ------------------------------
# 🧭 لوحة التحكم الإدارية
# ------------------------------
def admin_dashboard():
    st.markdown("<h2>🧭 لوحة التحكم الإدارية</h2>", unsafe_allow_html=True)

    if not LOGS:
        st.info("لا توجد بيانات بعد.")
        return

    df = pd.DataFrame(LOGS)
    users = list(USERS.keys())  # الآن يعرض كل المستخدمين المسجلين

    table = []
    for u in users:
        user_df = df[df["user"] == u]
        last_activity = user_df["timestamp"].max()
        total_scripts = len(user_df)
        last_product = user_df.iloc[-1]["product"]
        table.append({
            "المستخدم": u,
            "آخر نشاط": last_activity,
            "عدد السكربتات": total_scripts,
            "آخر منتج": last_product
        })

    st.table(pd.DataFrame(table))

    # إرسال توجيه
    st.markdown("---")
    st.subheader("✉️ إرسال توجيه لمستخدم:")
    target = st.selectbox("اختر المستخدم:", users)
    message = st.text_area("نص التوجيه:")
    if st.button("📤 إرسال التوجيه"):
        save_admin_message(target, message)
        st.success(f"✅ تم إرسال التوجيه إلى {target}")

# ------------------------------
# 💬 حفظ رسائل الأدمن
# ------------------------------
def save_admin_message(user, message):
    LOGS.append({
        "user": user,
        "product": "-",
        "scenario": "توجيه إداري",
        "platform": "-",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "رسالة من الأدمن",
        "note": message
    })
    with open("user_logs.json", "w", encoding="utf-8") as f:
        json.dump(LOGS, f, ensure_ascii=False, indent=2)

# ------------------------------
# 🚪 تسجيل الخروج
# ------------------------------
def logout():
    st.session_state.clear()
    st.success("تم تسجيل الخروج ✅")
    st.rerun()

# ------------------------------
# 🎛️ الواجهة الجانبية (الأزرار)
# ------------------------------
def sidebar():
    with st.sidebar:
        st.markdown(f"### 👋 مرحبًا {st.session_state.user}")
        if st.button("🏠 الرئيسية", use_container_width=True): st.session_state.page = "home"
        if st.button("🧠 توليد السيناريوهات", use_container_width=True): st.session_state.page = "generator"
        if st.button("👤 حسابي", use_container_width=True): st.session_state.page = "account"
        if st.session_state.role == "admin":
            if st.button("🧭 لوحة التحكم", use_container_width=True): st.session_state.page = "admin"
        if st.button("🚪 تسجيل الخروج", use_container_width=True): logout()

# ------------------------------
# 🚀 النظام الرئيسي
# ------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar()
    page = st.session_state.get("page", "home")
    if page == "home": home()
    elif page == "generator": generator()
    elif page == "account": account_page()
    elif page == "admin" and st.session_state.role == "admin": admin_dashboard()

