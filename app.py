# ============================================
# 🌿 Argan Package Smart Script Generator v2.1
# الكاتب: د. محمد القضاه
# ============================================

import streamlit as st
import openai
import json
import datetime

# إعدادات الواجهة
st.set_page_config(page_title="Argan Package Smart Script Generator", page_icon="🌿", layout="centered")

# تحميل البيانات من options.json
with open("options.json", "r", encoding="utf-8") as f:
    options = json.load(f)

# مفتاح OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ملف تسجيل الدخول التجريبي
USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "qudah": {"password": "1234", "role": "user"},
}

# ==============================
# 🔐 شاشة تسجيل الدخول
# ==============================
def login_screen():
    st.title("🌿 نظام Argan Package")
    st.subheader("👋 يرجى تسجيل الدخول للوصول للنظام")
    
    username = st.text_input("اسم المستخدم:")
    password = st.text_input("كلمة المرور:", type="password")

    if st.button("تسجيل الدخول"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.user = username
            st.session_state.role = USERS[username]["role"]
            st.session_state.logged_in = True
            st.success(f"مرحبًا بك يا {username} 🌿")
            st.rerun()
        else:
            st.error("❌ بيانات الدخول غير صحيحة.")

# ==============================
# 🧠 صفحة إنتاج السيناريوهات
# ==============================
def generator():
    st.markdown("<h2>🧠 إنتاج السيناريوهات التسويقية</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        offer = st.selectbox("🎁 العرض:", options["offer"])
        category = st.selectbox("🗂️ الفئة:", options["category"])
        
        # ✅ عرض المنتجات التابعة للفئة المختارة
        selected_products = options["products"].get(category, [])
        if selected_products:
            product = st.selectbox("🧴 المنتج:", selected_products)
        else:
            st.warning("⚠️ لا توجد منتجات في هذه الفئة.")
            return
        
        platform = st.selectbox("📱 المنصة:", options["platform"])
        scenario = st.selectbox("🎬 السيناريو:", options["scenario"])
    
    with c2:
        shipping = st.selectbox("🚚 التوصيل:", options["shipping"])
        gift = st.selectbox("🎁 الهدية:", options["gift"])
        cashback = st.selectbox("💸 الكاش باك:", options["cashback"])
        tone = st.selectbox("🎤 نبرة النص:", options["tone"])

    inst = st.text_area("📝 تعليمات إضافية:")

    if st.button("✨ توليد النص"):
        with st.spinner("جارٍ توليد النص..."):
            prompt = f"""
اكتب سكربت باللهجة السعودية لمنتج {product} من فئة {category} على منصة {platform} بأسلوب {tone}.
السيناريو: {scenario}.
العرض: {offer}.
التوصيل: {shipping}.
الهدية: {gift}.
الكاش باك: {cashback}.
تعليمات إضافية: {inst}.
"""
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت كاتب محتوى تسويقي سعودي محترف مختص في السناب والتيك توك."},
                        {"role": "user", "content": prompt}
                    ]
                )
                script = response.choices[0].message.content.strip()
                
                st.success("✅ تم توليد السكربت بنجاح!")
                st.text_area("📜 النص الناتج:", script, height=250)
                save_user_log(st.session_state.user, product, scenario, platform)
            
            except Exception as e:
                st.error(f"حدث خطأ أثناء توليد النص: {e}")

# ==============================
# 🧾 حفظ سجل المستخدم
# ==============================
def save_user_log(user, product, scenario, platform):
    with open("user_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {user} | {product} | {scenario} | {platform}\n")

# ==============================
# ⚙️ لوحة التحكم (للأدمن فقط)
# ==============================
def admin_dashboard():
    st.markdown("## 🧭 لوحة التحكم الإدارية")
    try:
        with open("user_logs.txt", "r", encoding="utf-8") as f:
            logs = f.readlines()
        if logs:
            st.write("### السجلات الأخيرة:")
            for line in reversed(logs[-10:]):
                st.write(line.strip())
        else:
            st.info("لا توجد بيانات بعد.")
    except FileNotFoundError:
        st.info("لم يتم إنشاء سجل بعد.")

# ==============================
# 🏠 الصفحة الرئيسية
# ==============================
def home():
    st.markdown("""
        <div style='text-align:center;'>
            <h1>🌿 نظام إدارة المحتوى الذكي لشركة Argan Package</h1>
            <p>تم تطويره بواسطة <b>د. محمد القضاه</b></p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("generator", label="🚀 إنتاج السيناريوهات")

# ==============================
# 🚪 تسجيل الخروج
# ==============================
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.success("تم تسجيل الخروج بنجاح ✅")
    st.rerun()

# ==============================
# 🔄 النظام الرئيسي
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
else:
    user = st.session_state.user
    role = st.session_state.role

    st.sidebar.title("🌿 القائمة")
    page = st.sidebar.radio("اختر الصفحة:", ["🏠 الرئيسية", "🧠 توليد السيناريوهات", "👤 حسابي"] + (["🧭 لوحة التحكم"] if role == "admin" else []) + ["🚪 تسجيل الخروج"])

    if page == "🏠 الرئيسية":
        home()
    elif page == "🧠 توليد السيناريوهات":
        generator()
    elif page == "🧭 لوحة التحكم" and role == "admin":
        admin_dashboard()
    elif page == "🚪 تسجيل الخروج":
        logout()
