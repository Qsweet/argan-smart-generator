# ============================================
# 🌿 Argan Package Smart Script Generator v3.0
# الكاتب: د. محمد القضاه
# ============================================

import streamlit as st
import openai
import json
import datetime

# إعداد الواجهة
st.set_page_config(page_title="Argan Package Smart Script Generator", page_icon="🌿", layout="centered")

# تحميل الخيارات
with open("options.json", "r", encoding="utf-8") as f:
    options = json.load(f)

# مفتاح OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# حسابات الدخول
# USERS = {...}
with open("users.json", "r", encoding="utf-8") as f:
    USERS = json.load(f)


# ==============================
# 🔐 شاشة تسجيل الدخول
# ==============================
def login_screen():
    st.title("🌿 نظام Argan Package")
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

# ==============================
# 🧠 صفحة توليد السكربتات
# ==============================
def generator():
    st.markdown("<h2>🧠 إنتاج السيناريوهات التسويقية</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        offer = st.selectbox("🎁 العرض:", options["offer"])
        category = st.selectbox("🗂️ الفئة:", options["category"])
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

    if st.button("✨ توليد النص", use_container_width=True):
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
                        {"role": "system", "content": "أنت كاتب محتوى تسويقي سعودي محترف مختص في سناب شات وتيك توك."},
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
# 🧭 لوحة التحكم الإدارية
# ==============================
def admin_dashboard():
    st.markdown("<h2>🧭 لوحة التحكم الإدارية</h2>", unsafe_allow_html=True)
    try:
        with open("user_logs.txt", "r", encoding="utf-8") as f:
            logs = f.readlines()
        if logs:
            st.write("### أحدث العمليات:")
            for line in reversed(logs[-15:]):
                st.write("🟢 " + line.strip())
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

    st.markdown("<h3 style='text-align:center;'>اختر ما ترغب بالقيام به 👇</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 الدخول إلى إنتاج السيناريوهات", use_container_width=True):
            st.session_state.page = "generator"
            st.rerun()

# ==============================
# 🚪 تسجيل الخروج
# ==============================
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.page = "login"
    st.success("تم تسجيل الخروج بنجاح ✅")
    st.rerun()

# ==============================
# 🔄 النظام الرئيسي
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# 🔹 واجهة المستخدم
if not st.session_state.logged_in:
    login_screen()
else:
    role = st.session_state.role
    page = st.session_state.page

    # شريط جانبي
    st.sidebar.title(f"👋 مرحبًا، {st.session_state.user}")
    menu = ["🏠 الرئيسية", "🧠 توليد السيناريوهات", "👤 حسابي"]
    if role == "admin":
        menu.append("🧭 لوحة التحكم")
    menu.append("🚪 تسجيل الخروج")

    choice = st.sidebar.radio("انتقل إلى:", menu)

    # تحديد الصفحة
    if choice == "🏠 الرئيسية":
        st.session_state.page = "home"
        home()
    elif choice == "🧠 توليد السيناريوهات" or st.session_state.page == "generator":
        generator()
    elif choice == "🧭 لوحة التحكم" and role == "admin":
        admin_dashboard()
    elif choice == "🚪 تسجيل الخروج":
        logout()

