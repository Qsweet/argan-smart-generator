# ============================================
# 🌿 Argan Package Smart Script Generator v4
# الكاتب: د. محمد القضاه
# الميزة الجديدة: لوحة تحكم للإدمن + تتبع الجلسات والسكربتات
# ============================================

import streamlit as st
import openai
import json
import datetime
import csv
import pandas as pd
from pathlib import Path

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Argan Smart Generator", page_icon="🌿", layout="wide")

# -----------------------------
# تحميل المستخدمين
# -----------------------------
try:
    with open("users.json", "r", encoding="utf-8") as f:
        USERS = json.load(f)
except Exception as e:
    st.error(f"❌ خطأ في قراءة users.json: {e}")
    st.stop()

# -----------------------------
# تحميل القوائم من options.json
# -----------------------------
try:
    with open("options.json", "r", encoding="utf-8") as f:
        options = json.load(f)
except Exception as e:
    st.error(f"❌ خطأ في قراءة options.json: {e}")
    st.stop()

# -----------------------------
# مفتاح OpenAI
# -----------------------------
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("⚠️ لم يتم العثور على مفتاح OpenAI في Secrets.")
    st.stop()

# -----------------------------
# ملفات السجلات (logs)
# -----------------------------
Path("sessions_log.csv").touch(exist_ok=True)
Path("scripts_log.csv").touch(exist_ok=True)

# -----------------------------
# وظائف مساعدة
# -----------------------------
def log_session(user, action):
    """تسجيل الدخول والخروج"""
    with open("sessions_log.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, action, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def log_script(user, product, scenario, platform):
    """تسجيل السكربت"""
    with open("scripts_log.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, product, scenario, platform, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def get_user_role(username):
    return USERS[username].get("role", "user")

# -----------------------------
# شاشة تسجيل الدخول
# -----------------------------
def login_screen():
    st.title("🔒 تسجيل الدخول إلى Argan Package System")
    st.markdown("👇 يرجى إدخال بيانات الدخول الخاصة بك للمتابعة")

    username = st.text_input("👤 اسم المستخدم:")
    password = st.text_input("🔑 كلمة المرور:", type="password")

    if st.button("تسجيل الدخول"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["user"] = username
            st.session_state["login_time"] = datetime.datetime.now()
            log_session(username, "login")
            st.success(f"🌿 مرحبًا بك يا {username}")
            st.rerun()
        else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")

# -----------------------------
# واجهة تسجيل الدخول
# -----------------------------
if "user" not in st.session_state:
    login_screen()
    st.stop()

# -----------------------------
# تسجيل الخروج
# -----------------------------
if st.sidebar.button("🚪 تسجيل الخروج"):
    log_session(st.session_state["user"], "logout")
    st.session_state.clear()
    st.rerun()

# -----------------------------
# صفحة الأدمن
# -----------------------------
if get_user_role(st.session_state["user"]) == "admin" and st.sidebar.checkbox("📊 فتح لوحة التحكم الإدارية"):
    st.title("👑 لوحة تحكم Argan Package Admin")

    # تحميل البيانات
    try:
        sessions = pd.read_csv("sessions_log.csv", names=["user", "action", "timestamp"])
        scripts = pd.read_csv("scripts_log.csv", names=["user", "product", "scenario", "platform", "timestamp"])
    except Exception:
        st.warning("⚠️ لم يتم توليد أي سجلات بعد.")
        st.stop()

    # تحويل الوقت
    sessions["timestamp"] = pd.to_datetime(sessions["timestamp"])

    # حساب آخر دخول ومجموع المدد
    summary = []
    for user in sessions["user"].unique():
        user_sessions = sessions[sessions["user"] == user]
        logins = user_sessions[user_sessions["action"] == "login"]
        logouts = user_sessions[user_sessions["action"] == "logout"]

        last_login = logins["timestamp"].max() if not logins.empty else None
        duration = None

        if not logouts.empty and not logins.empty:
            last_logout = logouts["timestamp"].max()
            duration = (last_logout - last_login).seconds / 60 if last_logout > last_login else 0

        total_scripts = scripts[scripts["user"] == user]
        total_time = round(duration or 0, 2)
        total_products = ", ".join(total_scripts["product"].unique()) if not total_scripts.empty else "-"
        total_scenarios = ", ".join(total_scripts["scenario"].unique()) if not total_scripts.empty else "-"

        summary.append([user, str(last_login), f"{total_time} دقيقة", len(total_scripts), total_products, total_scenarios])

    df_summary = pd.DataFrame(summary, columns=[
        "المستخدم", "آخر دخول", "مدة آخر جلسة", "عدد السكربتات", "المنتجات", "السيناريوهات"
    ])

    st.dataframe(df_summary, use_container_width=True)
    st.download_button("📥 تحميل التقرير كـ CSV", df_summary.to_csv(index=False), "admin_report.csv")

    st.stop()

# -----------------------------
# واجهة المستخدم العادي
# -----------------------------
st.title("🌿 Argan Package Smart Script Generator")
st.markdown("##### ✨ نظام توليد سكربتات تسويقية باللهجة السعودية 🇸🇦")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    offer = st.selectbox("🎁 العرض الخاص:", options["offer"])
    product = st.selectbox("🧴 المنتج:", options["product"])
    platform = st.selectbox("📱 المنصة:", options["platform"])
    scenario = st.selectbox("🎬 نوع السيناريو:", options["scenario"])
with col2:
    shipping = st.selectbox("🚚 التوصيل:", options["shipping"])
    gift = st.selectbox("🎁 الهدية:", options["gift"])
    cashback = st.selectbox("💸 الكاش باك (اختياري):", options["cashback"])
    tone = st.selectbox("🎤 نبرة النص:", options["tone"])

custom_inst = st.text_area("📝 تعليمات إضافية:", placeholder="مثلاً: اجعل النص قصيرًا باللهجة السعودية")

if st.button("🚀 توليد السكربت الآن"):
    if not custom_inst.strip():
        st.error("⚠️ الرجاء كتابة تعليمات إضافية.")
    else:
        with st.spinner("⚙️ جاري إنشاء السكربت..."):
            prompt = f"""
اكتب سكربت تسويقي باللهجة السعودية لمنتج "{product}" مناسب لمنصة {platform}.
نوع السيناريو: {scenario}.
نبرة النص: {tone}.

🎁 العرض: {offer}
🚚 التوصيل: {shipping}
🎁 الهدية: {gift}
💸 الكاش باك: {cashback}
📝 تعليمات إضافية: {custom_inst}
"""

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت كاتب محتوى سعودي محترف."},
                        {"role": "user", "content": prompt}
                    ]
                )
                script = response.choices[0].message.content.strip()
                log_script(st.session_state["user"], product, scenario, platform)
                st.success("✅ تم توليد السكربت بنجاح!")
                st.text_area("📜 السكربت الناتج:", script, height=250)
                st.download_button("📥 تحميل النص", script, f"{product}_script.txt")

            except Exception as e:
                st.error(f"❌ خطأ أثناء الاتصال بـ OpenAI: {e}")
