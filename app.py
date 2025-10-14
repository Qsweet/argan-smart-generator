# ============================================
# 🌿 Argan Package Smart CMS System v5
# الكاتب: د. محمد القضاه
# المميزات:
# - صفحة رئيسية أنيقة
# - صفحة توليد السيناريوهات
# - لوحة تحكم إدارية
# - صفحة "حسابي" لكل مستخدم
# ============================================

import streamlit as st
import pandas as pd
import openai
import datetime
import json
import csv
from pathlib import Path

# إعداد الصفحة
st.set_page_config(page_title="Argan Smart CMS", page_icon="🌿", layout="wide")

# تحميل المستخدمين
with open("users.json", "r", encoding="utf-8") as f:
    USERS = json.load(f)

# تحميل القوائم من options.json
with open("options.json", "r", encoding="utf-8") as f:
    options = json.load(f)

openai.api_key = st.secrets["OPENAI_API_KEY"]

# إنشاء ملفات السجلات
Path("scenarios_log.csv").touch(exist_ok=True)
Path("sessions_log.csv").touch(exist_ok=True)

# ----------------------------- #
# وظائف مساعدة
# ----------------------------- #
def log_scenario(user, product, scenario, platform):
    with open("scenarios_log.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, product, scenario, platform, "جديد", "جديد", "", "", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def get_user_role(username):
    data = USERS.get(username)
    if isinstance(data, dict):
        return data.get("role", "user")
    return "user"

def get_scenarios(user):
    try:
        df = pd.read_csv("scenarios_log.csv", names=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])
        return df[df["user"] == user]
    except:
        return pd.DataFrame(columns=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])

# ----------------------------- #
# تسجيل الدخول
# ----------------------------- #
def login_screen():
    st.title("🔒 تسجيل الدخول إلى نظام أرجان باكيج")
    username = st.text_input("👤 اسم المستخدم:")
    password = st.text_input("🔑 كلمة المرور:", type="password")

    if st.button("تسجيل الدخول"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["user"] = username
            st.session_state["page"] = "home"
            st.success(f"🌿 مرحبًا بك يا {username}")
            st.rerun()
        else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")

# ----------------------------- #
# الصفحة الرئيسية
# ----------------------------- #
def home_screen():
    st.title("🌿 نظام إدارة المحتوى الذكي لشركة أرجان باكيج")
    st.markdown("### 👋 أهلاً وسهلاً بكم في نظام إدارة المحتوى الذكي لشركة **Argan Package**")
    st.markdown("##### إعداد: د. محمد القضاه")

    st.markdown("---")
    if st.button("🚀 إنتاج السيناريوهات", use_container_width=True):
        st.session_state["page"] = "generator"
        st.rerun()

# ----------------------------- #
# صفحة توليد السيناريوهات
# ----------------------------- #
def generator_screen():
    st.title("🧠 إنتاج السيناريوهات التسويقية")
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
                st.success("✅ تم حفظ السيناريو وإضافته إلى حسابك.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# ----------------------------- #
# صفحة حسابي (My Account)
# ----------------------------- #
def account_screen():
    st.title("👤 حسابي")
    df = get_scenarios(st.session_state["user"])

    if df.empty:
        st.info("⚠️ لم يتم إنتاج أي سيناريوهات بعد.")
        return

    st.dataframe(df, use_container_width=True)

    st.markdown("### ✏️ تحديث الحالة أو التفاصيل:")

    selected_index = st.selectbox("اختر السيناريو للتحديث:", df.index.tolist())
    if selected_index is not None:
        row = df.loc[selected_index]

        action = st.selectbox("📍 التنفيذ المطلوب:", ["جديد", "اعادة مونتاج مع اضافه", "اعادة مونتاج", "مونتاج خارجي", "تصوير ماجد"], index=0)
        status = st.selectbox("📦 حالة السيناريو:", ["جاري البحث عن مؤثر", "تم اختيار المؤثر", "تم ارسال المنتجات", "بانتظار استلام المنتجات", "تم ارسال الفيديو للمونتاج", "جاري المونتاج", "بانتظار استلام تعليمات", "بانتظار تجهيز التصوير", "تم اكتمال الفيديو"], index=0)
        delivery_date = st.date_input("📅 تاريخ التسليم المطلوب:", value=datetime.date.today())

        video_link = ""
        if status == "تم اكتمال الفيديو":
            video_link = st.text_input("🔗 رابط العمل النهائي (Dropbox):")

        if st.button("💾 حفظ التعديلات"):
            df.loc[selected_index, "required_action"] = action
            df.loc[selected_index, "status"] = status
            df.loc[selected_index, "delivery_date"] = delivery_date
            df.loc[selected_index, "video_link"] = video_link

            df.to_csv("scenarios_log.csv", header=False, index=False)
            st.success("✅ تم تحديث البيانات بنجاح.")

# ----------------------------- #
# واجهة الإدمن
# ----------------------------- #
def admin_screen():
    st.title("👑 لوحة التحكم الإدارية - Argan Package")

    try:
        df = pd.read_csv("scenarios_log.csv", names=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])
        st.dataframe(df, use_container_width=True)
    except:
        st.warning("لا يوجد بيانات بعد.")

# ----------------------------- #
# الشريط العلوي (Navbar)
# ----------------------------- #
if "user" not in st.session_state:
    login_screen()
    st.stop()

col1, col2, col3 = st.columns([5, 1, 1])
with col2:
    if st.button("👤 حسابي"):
        st.session_state["page"] = "account"
        st.rerun()
with col3:
    if get_user_role(st.session_state["user"]) == "admin":
        if st.button("📊 لوحة التحكم"):
            st.session_state["page"] = "admin"
            st.rerun()
    if st.button("🚪 خروج"):
        st.session_state.clear()
        st.rerun()

# ----------------------------- #
# نظام التنقل بين الصفحات
# ----------------------------- #
page = st.session_state.get("page", "home")

if page == "home":
    home_screen()
elif page == "generator":
    generator_screen()
elif page == "account":
    account_screen()
elif page == "admin":
    admin_screen()
