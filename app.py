# ============================================
# 🌿 Argan Package Smart Script Generator v3
# الكاتب: د. محمد القضاه
# الوصف: نظام توليد سكربتات تسويقية باللهجة السعودية
# الميزة: دعم تسجيل الدخول متعدد المستخدمين
# ============================================

import streamlit as st
import openai
import json
import datetime

# -----------------------------
# 🟢 إعداد الصفحة العامة
# -----------------------------
st.set_page_config(
    page_title="Argan Package Script Generator",
    page_icon="🌿",
    layout="centered"
)

# -----------------------------
# 🔹 تحميل بيانات المستخدمين من ملف users.json
# -----------------------------
try:
    with open("users.json", "r", encoding="utf-8") as f:
        USERS = json.load(f)
except FileNotFoundError:
    st.error("❌ لم يتم العثور على ملف users.json. تأكد من رفعه مع التطبيق.")
    st.stop()

# -----------------------------
# 🔑 نظام تسجيل الدخول
# -----------------------------
def login_screen():
    st.title("🔒 تسجيل الدخول إلى Argan Package System")
    st.markdown("يرجى إدخال بيانات الدخول الخاصة بك للمتابعة 👇")

    username = st.text_input("👤 اسم المستخدم:")
    password = st.text_input("🔑 كلمة المرور:", type="password")

    if st.button("تسجيل الدخول"):
        if username in USERS and USERS[username] == password:
            st.session_state["user"] = username
            st.success(f"مرحبًا بك يا {username} 🌿")
            st.experimental_rerun()
        else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")

# التحقق من حالة الجلسة
if "user" not in st.session_state:
    login_screen()
    st.stop()

# -----------------------------
# 🧭 شريط جانبي (Sidebar)
# -----------------------------
st.sidebar.markdown(f"👋 **مرحبًا، {st.session_state['user']}**")
st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
    del st.session_state["user"]
    st.experimental_rerun()

# -----------------------------
# 🔹 تحميل القوائم من ملف options.json
# -----------------------------
try:
    with open("options.json", "r", encoding="utf-8") as f:
        options = json.load(f)
except FileNotFoundError:
    st.error("❌ لم يتم العثور على ملف options.json. تأكد من رفعه مع التطبيق.")
    st.stop()

# -----------------------------
# 🔑 مفتاح OpenAI من Streamlit Secrets
# -----------------------------
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("⚠️ لم يتم العثور على مفتاح OpenAI في Secrets. أضفه أولاً ثم أعد التشغيل.")
    st.stop()

# -----------------------------
# 🌿 واجهة التطبيق
# -----------------------------
st.title("🌿 Argan Package Smart Script Generator")
st.markdown("##### ✨ نظام توليد سكربتات تسويقية باللهجة السعودية 🇸🇦")
st.markdown("---")

# -----------------------------
# 🧩 إدخالات المستخدم
# -----------------------------
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

custom_inst = st.text_area(
    "📝 تعليمات إضافية:",
    placeholder="مثلاً: اجعل النص قصيرًا، باللهجة السعودية، وابدأ بجملة مشوقة..."
)

st.markdown("---")

# -----------------------------
# 🧠 زر توليد السكربت
# -----------------------------
if st.button("🚀 توليد السكربت الآن"):
    if not custom_inst.strip():
        st.error("⚠️ الرجاء كتابة تعليمات إضافية لبناء السكربت.")
    else:
        with st.spinner("⚙️ جاري إنشاء السكربت..."):
            # بناء البرومت الذكي
            prompt = f"""
اكتب سكربت تسويقي باللهجة السعودية لمنتج "{product}" مناسب لمنصة {platform}.
نوع السيناريو: {scenario}.
نبرة النص: {tone}.

🎁 العرض: {offer}
🚚 التوصيل: {shipping}
🎁 الهدية: {gift}
💸 الكاش باك: {cashback}
📝 تعليمات إضافية: {custom_inst}

✳️ المتطلبات:
- سكربت قصير لا يتجاوز 30 ثانية.
- يبدأ بجملة قوية تشد الانتباه.
- منطقي ومترابط.
- لهجة سعودية طبيعية وواثقة.
- ختام بدعوة للفعل مناسبة للمنصة ({platform}).
"""

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "أنت كاتب محتوى سعودي محترف متخصص في صناعة سكربتات تسويقية قصيرة باللهجة السعودية الواقعية والمنطقية والمتوافقة مع سياسات المنصات."
                        },
                        {"role": "user", "content": prompt}
                    ]
                )

                script = response.choices[0].message.content.strip()

                # -----------------------------
                # 🧾 عرض النتيجة
                # -----------------------------
                st.success("✅ تم توليد السكربت بنجاح!")
                st.markdown("### 📜 السكربت الناتج:")
                st.text_area("النص النهائي:", script, height=300)

                # زر تحميل النص
                st.download_button(
                    "📥 تحميل النص كملف TXT",
                    data=script,
                    file_name=f"{product}_script.txt"
                )

                # توقيع احترافي
                st.markdown("---")
                st.caption(
                    f"تم إعداد هذا النظام بواسطة د. محمد القضاه • Argan Package • {datetime.datetime.now().strftime('%Y/%m/%d %H:%M')}"
                )

            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء الاتصال بـ OpenAI:\n\n{e}")
