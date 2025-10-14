# ============================================
# 🌿 Argan Package Smart Script Generator v5.0
# المطور: د. محمد القضاه
# التحديثات: إصلاحات ضرورية + تحسينات احترافية على الواجهة
# تاريخ التعديل: 2025-10-15
# ============================================

import streamlit as st
import openai
import json
import datetime
import pandas as pd
import hashlib
import os

# إعداد الصفحة
st.set_page_config(
    page_title="Argan Smart System", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 تحسينات CSS للواجهة
# ============================================
def load_custom_css():
    st.markdown("""
    <style>
        /* تحسين الخطوط والألوان */
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Cairo', sans-serif;
        }
        
        /* تحسين الأزرار */
        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        
        /* تحسين البطاقات */
        .main-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        }
        
        /* تحسين الجداول */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* تحسين الـ Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* تحسين الـ Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        /* تحسين الـ Expander */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* تحسين الـ Text Input */
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 2px solid #e9ecef;
            padding: 0.75rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* تحسين الـ Select Box */
        .stSelectbox>div>div>select {
            border-radius: 8px;
            border: 2px solid #e9ecef;
        }
        
        /* إضافة أيقونات جميلة */
        .icon-box {
            display: inline-block;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            text-align: center;
            line-height: 50px;
            font-size: 24px;
            margin-bottom: 1rem;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        /* تحسين الرسائل */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* تحسين الـ Divider */
        hr {
            margin: 2rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# 🔐 تحسينات الأمان
# ============================================
def hash_password(password):
    """تشفير كلمة المرور باستخدام SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """التحقق من كلمة المرور"""
    return hash_password(password) == hashed

# ============================================
# 🧩 تحميل الملفات الأساسية مع معالجة الأخطاء
# ============================================
def load_json(path):
    """تحميل ملف JSON مع معالجة أفضل للأخطاء"""
    try:
        if not os.path.exists(path):
            # إنشاء ملف فارغ إذا لم يكن موجوداً
            default_data = [] if path.endswith('.json') and 'logs' in path else {}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            return default_data
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error(f"⚠️ خطأ في قراءة الملف: {path}")
        return [] if 'logs' in path else {}
    except Exception as e:
        st.error(f"⚠️ خطأ غير متوقع: {e}")
        return [] if 'logs' in path else {}

def save_json(path, data):
    """حفظ البيانات إلى ملف JSON مع معالجة الأخطاء"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"⚠️ فشل حفظ البيانات: {e}")
        return False

# تحميل البيانات
USERS = load_json("users.json")
OPTIONS = load_json("options.json")
LOGS = load_json("user_logs.json")
CAMPAIGNS = load_json("campaigns.json")

# مفتاح OpenAI
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("⚠️ لم يتم العثور على مفتاح OpenAI API")

# ============================================
# 🔐 شاشة تسجيل الدخول المحسّنة
# ============================================
def login_screen():
    load_custom_css()
    
    # Header جميل
    st.markdown("""
        <div class='main-card'>
            <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>🌿 نظام Argan Package</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>نظام إدارة المحتوى الذكي</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # نموذج تسجيل الدخول في منتصف الصفحة
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
                <h3 style='text-align: center; color: #667eea; margin-bottom: 1.5rem;'>👋 تسجيل الدخول</h3>
            </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("🧑‍💼 اسم المستخدم:", key="login_username")
        password = st.text_input("🔒 كلمة المرور:", type="password", key="login_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 تسجيل الدخول", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("❌ يرجى إدخال اسم المستخدم وكلمة المرور")
            elif username in USERS and USERS[username]["password"] == password:
                st.session_state.user = username
                st.session_state.role = USERS[username]["role"]
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.success(f"✅ مرحبًا بك يا {username}! 🌿")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ بيانات الدخول غير صحيحة. يرجى المحاولة مرة أخرى.")
        
        # معلومات إضافية
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("ℹ️ معلومات النظام"):
            st.info("""
            **نظام Argan Package Smart Script Generator v5.0**
            
            - توليد سيناريوهات تسويقية ذكية
            - إدارة الحملات الإعلانية
            - تتبع الأداء والإحصائيات
            - دعم اشتراطات SFDA
            
            تم التطوير بواسطة: د. محمد القضاه
            """)

# ============================================
# 🏠 الصفحة الرئيسية المحسّنة
# ============================================
def home():
    load_custom_css()
    
    # Header احترافي
    st.markdown("""
        <div class='main-card'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🌿 نظام إدارة المحتوى الذكي</h1>
            <p style='font-size: 1.1rem; opacity: 0.9;'>شركة Argan Package</p>
            <p style='font-size: 0.9rem; opacity: 0.8;'>تم تطويره بواسطة د. محمد القضاه</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # إحصائيات سريعة
    user_logs = [x for x in LOGS if x.get("user") == st.session_state.user]
    total_scripts = len(user_logs)
    total_campaigns = len(CAMPAIGNS)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='feature-card' style='text-align: center;'>
                <div class='icon-box'>📝</div>
                <h3 style='color: #667eea; margin: 0;'>{}</h3>
                <p style='color: #6c757d; margin: 0;'>سيناريوهاتي</p>
            </div>
        """.format(total_scripts), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card' style='text-align: center;'>
                <div class='icon-box'>📦</div>
                <h3 style='color: #667eea; margin: 0;'>{}</h3>
                <p style='color: #6c757d; margin: 0;'>الحملات النشطة</p>
            </div>
        """.format(total_campaigns), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='feature-card' style='text-align: center;'>
                <div class='icon-box'>👤</div>
                <h3 style='color: #667eea; margin: 0;'>{}</h3>
                <p style='color: #6c757d; margin: 0;'>نوع الحساب</p>
            </div>
        """.format(st.session_state.role.upper()), unsafe_allow_html=True)
    
    with col4:
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        st.markdown("""
            <div class='feature-card' style='text-align: center;'>
                <div class='icon-box'>📅</div>
                <h3 style='color: #667eea; margin: 0; font-size: 1.3rem;'>{}</h3>
                <p style='color: #6c757d; margin: 0;'>التاريخ</p>
            </div>
        """.format(today), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # الخيارات الرئيسية
    st.markdown("<h3 style='text-align: center; color: #495057;'>🎯 ماذا تريد أن تفعل اليوم؟</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 إنتاج السيناريوهات التسويقية", use_container_width=True, type="primary"):
            st.session_state.page = "generator"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("👤 عرض حسابي وسيناريوهاتي", use_container_width=True):
            st.session_state.page = "account"
            st.rerun()
        
        if st.session_state.role == "admin":
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🧭 لوحة التحكم الإدارية", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()

# ============================================
# 🧠 صفحة توليد السكربتات المحسّنة
# ============================================
def generator():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h2 style='margin: 0;'>🧠 إنتاج السيناريوهات التسويقية</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>قم بإنشاء محتوى تسويقي احترافي بالذكاء الاصطناعي</p>
        </div>
    """, unsafe_allow_html=True)
    
    # التحقق من وجود OPTIONS
    if not OPTIONS or not all(key in OPTIONS for key in ["offer", "product", "platform", "scenario"]):
        st.error("⚠️ لم يتم تحميل الخيارات بشكل صحيح. يرجى التحقق من ملف options.json")
        return
    
    # نموذج الإدخال
    with st.container():
        st.markdown("### 📋 تفاصيل السيناريو")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 المعلومات الأساسية")
            offer = st.selectbox("🎁 العرض:", OPTIONS.get("offer", []), help="اختر نوع العرض التسويقي")
            product = st.selectbox("🧴 المنتج:", OPTIONS.get("product", []), help="اختر المنتج المراد التسويق له")
            platform = st.selectbox("📱 المنصة:", OPTIONS.get("platform", []), help="اختر منصة النشر")
            scenario = st.selectbox("🎬 السيناريو:", OPTIONS.get("scenario", []), help="اختر نوع السيناريو")
        
        with col2:
            st.markdown("#### 🎁 التفاصيل الإضافية")
            shipping = st.selectbox("🚚 التوصيل:", OPTIONS.get("shipping", []), help="خيارات التوصيل")
            gift = st.selectbox("🎁 الهدية:", OPTIONS.get("gift", []), help="هل يوجد هدية مع المنتج؟")
            cashback = st.selectbox("💸 الكاش باك:", OPTIONS.get("cashback", []), help="نسبة الكاش باك")
            tone = st.selectbox("🎤 نبرة النص:", OPTIONS.get("tone", []), help="نبرة الكتابة المطلوبة")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # اشتراطات SFDA
    with st.expander("📜 اشتراطات هيئة الغذاء والدواء السعودية (SFDA)", expanded=False):
        sfda_compliance = st.radio(
            "هل تريد أن يكون السيناريو خاضعًا لاشتراطات SFDA؟",
            ["لا", "نعم"],
            horizontal=True,
            help="الالتزام بمعايير هيئة الغذاء والدواء السعودية"
        )
        
        if sfda_compliance == "نعم":
            st.info("""
            ✅ **سيتم تطبيق الاشتراطات التالية:**
            - تجنب الادعاءات الطبية المباشرة
            - استخدام عبارات قانونية مثل "يساعد" و"يدعم"
            - التركيز على التجربة الحسية والفوائد الواقعية
            """)
    
    # تعليمات إضافية
    inst = st.text_area(
        "📝 تعليمات إضافية (اختياري):",
        placeholder="أضف أي تعليمات خاصة أو تفاصيل إضافية تريد تضمينها في السيناريو...",
        height=100
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر التوليد
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("✨ توليد السيناريو الآن", use_container_width=True, type="primary")
    
    if generate_btn:
        if not all([offer, product, platform, scenario]):
            st.error("❌ يرجى ملء جميع الحقول المطلوبة")
            return
        
        with st.spinner("🔄 جارٍ توليد السيناريو... يرجى الانتظار"):
            try:
                # بناء الـ Prompt
                sfda_rules = ""
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
                
                prompt = f"""
اكتب سكربت تسويقي احترافي باللهجة السعودية لمنتج {product} على منصة {platform}.

**تفاصيل السيناريو:**
- السيناريو: {scenario}
- النبرة: {tone}
- العرض: {offer}
- التوصيل: {shipping}
- الهدية: {gift}
- الكاش باك: {cashback}

**تعليمات إضافية:** {inst if inst else "لا توجد"}

{sfda_rules}

**المطلوب:**
- اكتب سكربت جذاب ومقنع
- استخدم اللهجة السعودية بشكل طبيعي
- اجعل النص مناسب لمنصة {platform}
- ركز على الفوائد والقيمة المضافة
"""
                
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "أنت كاتب محتوى تسويقي سعودي محترف ومطلع على سياسات الإعلانات لمنصات التواصل الاجتماعي واشتراطات SFDA."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=1000
                )
                
                script = response.choices[0].message.content.strip()
                
                # عرض النتيجة
                st.success("✅ تم توليد السيناريو بنجاح!")
                st.balloons()
                
                st.markdown("### 📜 السيناريو الناتج")
                st.markdown(f"""
                    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                                border-right: 4px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
                        {script.replace(chr(10), '<br>')}
                    </div>
                """, unsafe_allow_html=True)
                
                # خيارات إضافية
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💾 حفظ السيناريو", use_container_width=True):
                        save_log(st.session_state.user, product, scenario, platform)
                        st.success("✅ تم حفظ السيناريو في حسابك")
                
                with col2:
                    if st.button("📋 نسخ النص", use_container_width=True):
                        st.code(script, language=None)
                        st.info("💡 يمكنك نسخ النص من الصندوق أعلاه")
                
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء توليد السيناريو: {str(e)}")
                st.info("💡 يرجى التحقق من اتصال الإنترنت ومفتاح OpenAI API")

# ============================================
# 💾 حفظ سجل النشاط (محسّن)
# ============================================
def save_log(user, product, scenario, platform, campaign="لا توجد حملة"):
    """حفظ سجل النشاط مع معالجة أفضل للأخطاء"""
    try:
        log_entry = {
            "user": user,
            "product": product,
            "scenario": scenario,
            "platform": platform,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "جديد",
            "note": "",
            "campaign": campaign
        }
        
        LOGS.append(log_entry)
        
        if save_json("user_logs.json", LOGS):
            return True
        return False
    except Exception as e:
        st.error(f"⚠️ فشل حفظ السجل: {e}")
        return False

# ============================================
# 👤 صفحة حسابي (محسّنة)
# ============================================
def account_page():
    load_custom_css()
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
            <h2 style='margin: 0;'>👤 حسابي - {st.session_state.user}</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>إدارة سيناريوهاتك ومتابعة نشاطك</p>
        </div>
    """, unsafe_allow_html=True)
    
    # التحقق من الرسائل الإدارية
    admin_msgs = [
        x for x in LOGS
        if x.get("user") == st.session_state.user and x.get("status") == "رسالة من الأدمن"
    ]
    
    if admin_msgs:
        latest_msg = admin_msgs[-1]
        st.markdown(f"""
            <div style='background: #fff3cd; border-left: 4px solid #ffc107; 
                        padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
                <h4 style='color: #856404; margin: 0 0 0.5rem 0;'>📩 رسالة جديدة من الإدارة</h4>
                <p style='color: #856404; margin: 0;'><strong>التاريخ:</strong> {latest_msg.get('timestamp', 'غير محدد')}</p>
                <p style='color: #856404; margin: 0.5rem 0 0 0;'>{latest_msg.get('note', '')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # سجل النشاط
    user_logs = [x for x in LOGS if x.get("user") == st.session_state.user and x.get("status") != "رسالة من الأدمن"]
    
    if not user_logs:
        st.info("📝 لم تُنتج أي سيناريوهات بعد. ابدأ الآن بإنشاء سيناريو جديد!")
        
        if st.button("🚀 إنشاء سيناريو جديد", use_container_width=True, type="primary"):
            st.session_state.page = "generator"
            st.rerun()
        return
    
    # إحصائيات سريعة
    st.markdown("### 📊 إحصائيات سريعة")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 إجمالي السيناريوهات", len(user_logs))
    
    with col2:
        campaigns_count = len(set([x.get("campaign", "لا توجد حملة") for x in user_logs if x.get("campaign") != "لا توجد حملة"]))
        st.metric("📦 الحملات المشاركة", campaigns_count)
    
    with col3:
        if user_logs:
            last_date = user_logs[-1].get("timestamp", "غير محدد").split()[0]
            st.metric("📅 آخر نشاط", last_date)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # عرض الجدول
    st.markdown("### 📋 سيناريوهاتي")
    
    df = pd.DataFrame(user_logs)
    if not df.empty:
        # إعادة ترتيب الأعمدة
        columns_order = ["timestamp", "product", "scenario", "platform", "campaign", "status"]
        df = df[[col for col in columns_order if col in df.columns]]
        
        # تسمية الأعمدة بالعربية
        df.columns = ["التاريخ", "المنتج", "السيناريو", "المنصة", "الحملة", "الحالة"]
        
        st.dataframe(df, use_container_width=True, height=300)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # إدارة السيناريوهات
    st.markdown("### 🛠️ إدارة السيناريوهات")
    
    for i, row in enumerate(user_logs):
        with st.expander(f"🎬 {row.get('product', 'غير محدد')} | {row.get('scenario', 'غير محدد')} | {row.get('timestamp', 'غير محدد')}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_campaign = st.selectbox(
                    "📦 اختر الحملة الإعلانية:",
                    ["لا توجد حملة"] + CAMPAIGNS,
                    index=(["لا توجد حملة"] + CAMPAIGNS).index(row.get("campaign", "لا توجد حملة")) if row.get("campaign", "لا توجد حملة") in (["لا توجد حملة"] + CAMPAIGNS) else 0,
                    key=f"campaign_{i}"
                )
                
                if st.button(f"💾 حفظ التعديل", key=f"save_{i}"):
                    # البحث عن الفهرس الصحيح في LOGS
                    for idx, log in enumerate(LOGS):
                        if (log.get("user") == row.get("user") and 
                            log.get("timestamp") == row.get("timestamp") and
                            log.get("product") == row.get("product")):
                            LOGS[idx]["campaign"] = selected_campaign
                            break
                    
                    if save_json("user_logs.json", LOGS):
                        st.success("✅ تم حفظ التعديل بنجاح")
                        st.rerun()
            
            with col2:
                if st.button(f"🗑️ حذف السيناريو", key=f"delete_{i}", type="secondary"):
                    # حذف من LOGS الأصلي
                    for idx, log in enumerate(LOGS):
                        if (log.get("user") == row.get("user") and 
                            log.get("timestamp") == row.get("timestamp") and
                            log.get("product") == row.get("product")):
                            LOGS.pop(idx)
                            break
                    
                    if save_json("user_logs.json", LOGS):
                        st.success("🗑️ تم حذف السيناريو")
                        st.rerun()

# ============================================
# 🧭 لوحة التحكم الإدارية (محسّنة)
# ============================================
def admin_dashboard():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
            <h2 style='margin: 0;'>🧭 لوحة التحكم الإدارية</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>إدارة المستخدمين والحملات والإحصائيات</p>
        </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات عامة
    st.markdown("### 📊 الإحصائيات العامة")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len([u for u, d in USERS.items() if d.get("role") == "user"])
        st.metric("👥 عدد المستخدمين", total_users)
    
    with col2:
        total_scripts = len([x for x in LOGS if x.get("status") != "رسالة من الأدمن"])
        st.metric("📝 إجمالي السيناريوهات", total_scripts)
    
    with col3:
        st.metric("📦 الحملات النشطة", len(CAMPAIGNS))
    
    with col4:
        today_scripts = len([x for x in LOGS if x.get("timestamp", "").startswith(datetime.datetime.now().strftime("%Y-%m-%d"))])
        st.metric("📅 سيناريوهات اليوم", today_scripts)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # جدول المستخدمين
    st.markdown("### 👥 نشاط المستخدمين")
    
    df = pd.DataFrame(LOGS)
    if not df.empty:
        users = list(USERS.keys())
        table = []
        
        for u in users:
            user_df = df[df["user"] == u]
            if not user_df.empty:
                last_activity = user_df["timestamp"].max()
                total_scripts = len(user_df[user_df["status"] != "رسالة من الأدمن"])
                last_product = user_df[user_df["status"] != "رسالة من الأدمن"].iloc[-1]["product"] if total_scripts > 0 else "-"
            else:
                last_activity = "-"
                total_scripts = 0
                last_product = "-"
            
            table.append({
                "المستخدم": u,
                "آخر نشاط": last_activity,
                "عدد السيناريوهات": total_scripts,
                "آخر منتج": last_product,
                "النوع": USERS[u].get("role", "user")
            })
        
        st.dataframe(pd.DataFrame(table), use_container_width=True, height=300)
    else:
        st.info("لا توجد بيانات بعد")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # إرسال توجيه
    st.markdown("### 💬 إرسال توجيه لمستخدم")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        users = [u for u, d in USERS.items() if d.get("role") == "user"]
        selected_user = st.selectbox("👤 اختر المستخدم:", users)
    
    with col2:
        note = st.text_area("✍️ اكتب التوجيه هنا:", placeholder="اكتب رسالتك للمستخدم...")
    
    if st.button("📤 إرسال التوجيه", use_container_width=True, type="primary"):
        if note.strip():
            LOGS.append({
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": selected_user,
                "status": "رسالة من الأدمن",
                "note": note,
                "product": "-",
                "scenario": "-",
                "platform": "-",
                "campaign": "-"
            })
            
            if save_json("user_logs.json", LOGS):
                st.success(f"✅ تم إرسال التوجيه إلى {selected_user}")
        else:
            st.warning("⚠️ يرجى كتابة التوجيه قبل الإرسال")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    # إدارة الحملات
    st.markdown("### 📦 إدارة الحملات الإعلانية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 القائمة الحالية")
        if CAMPAIGNS:
            for idx, camp in enumerate(CAMPAIGNS):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.text(f"{idx + 1}. {camp}")
                with col_b:
                    if st.button("🗑️", key=f"del_camp_{idx}"):
                        CAMPAIGNS.pop(idx)
                        if save_json("campaigns.json", CAMPAIGNS):
                            st.success("✅ تم الحذف")
                            st.rerun()
        else:
            st.info("لا توجد حملات بعد")
    
    with col2:
        st.markdown("#### ➕ إضافة حملة جديدة")
        new_campaign = st.text_input("اسم الحملة:", placeholder="مثال: حملة رمضان 2025")
        
        if st.button("إضافة الحملة", use_container_width=True):
            if new_campaign and new_campaign not in CAMPAIGNS:
                CAMPAIGNS.append(new_campaign)
                if save_json("campaigns.json", CAMPAIGNS):
                    st.success("✅ تمت إضافة الحملة بنجاح")
                    st.rerun()
            else:
                st.warning("⚠️ الحملة موجودة مسبقًا أو الاسم فارغ")

# ============================================
# 🗓️ صفحة تخطيط حملة جديدة (محسّنة)
# ============================================
def plan_campaign():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>🎯 تخطيط حملة تسويقية احترافية</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>خطط وأدر حملاتك التسويقية بكفاءة</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    try:
        with open("campaign_plans.json", "r", encoding="utf-8") as f:
            campaigns = json.load(f)
    except FileNotFoundError:
        campaigns = []
    
    product_list = OPTIONS.get("product", [])
    employee_users = [u for u, d in USERS.items() if d.get("role") == "user"]
    
    # إنشاء حملة جديدة
    with st.expander("➕ إنشاء حملة جديدة", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input("📝 اسم الحملة:", placeholder="مثال: حملة الصيف 2025")
        
        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                start_date = st.date_input("📅 تاريخ البداية:")
            with col_b:
                end_date = st.date_input("📅 تاريخ النهاية:")
        
        if st.button("✅ إنشاء الحملة", use_container_width=True, type="primary"):
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
                
                if save_json("campaign_plans.json", campaigns):
                    st.success(f"✅ تم إنشاء الحملة: {campaign_name}")
                    st.balloons()
                    st.rerun()
            else:
                st.warning("⚠️ يرجى إدخال اسم الحملة")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # عرض الحملات
    if not campaigns:
        st.info("📦 لا توجد حملات حالياً. قم بإنشاء حملة جديدة للبدء!")
        return
    
    st.markdown("### 📦 الحملات النشطة")
    
    for i, camp in enumerate(campaigns):
        with st.container():
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                            border-right: 4px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1); margin-bottom: 1.5rem;'>
                    <h3 style='color: #667eea; margin: 0 0 0.5rem 0;'>📦 {camp['campaign_name']}</h3>
                    <p style='color: #6c757d; margin: 0;'>
                        <strong>المدة:</strong> من {camp['start_date']} إلى {camp['end_date']} | 
                        <strong>المنشئ:</strong> {camp['created_by']} | 
                        <strong>تاريخ الإنشاء:</strong> {camp['created_at']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # إضافة منتج جديد
            with st.expander("➕ إضافة منتج إلى الحملة", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    prod_name = st.selectbox("🧴 اسم المنتج:", product_list, key=f"prod_{i}")
                with col2:
                    price_now = st.number_input("💰 السعر الحالي:", min_value=0.0, key=f"price_now_{i}")
                with col3:
                    price_new = st.number_input("💸 السعر بعد الخصم:", min_value=0.0, key=f"price_new_{i}")
                
                col4, col5 = st.columns(2)
                with col4:
                    discount_code = st.text_input("🎟️ كود الخصم:", key=f"disc_{i}")
                with col5:
                    status = st.selectbox("📊 الحالة:", ["قيد التنفيذ", "جاهز", "معلق"], key=f"status_{i}")
                
                # اختيار أنواع الفيديوهات
                video_types = st.multiselect(
                    "🎞️ أنواع الفيديوهات المطلوبة:",
                    ["توعية", "موشن", "UGC"],
                    key=f"videos_{i}"
                )
                
                video_counts = {}
                if video_types:
                    st.write("📊 عدد الفيديوهات المطلوبة لكل نوع:")
                    cols = st.columns(len(video_types))
                    for idx, v in enumerate(video_types):
                        with cols[idx]:
                            video_counts[v] = st.number_input(f"{v}:", min_value=0, key=f"count_{v}_{i}")
                
                assigned_to = st.selectbox("👤 الموظف المسؤول:", ["لم يتم التعيين"] + employee_users, key=f"assign_{i}")
                notes = st.text_area("📝 ملاحظات داخلية:", key=f"notes_{i}")
                
                if st.button("💾 إضافة المنتج للحملة", key=f"add_{i}", use_container_width=True, type="primary"):
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
                    
                    if save_json("campaign_plans.json", campaigns):
                        st.success("✅ تم إضافة المنتج إلى الحملة")
                        st.rerun()
            
            # عرض المنتجات
            if not camp["products"]:
                st.info("لم تتم إضافة أي منتجات بعد")
            else:
                st.markdown("#### 📋 المنتجات داخل الحملة")
                
                for j, p in enumerate(camp["products"]):
                    with st.container():
                        st.markdown(f"""
                            <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                                <h4 style='color: #495057; margin: 0 0 0.5rem 0;'>🧴 {p['المنتج']}</h4>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("السعر الحالي", f"{p['السعر الحالي']} ر.س")
                        col2.metric("بعد الخصم", f"{p['السعر بعد الخصم']} ر.س")
                        
                        discount_percent = 0
                        if p['السعر الحالي'] > 0:
                            discount_percent = ((p['السعر الحالي'] - p['السعر بعد الخصم']) / p['السعر الحالي']) * 100
                        col3.metric("نسبة الخصم", f"{discount_percent:.1f}%")
                        
                        st.write(f"**🎟️ كود الخصم:** {p['كود الخصم']}")
                        st.write(f"**📊 الحالة:** {p['الحالة']}")
                        st.write(f"**👤 الموظف المسؤول:** {p['الموظف المسؤول']}")
                        st.write(f"**🎞️ أنواع الفيديوهات:** {', '.join(p['أنواع الفيديوهات']) if p['أنواع الفيديوهات'] else '—'}")
                        
                        if p["عدد الفيديوهات"]:
                            st.write("**📊 تفاصيل الفيديوهات:**")
                            for t, n in p["عدد الفيديوهات"].items():
                                st.text(f"  • {t}: {n} فيديو")
                        
                        if p['ملاحظات']:
                            st.write(f"**📝 ملاحظات:** {p['ملاحظات']}")
                        
                        col_x1, col_x2, col_x3 = st.columns(3)
                        
                        with col_x1:
                            if p["الموظف المسؤول"] != "لم يتم التعيين":
                                if st.button(f"📢 إرسال تنبيه", key=f"notify_{i}_{j}"):
                                    LOGS.append({
                                        "user": p["الموظف المسؤول"],
                                        "product": p["المنتج"],
                                        "scenario": "تنفيذ فيديوهات الحملة",
                                        "platform": "-",
                                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "status": "رسالة من الأدمن",
                                        "note": f"يرجى تنفيذ فيديوهات {p['المنتج']} ({', '.join(p['أنواع الفيديوهات'])}) حسب الخطة.",
                                        "campaign": camp['campaign_name']
                                    })
                                    
                                    if save_json("user_logs.json", LOGS):
                                        st.success(f"✅ تم إرسال تنبيه إلى {p['الموظف المسؤول']}")
                        
                        with col_x2:
                            if st.button(f"✏️ تعديل", key=f"edit_prod_{i}_{j}"):
                                st.info("💡 قم بحذف المنتج وإضافته مرة أخرى بالتعديلات المطلوبة")
                        
                        with col_x3:
                            if st.button(f"🗑️ حذف", key=f"del_prod_{i}_{j}", type="secondary"):
                                camp["products"].pop(j)
                                if save_json("campaign_plans.json", campaigns):
                                    st.success("🗑️ تم حذف المنتج")
                                    st.rerun()
                        
                        st.divider()
            
            # حذف الحملة
            if st.button(f"🗑️ حذف الحملة بالكامل", key=f"del_camp_{i}", type="secondary"):
                campaigns.pop(i)
                if save_json("campaign_plans.json", campaigns):
                    st.success("🗑️ تم حذف الحملة بنجاح")
                    st.rerun()
            
            st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# 🚪 تسجيل الخروج
# ============================================
def logout():
    st.session_state.clear()
    st.success("✅ تم تسجيل الخروج بنجاح")
    st.rerun()

# ============================================
# 🎛️ الواجهة الجانبية المحسّنة
# ============================================
def sidebar():
    with st.sidebar:
        # Header جميل
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;'>
                <h3 style='margin: 0;'>👋 مرحبًا</h3>
                <p style='margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: 600;'>{st.session_state.user}</p>
                <p style='margin: 0.25rem 0 0 0; font-size: 0.9rem; opacity: 0.9;'>{st.session_state.role.upper()}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # القائمة
        st.markdown("### 🧭 القائمة الرئيسية")
        
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        
        if st.button("🧠 توليد السيناريوهات", use_container_width=True):
            st.session_state.page = "generator"
            st.rerun()
        
        if st.button("👤 حسابي", use_container_width=True):
            st.session_state.page = "account"
            st.rerun()
        
        if st.session_state.role == "admin":
            st.markdown("### 🔧 أدوات الإدارة")
            
            if st.button("🧭 لوحة التحكم", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()
            
            if st.button("📅 تخطيط حملة جديدة", use_container_width=True):
                st.session_state.page = "plan_campaign"
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
            logout()
        
        # معلومات النظام
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: #6c757d; font-size: 0.8rem;'>
                <p style='margin: 0;'>🌿 Argan Package</p>
                <p style='margin: 0;'>v5.0</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# 🚀 النظام الرئيسي
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar()
    page = st.session_state.get("page", "home")
    
    if page == "home":
        home()
    elif page == "generator":
        generator()
    elif page == "account":
        account_page()
    elif page == "admin" and st.session_state.role == "admin":
        admin_dashboard()
    elif page == "plan_campaign" and st.session_state.role == "admin":
        plan_campaign()
    else:
        home()

