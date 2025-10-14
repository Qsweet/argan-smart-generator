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
# 🗓️ صفحة تخطيط حملة جديدة (للمشرفين فقط)
# ------------------------------
def plan_campaign():
    st.markdown("<h2>🗓️ تخطيط حملة جديدة</h2>", unsafe_allow_html=True)

    # تحميل الحملات الحالية من الملف
    try:
        with open("campaign_plans.json", "r", encoding="utf-8") as f:
            campaigns = json.load(f)
    except FileNotFoundError:
        campaigns = []

    # تحميل قائمة المنتجات من options.json
    products_list = OPTIONS.get("product", [])

    # ✅ إنشاء حملة جديدة
    st.subheader("➕ إنشاء حملة جديدة")
    campaign_name = st.text_input("اسم الحملة:")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("تاريخ البداية:")
    with col2:
        end_date = st.date_input("تاريخ النهاية:")

    if st.button("✅ إنشاء الحملة", use_container_width=True):
        if campaign_name.strip():
            new_campaign = {
                "campaign_name": campaign_name.strip(),
                "start_date": str(start_date),
                "end_date": str(end_date),
                "created_by": st.session_state.user,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updates": [],
                "products": []  # جدول المنتجات داخل الحملة
            }
            campaigns.append(new_campaign)
            with open("campaign_plans.json", "w", encoding="utf-8") as f:
                json.dump(campaigns, f, ensure_ascii=False, indent=2)
            st.success(f"✅ تم إنشاء الحملة الجديدة: {campaign_name}")
            st.rerun()
        else:
            st.warning("⚠️ يرجى إدخال اسم الحملة أولاً.")

    st.markdown("---")
    st.subheader("📋 الحملات الحالية")

    # ✅ عرض الحملات
    if not campaigns:
        st.info("لا توجد حملات حالياً.")
        return

    for i, camp in enumerate(campaigns):
        with st.expander(f"📦 {camp['campaign_name']} | من {camp['start_date']} إلى {camp['end_date']}"):
            st.write(f"تم إنشاؤها بواسطة: **{camp['created_by']}** بتاريخ **{camp['created_at']}**")
            st.divider()

            # ✅ سجل التحديثات
            st.subheader("🧾 سجل التحديثات")
            if camp["updates"]:
                for u in camp["updates"]:
                    st.markdown(f"- 🕓 {u['time']} | {u['user']}: {u['action']}")
            else:
                st.info("لا توجد تحديثات بعد.")

            update_note = st.text_area(f"إضافة تحديث جديد للحملة:", key=f"update_{i}")
            if st.button(f"💾 حفظ التحديث #{i}"):
                if update_note.strip():
                    camp["updates"].append({
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "user": st.session_state.user,
                        "action": update_note.strip()
                    })
                    with open("campaign_plans.json", "w", encoding="utf-8") as f:
                        json.dump(campaigns, f, ensure_ascii=False, indent=2)
                    st.success("✅ تم حفظ التحديث.")
                    st.rerun()
                else:
                    st.warning("⚠️ اكتب ملاحظة قبل الحفظ.")

            st.divider()

            # ✅ جدول إدارة المنتجات داخل الحملة
            st.subheader("📦 إدارة منتجات الحملة")

            if "products" not in camp:
                camp["products"] = []

            df = pd.DataFrame(camp["products"], columns=[
                "المنتج", "السعر الحالي", "السعر بعد الخصم", "كود الخصم", "الحالة", "ملاحظات"
            ]) if camp["products"] else pd.DataFrame(columns=[
                "المنتج", "السعر الحالي", "السعر بعد الخصم", "كود الخصم", "الحالة", "ملاحظات"
            ])

            # ✅ واجهة تحرير مباشرة
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key=f"edit_{i}")

            # حفظ عند الضغط
            if st.button(f"💾 حفظ التعديلات في الحملة #{i}"):
                camp["products"] = edited_df.to_dict(orient="records")
                with open("campaign_plans.json", "w", encoding="utf-8") as f:
                    json.dump(campaigns, f, ensure_ascii=False, indent=2)
                st.success("✅ تم حفظ التعديلات بنجاح.")
                st.rerun()

            st.divider()

            # ✅ إضافة منتج جديد
            with st.form(f"add_product_form_{i}", clear_on_submit=True):
                st.write("إضافة منتج جديد إلى الحملة:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    prod_name = st.selectbox("اسم المنتج:", products_list)
                with col2:
                    price_now = st.number_input("السعر الحالي:", min_value=0.0)
                with col3:
                    price_new = st.number_input("السعر بعد الخصم:", min_value=0.0)

                col4, col5 = st.columns(2)
                with col4:
                    discount_code = st.text_input("كود الخصم:")
                with col5:
                    status = st.selectbox("الحالة:", ["نشط", "متوقف", "قيد المراجعة"])
                notes = st.text_area("ملاحظات إضافية:")

                submitted = st.form_submit_button("➕ إضافة المنتج")
                if submitted:
                    new_prod = {
                        "المنتج": prod_name,
                        "السعر الحالي": price_now,
                        "السعر بعد الخصم": price_new,
                        "كود الخصم": discount_code,
                        "الحالة": status,
                        "ملاحظات": notes
                    }
                    camp["products"].append(new_prod)
                    with open("campaign_plans.json", "w", encoding="utf-8") as f:
                        json.dump(campaigns, f, ensure_ascii=False, indent=2)
                    st.success("✅ تم إضافة المنتج إلى الحملة.")
                    st.rerun()

            # ✅ حذف الحملة بالكامل
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






