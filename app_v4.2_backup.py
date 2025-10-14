# ============================================
# 🌿 Argan Package Smart Script Generator v4.2
# المطور: د. محمد القضاه
# الوصف: تم إضافة إدارة الحملات (Campaigns) + خيارات الحذف والتصنيف للمستخدم
# تاريخ التعديل: 2025-10-14
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
CAMPAIGNS = load_json("campaigns.json")  # ✅ ملف الحملات الجديد

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
    
    sfda_compliance = st.radio(
        "📜 هل تريد أن يكون السيناريو خاضعًا لاشتراطات هيئة الغذاء والدواء السعودية؟",
        ["لا", "نعم"],
        horizontal=True
    )

    inst = st.text_area("📝 تعليمات إضافية:")

    if st.button("✨ توليد النص", use_container_width=True):
        with st.spinner("جارٍ توليد النص..."):
            if sfda_compliance == "نعم":
                sfda_rules = """
                ✅ طبق اشتراطات هيئة الغذاء والدواء السعودية (SFDA):
                - يمنع أي ادعاء طبي مثل "يعالج"، "يشفي"، "يقضي على"، "يوقف"، "يمنع"، "يصلح"، "يُجدد".
                - استخدم بدائل قانونية مثل: "يساعد"، "يساهم"، "يدعم"، "يعزز"، "يمنح إحساسًا بـ".
                - لا تُظهر المنتج كعلاج أو بديل طبي.
                - لا تستخدم صور أو عبارات توحي بنتائج مضمونة أو قبل/بعد.
                - لا تقلل من شأن المنافسين أو تدّعي أن المنتج "الأفضل".
                - لا تذكر أمراض، أعضاء جسمية، أو مصطلحات طبية.
                - ركّز على التجربة الحسية والفوائد الواقعية.
                """
            else:
                sfda_rules = ""

            prompt = f"""
اكتب سكربت باللهجة السعودية لمنتج {product} على منصة {platform}.
السيناريو: {scenario}. النبرة: {tone}.
العرض: {offer}. التوصيل: {shipping}. الهدية: {gift}. الكاش باك: {cashback}.
تعليمات إضافية: {inst}.
{sfda_rules}
"""
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت كاتب محتوى تسويقي سعودي محترف ومطلع على سياسات الإعلانات لمنصات التواصل الاجتماعي."},
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
        "note": "",
        "campaign": "لا توجد حملة"  # ✅ جديد
    })
    with open("user_logs.json", "w", encoding="utf-8") as f:
        json.dump(LOGS, f, ensure_ascii=False, indent=2)

# ------------------------------
# 👤 صفحة حسابي
# ------------------------------
def account_page():
    st.markdown(f"<h2>👤 حسابي - {st.session_state.user}</h2>", unsafe_allow_html=True)

    admin_msgs = [
        x for x in LOGS
        if x["user"] == st.session_state.user and x["status"] == "رسالة من الأدمن"
    ]
    if admin_msgs:
        latest_msg = admin_msgs[-1]
        st.warning(f"📩 لديك رسالة جديدة من الأدمن بتاريخ {latest_msg['timestamp']}:\n\n**{latest_msg['note']}**")

    user_logs = [x for x in LOGS if x["user"] == st.session_state.user]
    if not user_logs:
        st.info("لم تُنتج أي سكربتات بعد.")
        return

    df = pd.DataFrame(user_logs)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("🧭 إدارة السكربتات:")

    for i, row in enumerate(user_logs):
        with st.expander(f"🎬 {row['product']} | {row['scenario']} | {row['timestamp']}"):
            col1, col2 = st.columns([2, 1])

            with col1:
                selected_campaign = st.selectbox(
                    "اختر الحملة الإعلانية:",
                    ["لا توجد حملة"] + CAMPAIGNS,
                    index=(["لا توجد حملة"] + CAMPAIGNS).index(row.get("campaign", "لا توجد حملة")),
                    key=f"campaign_{i}"
                )
                if st.button(f"💾 حفظ التعديل #{i}"):
                    LOGS[i]["campaign"] = selected_campaign
                    with open("user_logs.json", "w", encoding="utf-8") as f:
                        json.dump(LOGS, f, ensure_ascii=False, indent=2)
                    st.success("✅ تم حفظ التعديل بنجاح.")

            with col2:
                if st.button(f"🗑️ حذف هذا السكربت #{i}"):
                    LOGS.remove(row)
                    with open("user_logs.json", "w", encoding="utf-8") as f:
                        json.dump(LOGS, f, ensure_ascii=False, indent=2)
                    st.warning("🚮 تم حذف هذا السكربت.")
                    st.rerun()

# ------------------------------
# 🧭 لوحة التحكم الإدارية
# ------------------------------
def admin_dashboard():
    st.markdown("<h2>🧭 لوحة التحكم الإدارية</h2>", unsafe_allow_html=True)

    df = pd.DataFrame(LOGS)
    if df.empty:
        st.info("لا توجد بيانات بعد.")
        return

    users = list(USERS.keys())
    table = []

    for u in users:
        user_df = df[df["user"] == u]
        if not user_df.empty:
            last_activity = user_df["timestamp"].max()
            total_scripts = len(user_df)
            last_product = user_df.iloc[-1]["product"]
        else:
            last_activity = "-"
            total_scripts = 0
            last_product = "-"
        table.append({
            "المستخدم": u,
            "آخر نشاط": last_activity,
            "عدد السكربتات": total_scripts,
            "آخر منتج": last_product
        })

    st.dataframe(pd.DataFrame(table), use_container_width=True)

    st.subheader("💬 إرسال توجيه لمستخدم:")
    selected_user = st.selectbox("اختر المستخدم:", users)
    note = st.text_area("اكتب التوجيه هنا:")

    if st.button("📤 إرسال التوجيه"):
        if note.strip():
            LOGS.append({
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": selected_user,
                "status": "رسالة من الأدمن",
                "note": note
            })
            with open("user_logs.json", "w", encoding="utf-8") as f:
                json.dump(LOGS, f, ensure_ascii=False, indent=2)
            st.success(f"✅ تم إرسال التوجيه إلى {selected_user}")
        else:
            st.warning("⚠️ يرجى كتابة التوجيه قبل الإرسال.")

    # ------------------------------
    # 🧩 إدارة الحملات
    # ------------------------------
    st.markdown("---")
    st.subheader("📦 إدارة الحملات الإعلانية:")

    st.write("القائمة الحالية:")
    if CAMPAIGNS:
        st.table(pd.DataFrame(CAMPAIGNS, columns=["اسم الحملة"]))
    else:
        st.info("لا توجد حملات بعد.")

    new_campaign = st.text_input("➕ إضافة حملة جديدة:")
    if st.button("إضافة الحملة"):
        if new_campaign and new_campaign not in CAMPAIGNS:
            CAMPAIGNS.append(new_campaign)
            with open("campaigns.json", "w", encoding="utf-8") as f:
                json.dump(CAMPAIGNS, f, ensure_ascii=False, indent=2)
            st.success("✅ تمت إضافة الحملة بنجاح.")
        else:
            st.warning("⚠️ الحملة موجودة مسبقًا أو الاسم فارغ.")

    if st.button("🗑️ حذف آخر حملة"):
        if CAMPAIGNS:
            removed = CAMPAIGNS.pop()
            with open("campaigns.json", "w", encoding="utf-8") as f:
                json.dump(CAMPAIGNS, f, ensure_ascii=False, indent=2)
            st.error(f"🚮 تم حذف الحملة: {removed}")
        else:
            st.info("لا توجد حملات لحذفها.")


# ------------------------------
# 🗓️ صفحة تخطيط حملة جديدة (احترافية)
# ------------------------------
def plan_campaign():
    st.markdown("<h1 style='text-align:center;'>🎯 تخطيط حملة تسويقية احترافية</h1>", unsafe_allow_html=True)
    st.divider()

    # تحميل البيانات
    try:
        with open("campaign_plans.json", "r", encoding="utf-8") as f:
            campaigns = json.load(f)
    except FileNotFoundError:
        campaigns = []

    product_list = OPTIONS.get("product", [])
    employee_users = [u for u, d in USERS.items() if d["role"] == "user"]

    # إنشاء حملة جديدة
    with st.expander("➕ إنشاء حملة جديدة", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("اسم الحملة:")
        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                start_date = st.date_input("تاريخ البداية:")
            with col_b:
                end_date = st.date_input("تاريخ النهاية:")

        if st.button("✅ إنشاء الحملة", use_container_width=True):
            if campaign_name.strip():
                new_campaign = {
                    "campaign_name": campaign_name,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "created_by": st.session_state.user,
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "products": []
                }
                campaigns.append(new_campaign)
                with open("campaign_plans.json", "w", encoding="utf-8") as f:
                    json.dump(campaigns, f, ensure_ascii=False, indent=2)
                st.success(f"✅ تم إنشاء الحملة: {campaign_name}")
                st.rerun()

    # عرض الحملات
    if not campaigns:
        st.info("لا توجد حملات حالياً.")
        return

    for i, camp in enumerate(campaigns):
        st.markdown(f"### 📦 {camp['campaign_name']} | من {camp['start_date']} إلى {camp['end_date']}")
        st.caption(f"تم إنشاؤها بواسطة {camp['created_by']} بتاريخ {camp['created_at']}")
        st.divider()

        # 🧴 إضافة منتج جديد
        with st.expander("➕ إضافة منتج إلى الحملة", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                prod_name = st.selectbox("اسم المنتج:", product_list, key=f"prod_{i}")
            with col2:
                price_now = st.number_input("السعر الحالي:", min_value=0.0, key=f"price_now_{i}")
            with col3:
                price_new = st.number_input("السعر بعد الخصم:", min_value=0.0, key=f"price_new_{i}")

            col4, col5 = st.columns(2)
            with col4:
                discount_code = st.text_input("كود الخصم:", key=f"disc_{i}")
            with col5:
                status = st.selectbox("الحالة:", ["قيد التنفيذ", "جاهز", "معلق"], key=f"status_{i}")

            # اختيار أنواع الفيديوهات
            video_types = st.multiselect(
                "أنواع الفيديوهات المطلوبة:",
                ["توعية", "موشن", "UGC"],
                key=f"videos_{i}"
            )

            video_counts = {}
            if video_types:
                st.write("🎞️ عدد الفيديوهات المطلوبة لكل نوع:")
                for v in video_types:
                    video_counts[v] = st.number_input(f"{v}:", min_value=0, key=f"count_{v}_{i}")

            assigned_to = st.selectbox("👤 الموظف المسؤول:", ["لم يتم التعيين"] + employee_users, key=f"assign_{i}")
            notes = st.text_area("ملاحظات داخلية:", key=f"notes_{i}")

            if st.button("💾 إضافة المنتج للحملة", key=f"add_{i}", use_container_width=True):
                new_prod = {
                    "المنتج": prod_name,
                    "السعر الحالي": price_now,
                    "السعر بعد الخصم": price_new,
                    "كود الخصم": discount_code,
                    "الحالة": status,
                    "أنواع الفيديوهات": video_types,
                    "عدد الفيديوهات": video_counts,
                    "الموظف المسؤول": assigned_to,
                    "ملاحظات": notes
                }
                camp["products"].append(new_prod)
                with open("campaign_plans.json", "w", encoding="utf-8") as f:
                    json.dump(campaigns, f, ensure_ascii=False, indent=2)
                st.success("✅ تم إضافة المنتج إلى الحملة.")
                st.rerun()

        # 🎯 عرض المنتجات بشكل منظم
        if not camp["products"]:
            st.info("لم تتم إضافة أي منتجات بعد.")
            st.divider()
            continue

        st.subheader("📋 المنتجات داخل الحملة")
        for j, p in enumerate(camp["products"]):
            with st.container():
                st.markdown(f"#### 🧴 {p['المنتج']}")
                col1, col2, col3 = st.columns(3)
                col1.metric("السعر الحالي", f"{p['السعر الحالي']} ر.س")
                col2.metric("بعد الخصم", f"{p['السعر بعد الخصم']} ر.س")
                col3.text(f"🎟️ كود الخصم: {p['كود الخصم']}")

                st.write(f"**الحالة:** {p['الحالة']}")
                st.write(f"**الموظف المسؤول:** {p['الموظف المسؤول']}")
                st.write(f"**أنواع الفيديوهات:** {', '.join(p['أنواع الفيديوهات']) if p['أنواع الفيديوهات'] else '—'}")
                if p["عدد الفيديوهات"]:
                    st.write("**تفاصيل الفيديوهات:**")
                    for t, n in p["عدد الفيديوهات"].items():
                        st.text(f"- {t}: {n} فيديو")

                st.write(f"**ملاحظات:** {p['ملاحظات']}")

                colx1, colx2 = st.columns(2)
                with colx1:
                    if st.button(f"✏️ تعديل المنتج #{j}", key=f"edit_prod_{i}_{j}"):
                        st.warning("سيتم لاحقًا تفعيل نظام تعديل مباشر للمنتج.")
                with colx2:
                    if st.button(f"🗑️ حذف المنتج #{j}", key=f"del_prod_{i}_{j}"):
                        camp["products"].pop(j)
                        with open("campaign_plans.json", "w", encoding="utf-8") as f:
                            json.dump(campaigns, f, ensure_ascii=False, indent=2)
                        st.error("🚮 تم حذف المنتج.")
                        st.rerun()

                st.divider()

                # 🔔 إرسال تنبيه للموظف
                if p["الموظف المسؤول"] != "لم يتم التعيين":
                    if st.button(f"📢 إرسال تنبيه للموظف {p['الموظف المسؤول']}", key=f"notify_{i}_{j}"):
                        LOGS.append({
                            "user": p["الموظف المسؤول"],
                            "product": p["المنتج"],
                            "scenario": "تنفيذ فيديوهات الحملة",
                            "platform": "-",
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "رسالة من الأدمن",
                            "note": f"يرجى تنفيذ فيديوهات {p['المنتج']} ({', '.join(p['أنواع الفيديوهات'])}) حسب الخطة."
                        })
                        with open("user_logs.json", "w", encoding="utf-8") as f:
                            json.dump(LOGS, f, ensure_ascii=False, indent=2)
                        st.success(f"✅ تم إرسال تنبيه إلى {p['الموظف المسؤول']}")

        # حذف الحملة
        st.divider()
        if st.button(f"🗑️ حذف الحملة بالكامل #{i}", type="secondary"):
            campaigns.pop(i)
            with open("campaign_plans.json", "w", encoding="utf-8") as f:
                json.dump(campaigns, f, ensure_ascii=False, indent=2)
            st.error("🚮 تم حذف الحملة بنجاح.")
            st.rerun()


# ------------------------------
# 🚪 تسجيل الخروج
# ------------------------------
def logout():
    st.session_state.clear()
    st.success("تم تسجيل الخروج ✅")
    st.rerun()

# ------------------------------
# 🎛️ الواجهة الجانبية
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
        if st.session_state.role == "admin":
            if st.button("📅 تخطيط حملة جديدة", use_container_width=True):
                st.session_state.page = "plan_campaign"

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
    elif page == "plan_campaign" and st.session_state.role == "admin":
        plan_campaign()







