# ============================================
# 🌿 Argan Package Smart Script Generator v5.1
# المطور: د. محمد القضاه
# التحديثات: إصلاحات ضرورية + تحسينات احترافية على الواجهة
# التحديث: قسم تخطيط الحملات المتقدم
# تاريخ التعديل: 2025-10-15
# ============================================

import streamlit as st
import openai
import json
import datetime
import pandas as pd
import hashlib
import os
from hijri_converter import Hijri, Gregorian

# إعداد الصفحة
st.set_page_config(
    page_title="Argan Smart System", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🔒 نظام حفظ الجلسة
# ============================================
def save_session(username, role):
    """حفظ بيانات الجلسة في ملف مؤقت"""
    session_data = {
        "username": username,
        "role": role,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(".session.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    except:
        pass

def load_session():
    """تحميل بيانات الجلسة من الملف المؤقت"""
    try:
        if os.path.exists(".session.json"):
            with open(".session.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                # التحقق من أن الجلسة لم تنتهي صلاحيتها (24 ساعة)
                timestamp = datetime.datetime.strptime(session_data["timestamp"], "%Y-%m-%d %H:%M:%S")
                if (datetime.datetime.now() - timestamp).total_seconds() < 86400:  # 24 hours
                    return session_data
    except:
        pass
    return None

def clear_session():
    """مسح بيانات الجلسة"""
    try:
        if os.path.exists(".session.json"):
            os.remove(".session.json")
    except:
        pass

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
        
        /* بطاقات الحملات */
        .campaign-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .campaign-upcoming {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        /* تحسين الجدول التفاعلي */
        .editable-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        
        .editable-table th {
            background: #667eea;
            color: white;
            padding: 0.75rem;
            text-align: right;
        }
        
        .editable-table td {
            padding: 0.75rem;
            border-bottom: 1px solid #dee2e6;
        }
        
        .editable-table tr:hover {
            background: #f8f9fa;
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
@st.cache_data(ttl=300)  # Cache لمدة 5 دقائق
def load_json(path):
    """تحميل ملف JSON مع معالجة أفضل للأخطاء (cached)"""
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


# ============================================
# 📅 دوال التقويم الهجري والميلادي
# ============================================
def gregorian_to_hijri(date):
    """تحويل التاريخ الميلادي إلى هجري"""
    try:
        hijri = Gregorian(date.year, date.month, date.day).to_hijri()
        return f"{hijri.day}/{hijri.month}/{hijri.year}"
    except:
        return "—"

def hijri_to_gregorian(day, month, year):
    """تحويل التاريخ الهجري إلى ميلادي"""
    try:
        greg = Hijri(year, month, day).to_gregorian()
        return datetime.date(greg.year, greg.month, greg.day)
    except:
        return None

def calculate_days_remaining(end_date_str):
    """حساب الأيام المتبقية"""
    try:
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = (end_date - today).days
        return delta
    except:
        return None

def calculate_days_until_start(start_date_str):
    """حساب الأيام حتى بداية الحملة"""
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = (start_date - today).days
        return delta
    except:
        return None

def get_current_and_upcoming_campaigns(campaigns):
    """الحصول على الحملة الحالية والقادمة"""
    today = datetime.date.today()
    current = None
    upcoming = None
    
    for camp in campaigns:
        try:
            start = datetime.datetime.strptime(camp["start_date"], "%Y-%m-%d").date()
            end = datetime.datetime.strptime(camp["end_date"], "%Y-%m-%d").date()
            
            if start <= today <= end:
                current = camp
            elif start > today:
                if upcoming is None or start < datetime.datetime.strptime(upcoming["start_date"], "%Y-%m-%d").date():
                    upcoming = camp
        except:
            continue
    
    return current, upcoming

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
                # حفظ الجلسة
                save_session(username, USERS[username]["role"])
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
            - تخطيط وإدارة الحملات
            - تتبع الأداء والإحصائيات
            - إدارة الجرد والمخزون
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
    
    # إحصائيات المنتجات
    st.markdown("إحصائيات المنتجات")
    
    # الجرد المحدث
    st.markdown("الجرد المحدث")
    
    # رفع ملف Excel
    uploaded_file = st.file_uploader(
        "📄 ارفع ملف الجرد (Excel):",
        type=["xlsx", "xls"],
        help="ارفع ملف Excel يحتوي على بيانات الجرد",
        key="inventory_uploader"
    )
    
    if uploaded_file:
        try:
            # حفظ الملف
            import os
            os.makedirs("inventory_files", exist_ok=True)
            
            file_path = f"inventory_files/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ تم رفع الملف: {uploaded_file.name}")
            
            # قراءة وعرض البيانات
            df = pd.read_excel(file_path)
            
            # إحصائيات سريعة
            st.markdown("إحصائيات الجرد")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📦 إجمالي المنتجات", len(df))
            
            with col2:
                if "كميته" in df.columns:
                    total_qty = df["كميته"].sum()
                    st.metric("📊 إجمالي الكمية", f"{total_qty:,.0f}")
                else:
                    st.metric("📊 إجمالي الكمية", "-")
            
            with col3:
                if "كميته" in df.columns:
                    low_stock = len(df[df["كميته"] < 100])
                    st.metric("⚠️ منتجات قليلة المخزون", low_stock)
                else:
                    st.metric("⚠️ منتجات قليلة المخزون", "-")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # عرض الجدول
            st.markdown("جدول الجرد الكامل")
            
            # تنسيق الجدول
            if "كميته" in df.columns:
                # تلوين الصفوف حسب الكمية
                def highlight_low_stock(row):
                    if row["كميته"] < 100:
                        return ['background-color: #fff3cd'] * len(row)
                    elif row["كميته"] < 500:
                        return ['background-color: #d1ecf1'] * len(row)
                    else:
                        return ['background-color: #d4edda'] * len(row)
                
                styled_df = df.style.apply(highlight_low_stock, axis=1)
                st.dataframe(styled_df, use_container_width=True, height=400)
            else:
                st.dataframe(df, use_container_width=True, height=400)
            
            # ملاحظة
            st.info("""
                💡 **ملاحظة:** 
                - 🟡 **أخضر**: مخزون جيد (500+)
                - 🔵 **أزرق**: مخزون متوسط (100-499)
                - 🟠 **أصفر**: مخزون قليل (<100)
            """)
            
            # حفظ مسار الملف للاستخدام اللاحق
            st.session_state.current_inventory_file = file_path
            
        except Exception as e:
            st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
    
    # عرض آخر ملف محفوظ
    else:
        # التأكد من وجود المجلد
        os.makedirs("inventory_files", exist_ok=True)
        
        if os.path.exists("inventory_files"):
            files = [f for f in os.listdir("inventory_files") if f.endswith(('.xlsx', '.xls'))]
        else:
            files = []
        
        if files:
            latest_file = max([f"inventory_files/{f}" for f in files], key=os.path.getmtime)
            
            st.info(f"📁 آخر ملف محفوظ: {os.path.basename(latest_file)}")
            
            if st.button("👁️ عرض الملف المحفوظ", use_container_width=True):
                try:
                    df = pd.read_excel(latest_file)
                    
                    # إحصائيات
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📦 إجمالي المنتجات", len(df))
                    with col2:
                        if "كميته" in df.columns:
                            st.metric("📊 إجمالي الكمية", f"{df['كميته'].sum():,.0f}")
                    with col3:
                        if "كميته" in df.columns:
                            st.metric("⚠️ منتجات قليلة", len(df[df["كميته"] < 100]))
                    
                    st.dataframe(df, use_container_width=True, height=400)
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ لا توجد ملفات جرد محفوظة. ارفع ملف Excel للبدء.")
    
    # قسم النسخ الاحتياطي
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("💾 النسخ الاحتياطي والاستعادة")
    
    st.info("""
        💡 **ملاحظة مهمة:** 
        - قم بتحميل نسخة احتياطية قبل كل تحديث للتطبيق
        - يتم حفظ جميع بياناتك (الحملات، العملاء، الإيرادات، إلخ)
        - يمكنك استعادة البيانات بعد أي تحديث
    """)
    
    col_backup1, col_backup2 = st.columns(2)
    
    with col_backup1:
        st.markdown("📥 **تحميل نسخة احتياطية**")
        if st.button("📥 إنشاء وتحميل نسخة احتياطية", use_container_width=True, type="primary"):
            try:
                from backup_utility import BackupManager
                manager = BackupManager()
                backup_path = manager.create_backup()
                
                # قراءة الملف للتحميل
                with open(backup_path, "rb") as f:
                    backup_data = f.read()
                
                st.success("✅ تم إنشاء النسخة الاحتياطية بنجاح!")
                
                st.download_button(
                    label="⬇️ تحميل النسخة الاحتياطية",
                    data=backup_data,
                    file_name=os.path.basename(backup_path),
                    mime="application/zip",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ خطأ في إنشاء النسخة: {str(e)}")
    
    with col_backup2:
        st.markdown("📤 **استعادة نسخة احتياطية**")
        uploaded_backup = st.file_uploader(
            "ارفع ملف النسخة الاحتياطية (ZIP):",
            type=["zip"],
            key="backup_restore_uploader"
        )
        
        if uploaded_backup:
            if st.button("🔄 استعادة البيانات", use_container_width=True, type="primary"):
                try:
                    # حفظ الملف مؤقتاً
                    temp_path = f"/tmp/{uploaded_backup.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_backup.getbuffer())
                    
                    from backup_utility import BackupManager
                    manager = BackupManager()
                    
                    if manager.restore_backup(temp_path):
                        st.success("✅ تم استعادة البيانات بنجاح!")
                        st.balloons()
                        st.info("🔄 يرجى إعادة تحميل الصفحة لرؤية البيانات المستعادة")
                    else:
                        st.error("❌ فشلت عملية الاستعادة")
                except Exception as e:
                    st.error(f"❌ خطأ في الاستعادة: {str(e)}")
    
    # عرض النسخ الاحتياطية المتاحة
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📁 عرض النسخ الاحتياطية المحفوظة"):
        try:
            from backup_utility import BackupManager
            manager = BackupManager()
            backups = manager.list_backups()
            
            if backups:
                for backup in backups:
                    col_b1, col_b2, col_b3 = st.columns([3, 2, 1])
                    with col_b1:
                        st.text(f"📦 {backup['filename']}")
                    with col_b2:
                        st.text(f"📅 {backup['date']}")
                    with col_b3:
                        st.text(f"📊 {backup['size_mb']:.2f} MB")
            else:
                st.info("💭 لا توجد نسخ احتياطية محفوظة")
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")

# ============================================
# 📅 صفحة تخطيط الحملات (محسَّنة ومتقدمة v5.1)
# ============================================
def plan_campaign():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>📅 تخطيط الحملات</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>إدارة شاملة لجميع الحملات التسويقية</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    try:
        with open("campaign_plans.json", "r", encoding="utf-8") as f:
            campaigns = json.load(f)
    except FileNotFoundError:
        campaigns = []
    except json.JSONDecodeError:
        st.error("⚠️ ملف الحملات تالف")
        campaigns = []
    
    product_list = OPTIONS.get("product", [])
    scenario_list = OPTIONS.get("scenario", [])
    
    # ============================================
    # 📊 عرض الحملة الحالية والقادمة
    # ============================================
    st.markdown("### 📊 نظرة عامة على الحملات")
    
    current_campaign, upcoming_campaign = get_current_and_upcoming_campaigns(campaigns)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if current_campaign:
            days_remaining = calculate_days_remaining(current_campaign["end_date"])
            st.markdown(f"""
                <div class='campaign-card'>
                    <h3 style='margin: 0 0 1rem 0;'>🎯 الحملة الحالية</h3>
                    <h2 style='margin: 0 0 1rem 0;'>{current_campaign['campaign_name']}</h2>
                    <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;'>
                        <p style='margin: 0; font-size: 1.2rem;'><strong>⏰ متبقي:</strong> {days_remaining} يوم</p>
                        <p style='margin: 0.5rem 0 0 0;'>📅 من {current_campaign['start_date']} إلى {current_campaign['end_date']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📭 لا توجد حملة نشطة حالياً")
    
    with col2:
        if upcoming_campaign:
            days_until = calculate_days_until_start(upcoming_campaign["start_date"])
            duration = (datetime.datetime.strptime(upcoming_campaign["end_date"], "%Y-%m-%d") - 
                       datetime.datetime.strptime(upcoming_campaign["start_date"], "%Y-%m-%d")).days
            st.markdown(f"""
                <div class='campaign-card campaign-upcoming'>
                    <h3 style='margin: 0 0 1rem 0;'>🚀 الحملة القادمة</h3>
                    <h2 style='margin: 0 0 1rem 0;'>{upcoming_campaign['campaign_name']}</h2>
                    <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;'>
                        <p style='margin: 0; font-size: 1.2rem;'><strong>⏳ تبدأ بعد:</strong> {days_until} يوم</p>
                        <p style='margin: 0.5rem 0 0 0;'>⏱️ <strong>المدة:</strong> {duration} يوم</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📭 لا توجد حملة قادمة مجدولة")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # ➕ إنشاء حملة جديدة
    # ============================================
    st.markdown("### ➕ إنشاء حملة جديدة")
    
    with st.expander("🎯 تخطيط حملة جديدة", expanded=False):
        # اسم الحملة
        campaign_name = st.text_input(
            "📝 اسم الحملة:",
            placeholder="مثال: حملة رمضان 2025",
            help="أدخل اسماً واضحاً ومميزاً للحملة"
        )
        
        # شعار الحملة
        st.markdown("#### 🎨 شعار الحملة")
        campaign_logo = st.file_uploader(
            "ارفع شعار الحملة (اختياري):",
            type=["png", "jpg", "jpeg", "svg"],
            help="ارفع صورة شعار الحملة بصيغة PNG أو JPG",
            key="campaign_logo_uploader"
        )
        
        logo_path = None
        if campaign_logo:
            # حفظ الشعار
            import os
            logo_filename = f"{campaign_name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{campaign_logo.name.split('.')[-1]}"
            logo_path = f"campaign_logos/{logo_filename}"
            
            os.makedirs("campaign_logos", exist_ok=True)
            with open(logo_path, "wb") as f:
                f.write(campaign_logo.getbuffer())
            
            st.success(f"✅ تم رفع الشعار: {logo_filename}")
            st.image(campaign_logo, width=200, caption="معاينة الشعار")
        
        # اختيار نوع التقويم
        calendar_type = st.radio(
            "📅 نوع التقويم:",
            ["ميلادي", "هجري"],
            horizontal=True,
            help="اختر التقويم المناسب لتحديد مدة الحملة"
        )
        
        col1, col2 = st.columns(2)
        
        if calendar_type == "ميلادي":
            with col1:
                start_date = st.date_input(
                    "📅 تاريخ البداية (ميلادي):",
                    help="تاريخ بداية الحملة"
                )
                st.info(f"🌙 هجري: {gregorian_to_hijri(start_date)}")
            
            with col2:
                end_date = st.date_input(
                    "📅 تاريخ النهاية (ميلادي):",
                    help="تاريخ انتهاء الحملة"
                )
                st.info(f"🌙 هجري: {gregorian_to_hijri(end_date)}")
        
        else:  # هجري
            with col1:
                st.write("📅 تاريخ البداية (هجري):")
                col_d1, col_m1, col_y1 = st.columns(3)
                with col_d1:
                    h_start_day = st.number_input("اليوم", 1, 30, 1, key="h_start_day")
                with col_m1:
                    h_start_month = st.number_input("الشهر", 1, 12, 1, key="h_start_month")
                with col_y1:
                    h_start_year = st.number_input("السنة", 1440, 1500, 1446, key="h_start_year")
                
                start_date = hijri_to_gregorian(h_start_day, h_start_month, h_start_year)
                if start_date:
                    st.success(f"📅 ميلادي: {start_date}")
                else:
                    st.error("❌ تاريخ هجري غير صحيح")
            
            with col2:
                st.write("📅 تاريخ النهاية (هجري):")
                col_d2, col_m2, col_y2 = st.columns(3)
                with col_d2:
                    h_end_day = st.number_input("اليوم", 1, 30, 1, key="h_end_day")
                with col_m2:
                    h_end_month = st.number_input("الشهر", 1, 12, 1, key="h_end_month")
                with col_y2:
                    h_end_year = st.number_input("السنة", 1440, 1500, 1446, key="h_end_year")
                
                end_date = hijri_to_gregorian(h_end_day, h_end_month, h_end_year)
                if end_date:
                    st.success(f"📅 ميلادي: {end_date}")
                else:
                    st.error("❌ تاريخ هجري غير صحيح")
        
        # حساب مدة الحملة
        if start_date and end_date:
            duration = (end_date - start_date).days
            if duration > 0:
                st.info(f"⏱️ مدة الحملة: **{duration} يوم**")
            else:
                st.warning("⚠️ تاريخ النهاية يجب أن يكون بعد تاريخ البداية")
        
        # زر إنشاء الحملة
        if st.button("✅ إنشاء الحملة", use_container_width=True, type="primary"):
            if not campaign_name.strip():
                st.error("❌ يرجى إدخال اسم الحملة")
            elif not start_date or not end_date:
                st.error("❌ يرجى تحديد تواريخ البداية والنهاية")
            elif end_date <= start_date:
                st.error("❌ تاريخ النهاية يجب أن يكون بعد تاريخ البداية")
            else:
                new_campaign = {
                    "campaign_name": campaign_name,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "calendar_type": calendar_type,
                    "logo_path": logo_path,
                    "created_by": st.session_state.get("user", "admin"),
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "products": [],
                    "deleted": False
                }
                campaigns.append(new_campaign)
                
                if save_json("campaign_plans.json", campaigns):
                    st.success(f"✅ تم إنشاء الحملة: {campaign_name}")
                    st.balloons()
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # 📦 عرض وإدارة الحملات
    # ============================================
    if not campaigns:
        st.info("📦 لا توجد حملات حالياً. قم بإنشاء حملة جديدة للبدء!")
        return
    
    st.markdown("### 📦 جميع الحملات")
    
    # تصفية الحملات لإخفاء المحذوفة
    active_campaigns = [c for c in campaigns if not c.get('deleted', False)]
    deleted_campaigns = [c for c in campaigns if c.get('deleted', False)]
    
    # عرض عدد الحملات
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info(f"📦 الحملات النشطة: **{len(active_campaigns)}**")
    with col_info2:
        st.warning(f"🗑️ سلة المهملات: **{len(deleted_campaigns)}**")
    
    for i, camp in enumerate(active_campaigns):
        with st.container():
            # عنوان الحملة
            col_logo, col_title, col_delete = st.columns([1, 5, 1])
            
            with col_logo:
                if camp.get('logo_path') and os.path.exists(camp['logo_path']):
                    st.image(camp['logo_path'], width=80)
                else:
                    st.markdown("🎨", unsafe_allow_html=True)
            
            with col_title:
                st.markdown(f"""
                    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                                border-right: 4px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
                        <h3 style='color: #667eea; margin: 0;'>📦 {camp['campaign_name']}</h3>
                        <p style='color: #6c757d; margin: 0.5rem 0 0 0;'>
                            📅 من {camp['start_date']} إلى {camp['end_date']} | 
                            👤 {camp.get('created_by', 'admin')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_delete:
                if st.button("🗑️", key=f"del_camp_{i}", help="نقل إلى سلة المهملات"):
                    # نقل إلى سلة المهملات
                    camp['deleted'] = True
                    camp['deleted_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    camp['deleted_by'] = st.session_state.get("user", "admin")
                    save_json("campaign_plans.json", campaigns)
                    st.success("✅ تم نقل الحملة إلى سلة المهملات")
                    st.rerun()
            
            # إضافة منتج للحملة
            with st.expander("➕ إضافة منتج إلى الحملة", expanded=False):
                # اختيار المنتج
                # إزالة المنتجات المضافة مسبقاً
                existing_products = [p.get("product_name", p.get("المنتج")) for p in camp.get("products", [])]
                available_products = [p for p in product_list if p not in existing_products]
                
                if not available_products:
                    st.warning("⚠️ جميع المنتجات مضافة بالفعل إلى هذه الحملة")
                    selected_product = None
                else:
                    selected_product = st.selectbox(
                        "🧊 اختر المنتج:",
                        available_products,
                        key=f"prod_{i}",
                        help="اختر المنتج من القائمة (المنتجات المضافة مسبقاً مخفية)"
                    )
                
                # الأسعار
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    current_price = st.number_input(
                        "💰 سعر البيع الحالي (ر.س):",
                        min_value=0.0,
                        step=1.0,
                        key=f"curr_price_{i}"
                    )
                
                with col_p2:
                    campaign_price = st.number_input(
                        "💸 سعر البيع على الحملة (ر.س):",
                        min_value=0.0,
                        step=1.0,
                        key=f"camp_price_{i}"
                    )
                
                with col_p3:
                    if current_price > 0:
                        discount = ((current_price - campaign_price) / current_price) * 100
                        st.metric("📊 نسبة الخصم", f"{discount:.1f}%")
                
                # نوع الخصم
                discount_type = st.radio(
                    "🎟️ نوع الخصم:",
                    ["كود خصم", "رخصة تخفيض"],
                    horizontal=True,
                    key=f"disc_type_{i}"
                )
                
                discount_code = ""
                if discount_type == "كود خصم":
                    discount_code = st.text_input(
                        "🔖 كود الخصم:",
                        placeholder="مثال: RAMADAN2025",
                        key=f"disc_code_{i}"
                    )
                
                # أنواع الفيديوهات
                st.markdown("#### 🎬 الفيديوهات المطلوبة")
                
                video_data = []
                num_videos = st.number_input(
                    "عدد أنواع الفيديوهات:",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"num_vids_{i}"
                )
                
                for v in range(int(num_videos)):
                    col_v1, col_v2 = st.columns(2)
                    with col_v1:
                        video_type = st.selectbox(
                            f"نوع الفيديو #{v+1}:",
                            scenario_list,
                            key=f"vid_type_{i}_{v}"
                        )
                    with col_v2:
                        video_count = st.number_input(
                            f"العدد:",
                            min_value=1,
                            value=1,
                            key=f"vid_count_{i}_{v}"
                        )
                    video_data.append({"type": video_type, "count": video_count})
                
                # التصاميم المطلوبة
                st.markdown("#### 🎨 التصاميم المطلوبة")
                
                design_data = []
                num_designs = st.number_input(
                    "عدد أنواع التصاميم:",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"num_designs_{i}"
                )
                
                for d in range(int(num_designs)):
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        design_type = st.selectbox(
                            f"نوع التصميم #{d+1}:",
                            ["ريل ستايل", "تصميم منتج", "بوست", "ستوري"],
                            key=f"design_type_{i}_{d}"
                        )
                    with col_d2:
                        design_count = st.number_input(
                            f"العدد:",
                            min_value=1,
                            value=1,
                            key=f"design_count_{i}_{d}"
                        )
                    design_data.append({"type": design_type, "count": design_count})
                
                # زر الإضافة
                if selected_product and st.button("💾 إضافة المنتج", key=f"add_prod_{i}", use_container_width=True, type="primary"):
                    new_product = {
                        "product_name": selected_product,
                        "current_price": current_price,
                        "campaign_price": campaign_price,
                        "discount_type": discount_type,
                        "discount_code": discount_code,
                        "videos": video_data,
                        "designs": design_data,
                        "added_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    camp["products"].append(new_product)
                    
                    if save_json("campaign_plans.json", campaigns):
                        st.success(f"✅ تم إضافة {selected_product} إلى الحملة")
                        st.rerun()
            
            # ============================================
            # 📊 عرض المنتجات في جدول تفاعلي
            # ============================================
            if camp.get("products"):
                st.markdown("#### 📋 المنتجات في الحملة")
                
                # تحويل المنتجات إلى DataFrame
                products_data = []
                for p in camp["products"]:
                    videos_str = ", ".join([f"{v['type']} ({v['count']})" for v in p.get("videos", p.get("أنواع الفيديوهات", []))])
                    designs_str = ", ".join([f"{d['type']} ({d['count']})" for d in p.get("designs", [])])
                    
                    # دعم الصيغة القديمة والجديدة
                    product_name = p.get("product_name", p.get("المنتج", "—"))
                    current_price = p.get("current_price", p.get("السعر الحالي", 0))
                    campaign_price = p.get("campaign_price", p.get("السعر بعد الخصم", 0))
                    discount_type = p.get("discount_type", "—")
                    discount_code = p.get("discount_code", p.get("كود الخصم", "—"))
                    
                    # تنظيف القيم إذا كانت تحتوي على "ر.س"
                    if isinstance(current_price, str):
                        current_price = current_price.replace(" ر.س", "").strip()
                    if isinstance(campaign_price, str):
                        campaign_price = campaign_price.replace(" ر.س", "").strip()
                    
                    products_data.append({
                        "المنتج": product_name,
                        "السعر الحالي": f"{current_price} ر.س",
                        "سعر الحملة": f"{campaign_price} ر.س",
                        "نوع الخصم": discount_type,
                        "الكود": discount_code,
                        "الفيديوهات": videos_str if videos_str else "—",
                        "التصاميم": designs_str if designs_str else "—"
                    })
                
                df = pd.DataFrame(products_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # خيارات التعديل
                st.markdown("##### ✏️ تعديل المنتجات")
                product_to_edit = st.selectbox(
                    "اختر منتج للتعديل:",
                    [p.get("product_name", p.get("المنتج", "—")) for p in camp["products"]],
                    key=f"edit_select_{i}"
                )
                
                col_edit, col_del = st.columns(2)
                
                with col_edit:
                    if st.button("✏️ تعديل", key=f"edit_btn_{i}", use_container_width=True):
                        st.info("💡 قريباً: سيتم إضافة واجهة تعديل تفاعلية")
                
                with col_del:
                    if st.button("🗑️ حذف المنتج", key=f"del_prod_{i}", use_container_width=True, type="secondary"):
                        camp["products"] = [p for p in camp["products"] if p.get("product_name", p.get("المنتج")) != product_to_edit]
                        save_json("campaign_plans.json", campaigns)
                        st.success(f"✅ تم حذف {product_to_edit}")
                        st.rerun()
            else:
                st.info("📭 لم تتم إضافة أي منتجات بعد")
            
            st.markdown("---")
    
    # ============================================
    # 🗑️ سلة المهملات
    # ============================================
    if deleted_campaigns:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🗑️ سلة المهملات")
        
        with st.expander(f"📦 عرض الحملات المحذوفة ({len(deleted_campaigns)})", expanded=False):
            for i, camp in enumerate(deleted_campaigns):
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.markdown(f"""
                        <div style='background: #fff3cd; padding: 1rem; border-radius: 8px; border-right: 3px solid #ffc107;'>
                            <h4 style='margin: 0; color: #856404;'>🗑️ {camp['campaign_name']}</h4>
                            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #856404;'>
                                📅 {camp['start_date']} - {camp['end_date']} | 
                                🗑️ حذف بواسطة: {camp.get('deleted_by', 'admin')} | 
                                ⏰ {camp.get('deleted_at', '---')}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("♻️ استرجاع", key=f"restore_{i}", help="استرجاع الحملة"):
                        camp['deleted'] = False
                        camp.pop('deleted_at', None)
                        camp.pop('deleted_by', None)
                        save_json("campaign_plans.json", campaigns)
                        st.success(f"✅ تم استرجاع الحملة: {camp['campaign_name']}")
                        st.rerun()
                
                with col3:
                    if st.button("❌ حذف نهائي", key=f"perm_del_{i}", help="حذف نهائي للحملة"):
                        # حذف الشعار إن وجد
                        if camp.get('logo_path') and os.path.exists(camp['logo_path']):
                            os.remove(camp['logo_path'])
                        
                        campaigns.remove(camp)
                        save_json("campaign_plans.json", campaigns)
                        st.warning(f"⚠️ تم حذف الحملة نهائياً: {camp['campaign_name']}")
                        st.rerun()
                
                st.markdown("---")
            
            # زر حذف جميع الحملات المحذوفة
            if st.button("🗑️ إفراغ سلة المهملات", use_container_width=True, type="secondary"):
                for camp in deleted_campaigns:
                    if camp.get('logo_path') and os.path.exists(camp['logo_path']):
                        os.remove(camp['logo_path'])
                    campaigns.remove(camp)
                
                save_json("campaign_plans.json", campaigns)
                st.success("✅ تم إفراغ سلة المهملات")
                st.rerun()

# ============================================
# 💰 تتبع العائد الشهري
# ============================================
# ============================================
# 💰 تتبع العائد الشهري - النسخة المحسّنة v5.5
# ============================================
def monthly_revenue_tracking():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>💰 تتبع العائد الشهري</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>إدارة ومتابعة المصاريف والمداخيل والعائد على الاستثمار</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    try:
        with open("revenue_data.json", "r", encoding="utf-8") as f:
            revenue_data = json.load(f)
    except FileNotFoundError:
        revenue_data = {}
    except json.JSONDecodeError:
        st.error("⚠️ ملف البيانات تالف")
        revenue_data = {}
    
    if not revenue_data:
        st.warning("⚠️ لا توجد بيانات بعد. ابدأ بإضافة شهر جديد.")
        revenue_data = {}
    
    # الحصول على قائمة الأشهر
    months = list(revenue_data.keys())
    
    # ============================================
    # 📊 عرض البيانات الحالية
    # ============================================
    if months:
        current_month = months[0]
        month_data = revenue_data[current_month]
        
        st.markdown(f"### 📅 الشهر الحالي: **{current_month}**")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"📅 **الشهر:** {current_month}")
        with col_info2:
            st.info(f"⏰ **آخر تحديث:** {month_data.get('last_update', 'غير محدد')}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # حساب الإحصائيات
        total_expenses = sum([e['value'] for e in month_data.get('expenses', [])])
        total_revenue = sum([r['value'] for r in month_data.get('revenues', [])])
        total_orders = sum([r.get('orders', 0) for r in month_data.get('revenues', [])])
        net_profit = total_revenue - total_expenses
        roi = (net_profit / total_expenses * 100) if total_expenses > 0 else 0
        
        # عرض الإحصائيات الرئيسية
        st.markdown("### 📊 الإحصائيات الرئيسية")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>📈 إجمالي المداخيل</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{total_revenue:,.0f}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>ر.س</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>📉 إجمالي المصاريف</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{total_expenses:,.0f}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>ر.س</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            profit_color = "#28a745" if net_profit > 0 else "#dc3545"
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>💰 صافي الربح</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{net_profit:,.0f}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>ROI: {roi:.1f}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>📦 عدد الطلبات</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{int(total_orders):,}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>طلب</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # عرض تفصيلي للمصاريف والمداخيل
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 📉 المصاريف")
            if month_data.get('expenses'):
                for exp in month_data['expenses']:
                    st.markdown(f"""
                        <div style='background: #fff3cd; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #ffc107;'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='font-weight: 600; color: #856404;'>{exp['type']}</span>
                                <span style='font-size: 1.1rem; font-weight: 700; color: #856404;'>{exp['value']:,.0f} ر.س</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("لا توجد مصاريف")
        
        with col_right:
            st.markdown("### 📈 المداخيل")
            if month_data.get('revenues'):
                for rev in month_data['revenues']:
                    roi_val = rev.get('roi', 0)
                    roi_color = "#28a745" if roi_val >= 2.0 else "#17a2b8" if roi_val >= 1.0 else "#ffc107"
                    roi_bg = "#d4edda" if roi_val >= 2.0 else "#d1ecf1" if roi_val >= 1.0 else "#fff3cd"
                    
                    st.markdown(f"""
                        <div style='background: {roi_bg}; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {roi_color};'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <div style='font-weight: 600; color: #333;'>{rev['type']}</div>
                                    <div style='font-size: 0.85rem; color: #666; margin-top: 0.2rem;'>
                                        ROI: {roi_val:.2f} | الطلبات: {rev.get('orders', 0)}
                                    </div>
                                </div>
                                <span style='font-size: 1.1rem; font-weight: 700; color: {roi_color};'>{rev['value']:,.0f} ر.س</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("لا توجد مداخيل")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
    
    # ============================================
    # ➕ إضافة/تعديل بيانات الشهر
    # ============================================
    st.markdown("### ⚙️ إدارة البيانات")
    
    tab1, tab2, tab3 = st.tabs(["➕ إضافة شهر جديد", "✏️ تعديل شهر موجود", "📅 عرض الأشهر السابقة"])
    
    with tab1:
        st.markdown("#### ➕ إضافة شهر جديد")
        
        new_month_name = st.text_input("📅 اسم الشهر:", placeholder="مثال: شهر سبتمبر 2025", key="new_month")
        
        if new_month_name and new_month_name not in revenue_data:
            st.markdown("##### 📉 المصاريف")
            
            num_expenses = st.number_input("عدد بنود المصاريف:", min_value=1, max_value=20, value=3, key="num_exp")
            
            expenses = []
            for i in range(int(num_expenses)):
                col_exp1, col_exp2 = st.columns([2, 1])
                with col_exp1:
                    exp_type = st.text_input(f"نوع المصروف {i+1}:", key=f"exp_type_{i}")
                with col_exp2:
                    exp_value = st.number_input(f"القيمة (ر.س):", min_value=0.0, key=f"exp_val_{i}")
                
                if exp_type and exp_value > 0:
                    expenses.append({"type": exp_type, "value": exp_value})
            
            st.markdown("##### 📈 المداخيل")
            
            num_revenues = st.number_input("عدد بنود المداخيل:", min_value=1, max_value=20, value=3, key="num_rev")
            
            revenues = []
            for i in range(int(num_revenues)):
                col_rev1, col_rev2, col_rev3, col_rev4 = st.columns([2, 1, 1, 1])
                with col_rev1:
                    rev_type = st.text_input(f"نوع المدخول {i+1}:", key=f"rev_type_{i}")
                with col_rev2:
                    rev_value = st.number_input(f"القيمة (ر.س):", min_value=0.0, key=f"rev_val_{i}")
                with col_rev3:
                    rev_orders = st.number_input(f"الطلبات:", min_value=0, key=f"rev_ord_{i}")
                with col_rev4:
                    rev_roi = st.number_input(f"ROI:", min_value=0.0, key=f"rev_roi_{i}")
                
                if rev_type and rev_value > 0:
                    revenues.append({
                        "type": rev_type,
                        "value": rev_value,
                        "orders": int(rev_orders),
                        "roi": rev_roi
                    })
            
            if st.button("💾 حفظ الشهر الجديد", use_container_width=True, type="primary"):
                revenue_data[new_month_name] = {
                    "month_name": new_month_name,
                    "last_update": datetime.now().strftime("%Y-%m-%d"),
                    "expenses": expenses,
                    "revenues": revenues
                }
                
                # إعادة ترتيب الأشهر (الأحدث أولاً)
                revenue_data = {k: revenue_data[k] for k in sorted(revenue_data.keys(), reverse=True)}
                
                with open("revenue_data.json", "w", encoding="utf-8") as f:
                    json.dump(revenue_data, f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ تم إضافة الشهر: {new_month_name}")
                st.rerun()
        elif new_month_name in revenue_data:
            st.warning("⚠️ هذا الشهر موجود بالفعل. استخدم تبويب 'تعديل شهر موجود'")
    
    with tab2:
        st.markdown("#### ✏️ تعديل شهر موجود")
        
        if months:
            selected_month = st.selectbox("📅 اختر الشهر:", months, key="edit_month")
            
            if selected_month:
                month_data = revenue_data[selected_month]
                
                st.markdown("##### 📉 المصاريف الحالية")
                
                expenses_to_keep = []
                for i, exp in enumerate(month_data.get('expenses', [])):
                    col1, col2, col3 = st.columns([2, 1, 0.5])
                    with col1:
                        exp_type = st.text_input(f"نوع:", value=exp['type'], key=f"edit_exp_type_{i}")
                    with col2:
                        exp_value = st.number_input(f"القيمة:", value=float(exp['value']), key=f"edit_exp_val_{i}")
                    with col3:
                        if st.button("🗑️", key=f"del_exp_{i}"):
                            continue
                    
                    if exp_type and exp_value > 0:
                        expenses_to_keep.append({"type": exp_type, "value": exp_value})
                
                if st.button("➕ إضافة مصروف جديد", key="add_exp_btn"):
                    st.session_state.adding_expense = True
                
                if st.session_state.get('adding_expense'):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        new_exp_type = st.text_input("نوع المصروف:", key="new_exp_type")
                    with col2:
                        new_exp_value = st.number_input("القيمة:", min_value=0.0, key="new_exp_value")
                    
                    if new_exp_type and new_exp_value > 0:
                        expenses_to_keep.append({"type": new_exp_type, "value": new_exp_value})
                        st.session_state.adding_expense = False
                
                st.markdown("##### 📈 المداخيل الحالية")
                
                revenues_to_keep = []
                for i, rev in enumerate(month_data.get('revenues', [])):
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
                    with col1:
                        rev_type = st.text_input(f"نوع:", value=rev['type'], key=f"edit_rev_type_{i}")
                    with col2:
                        rev_value = st.number_input(f"القيمة:", value=float(rev['value']), key=f"edit_rev_val_{i}")
                    with col3:
                        rev_orders = st.number_input(f"الطلبات:", value=int(rev.get('orders', 0)), key=f"edit_rev_ord_{i}")
                    with col4:
                        rev_roi = st.number_input(f"ROI:", value=float(rev.get('roi', 0)), key=f"edit_rev_roi_{i}")
                    with col5:
                        if st.button("🗑️", key=f"del_rev_{i}"):
                            continue
                    
                    if rev_type and rev_value > 0:
                        revenues_to_keep.append({
                            "type": rev_type,
                            "value": rev_value,
                            "orders": rev_orders,
                            "roi": rev_roi
                        })
                
                if st.button("➕ إضافة مدخول جديد", key="add_rev_btn"):
                    st.session_state.adding_revenue = True
                
                if st.session_state.get('adding_revenue'):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        new_rev_type = st.text_input("نوع المدخول:", key="new_rev_type")
                    with col2:
                        new_rev_value = st.number_input("القيمة:", min_value=0.0, key="new_rev_value")
                    with col3:
                        new_rev_orders = st.number_input("الطلبات:", min_value=0, key="new_rev_orders")
                    with col4:
                        new_rev_roi = st.number_input("ROI:", min_value=0.0, key="new_rev_roi")
                    
                    if new_rev_type and new_rev_value > 0:
                        revenues_to_keep.append({
                            "type": new_rev_type,
                            "value": new_rev_value,
                            "orders": int(new_rev_orders),
                            "roi": new_rev_roi
                        })
                        st.session_state.adding_revenue = False
                
                col_save, col_delete = st.columns([3, 1])
                
                with col_save:
                    if st.button("💾 حفظ التعديلات", use_container_width=True, type="primary"):
                        revenue_data[selected_month] = {
                            "month_name": selected_month,
                            "last_update": datetime.now().strftime("%Y-%m-%d"),
                            "expenses": expenses_to_keep,
                            "revenues": revenues_to_keep
                        }
                        
                        with open("revenue_data.json", "w", encoding="utf-8") as f:
                            json.dump(revenue_data, f, ensure_ascii=False, indent=2)
                        
                        st.success(f"✅ تم تحديث الشهر: {selected_month}")
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️ حذف الشهر", use_container_width=True, type="secondary"):
                        del revenue_data[selected_month]
                        
                        with open("revenue_data.json", "w", encoding="utf-8") as f:
                            json.dump(revenue_data, f, ensure_ascii=False, indent=2)
                        
                        st.warning(f"⚠️ تم حذف الشهر: {selected_month}")
                        st.rerun()
        else:
            st.info("لا توجد أشهر لتعديلها")
    
    with tab3:
        st.markdown("#### 📅 عرض الأشهر السابقة")
        
        if len(months) > 1:
            previous_months = months[1:]
            selected_prev_month = st.selectbox("📅 اختر الشهر:", previous_months, key="prev_month")
            
            if selected_prev_month:
                prev_data = revenue_data[selected_prev_month]
                
                # حساب الإحصائيات
                prev_expenses = sum([e['value'] for e in prev_data.get('expenses', [])])
                prev_revenue = sum([r['value'] for r in prev_data.get('revenues', [])])
                prev_orders = sum([r.get('orders', 0) for r in prev_data.get('revenues', [])])
                prev_profit = prev_revenue - prev_expenses
                prev_roi = (prev_profit / prev_expenses * 100) if prev_expenses > 0 else 0
                
                st.markdown(f"### 📅 {selected_prev_month}")
                st.info(f"⏰ آخر تحديث: {prev_data.get('last_update', 'غير محدد')}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📈 المداخيل", f"{prev_revenue:,.0f} ر.س")
                with col2:
                    st.metric("📉 المصاريف", f"{prev_expenses:,.0f} ر.س")
                with col3:
                    st.metric("💰 الربح", f"{prev_profit:,.0f} ر.س", delta=f"{prev_roi:.1f}% ROI")
                with col4:
                    st.metric("📦 الطلبات", f"{int(prev_orders):,}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("**📉 المصاريف:**")
                    for exp in prev_data.get('expenses', []):
                        st.markdown(f"- **{exp['type']}:** {exp['value']:,.0f} ر.س")
                
                with col_right:
                    st.markdown("**📈 المداخيل:**")
                    for rev in prev_data.get('revenues', []):
                        st.markdown(f"- **{rev['type']}:** {rev['value']:,.0f} ر.س (ROI: {rev.get('roi', 0):.2f})")
        else:
            st.info("لا توجد أشهر سابقة")


# ============================================
# 📱 حملات مراسلاتي
# ============================================
def create_moraselaty_campaign():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>📱 إنشاء حملات مراسلاتي</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>تخطيط وإدارة حملات WhatsApp التسويقية</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل بيانات العملاء من SQLite
    try:
        from modules.database import get_all_orders
        from datetime import datetime as dt
        orders = get_all_orders()
        last_updated = dt.now().strftime("%Y-%m-%d")
    except Exception as e:
        st.error(f"❌ خطأ في تحميل بيانات العملاء: {e}")
        return
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 إجمالي الطلبات", f"{len(orders):,}")
    with col2:
        unique_customers = len(set([o.get('رقم الهاتف', '') for o in orders if o.get('رقم الهاتف')]))
        st.metric("👥 عدد العملاء", f"{unique_customers:,}")
    with col3:
        cities_count = len(set([o.get('المدينة', '') for o in orders if o.get('المدينة')]))
        st.metric("🏙️ عدد المدن", f"{cities_count}")
    with col4:
        st.metric("📅 آخر تحديث", last_updated.split()[0])
    
    st.markdown("---")
    
    # تبويبات
    tab1, tab2, tab3, tab4 = st.tabs(["📤 رفع بيانات جديدة", "🎯 إنشاء حملة جديدة", "✍️ إنشاء حملة تسويقية", "📋 الحملات السابقة"])
    
    with tab1:
        st.markdown("### 📤 رفع ملف بيانات العملاء")
        st.info("💡 يمكنك رفع ملف Excel يحتوي على بيانات الطلبات. سيتم دمجها مع البيانات الموجودة مع منع التكرار.")
        
        uploaded_file = st.file_uploader("اختر ملف Excel", type=['xlsx', 'xls'], key="moraselaty_upload")
        
        if uploaded_file:
            try:
                import pandas as pd
                df_new = pd.read_excel(uploaded_file)
                
                st.success(f"✅ تم قراءة {len(df_new)} طلب من الملف")
                
                # عرض عينة
                with st.expander("👁️ معاينة البيانات (أول 5 صفوف)"):
                    st.dataframe(df_new.head())
                
                if st.button("💾 حفظ ودمج البيانات", type="primary"):
                    # دمج مع البيانات الموجودة
                    df_existing = pd.DataFrame(orders)
                    df_all = pd.concat([df_existing, df_new], ignore_index=True)
                    
                    # إزالة التكرار
                    df_unique = df_all.drop_duplicates(subset=['رقم الطلب'], keep='first')
                    df_unique = df_unique.fillna("")
                    
                    # حفظ
                    customers_data_new = {
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "total_orders": len(df_unique),
                        "orders": df_unique.to_dict('records')
                    }
                    
                    with open("moraselaty_customers.json", "w", encoding="utf-8") as f:
                        json.dump(customers_data_new, f, ensure_ascii=False, indent=2)
                    
                    st.success(f"✅ تم الدمج بنجاح! الإجمالي الآن: {len(df_unique)} طلب")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
    
    with tab2:
        st.markdown("### 🎯 إنشاء حملة جديدة")
        
        # اسم الحملة
        campaign_name = st.text_input("📝 اسم الحملة:", placeholder="مثال: حملة عيد الفطر 2025")
        
        st.markdown("#### 🔍 تحديد العملاء المستهدفين")
        
        # الفلاتر
        col_f1, col_f2 = st.columns(2)
        
        # تهيئة المتغيرات لتجنب UnboundLocalError
        min_price = 0.0
        max_price = 0.0
        
        with col_f1:
            st.markdown("##### 💰 قيمة الطلبات")
            price_filter_type = st.selectbox(
                "نوع الفلتر:",
                ["الكل", "أكثر من", "أقل من", "بين"],
                key="price_filter"
            )
            
            if price_filter_type == "أكثر من":
                min_price = st.number_input("القيمة (ر.س):", min_value=0.0, value=100.0, key="min_price")
            elif price_filter_type == "أقل من":
                max_price = st.number_input("القيمة (ر.س):", min_value=0.0, value=500.0, key="max_price")
            elif price_filter_type == "بين":
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    min_price = st.number_input("من (ر.س):", min_value=0.0, value=100.0, key="min_price_between")
                with col_p2:
                    max_price = st.number_input("إلى (ر.س):", min_value=0.0, value=500.0, key="max_price_between")
        
        with col_f2:
            st.markdown("##### 🏙️ المدينة")
            cities = sorted(set([o.get('المدينة', '') for o in orders if o.get('المدينة')]))
            city_filter = st.multiselect(
                "اختر المدن:",
                ["كامل السعودية"] + cities,
                default=["كامل السعودية"],
                key="city_filter"
            )
        
        col_f3, col_f4 = st.columns(2)
        
        with col_f3:
            st.markdown("##### 📦 حالة الطلب")
            statuses = sorted(set([o.get('حالة الطلب', '') for o in orders if o.get('حالة الطلب')]))
            status_filter = st.multiselect(
                "اختر الحالات:",
                ["الكل"] + statuses,
                default=["تم توصيل الطلب"],
                key="status_filter"
            )
        
        with col_f4:
            st.markdown("##### 💳 طريقة الدفع")
            payments = sorted(set([o.get(' طريقة الدفع', '') for o in orders if o.get(' طريقة الدفع')]))
            payment_filter = st.multiselect(
                "اختر طرق الدفع:",
                ["الكل"] + payments,
                default=["الكل"],
                key="payment_filter"
            )
        
        # تطبيق الفلاتر
        if st.button("🔍 تطبيق الفلاتر وعرض النتائج", type="primary", use_container_width=True):
            filtered_orders = orders.copy()
            
            # فلتر السعر
            if price_filter_type == "أكثر من":
                filtered_orders = [o for o in filtered_orders if float(o.get('المبلغ الاجمالي', 0) or 0) > min_price]
            elif price_filter_type == "أقل من":
                filtered_orders = [o for o in filtered_orders if float(o.get('المبلغ الاجمالي', 0) or 0) < max_price]
            elif price_filter_type == "بين":
                filtered_orders = [o for o in filtered_orders if min_price <= float(o.get('المبلغ الاجمالي', 0) or 0) <= max_price]
            
            # فلتر المدينة
            if "كامل السعودية" not in city_filter:
                filtered_orders = [o for o in filtered_orders if o.get('المدينة', '') in city_filter]
            
            # فلتر الحالة
            if "الكل" not in status_filter:
                filtered_orders = [o for o in filtered_orders if o.get('حالة الطلب', '') in status_filter]
            
            # فلتر طريقة الدفع
            if "الكل" not in payment_filter:
                filtered_orders = [o for o in filtered_orders if o.get(' طريقة الدفع', '') in payment_filter]
            
            # حفظ في session_state
            st.session_state.filtered_customers = filtered_orders
            
            st.success(f"✅ تم العثور على {len(filtered_orders)} عميل مطابق للفلاتر!")
        
        # عرض النتائج
        if hasattr(st.session_state, 'filtered_customers') and st.session_state.filtered_customers:
            filtered = st.session_state.filtered_customers
            
            st.markdown("---")
            st.markdown(f"### 📊 النتائج: {len(filtered)} عميل")
            
            # إحصائيات
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                total_value = sum([float(o.get('المبلغ الاجمالي', 0) or 0) for o in filtered])
                st.metric("💰 إجمالي القيمة", f"{total_value:,.0f} ر.س")
            with col_s2:
                unique_phones = len(set([o.get('رقم الهاتف', '') for o in filtered if o.get('رقم الهاتف')]))
                st.metric("📱 أرقام فريدة", f"{unique_phones:,}")
            with col_s3:
                avg_order = total_value / len(filtered) if filtered else 0
                st.metric("📊 متوسط الطلب", f"{avg_order:,.0f} ر.س")
            with col_s4:
                cities_in_result = len(set([o.get('المدينة', '') for o in filtered if o.get('المدينة')]))
                st.metric("🏙️ المدن", f"{cities_in_result}")
            
            # عرض الجدول
            with st.expander("👁️ عرض تفاصيل العملاء"):
                df_filtered = pd.DataFrame(filtered)
                st.dataframe(df_filtered[['اسم العميل', 'رقم الهاتف', 'المدينة', 'المبلغ الاجمالي', 'حالة الطلب', ' طريقة الدفع']])
            
            # حفظ الحملة
            st.markdown("---")
            campaign_message = st.text_area(
                "✍️ نص الرسالة:",
                placeholder="مثال: مرحباً {الاسم}، نقدم لك عرض خاص...",
                height=150
            )
            
            if st.button("💾 حفظ الحملة", type="primary", use_container_width=True):
                if not campaign_name:
                    st.error("❌ يرجى إدخال اسم الحملة!")
                elif not campaign_message:
                    st.error("❌ يرجى كتابة نص الرسالة!")
                else:
                    # تحميل الحملات الموجودة
                    try:
                        with open("moraselaty_campaigns.json", "r", encoding="utf-8") as f:
                            campaigns_data = json.load(f)
                    except:
                        campaigns_data = {"campaigns": []}
                    
                    # إنشاء الحملة
                    new_campaign = {
                        "id": len(campaigns_data["campaigns"]) + 1,
                        "name": campaign_name,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "created_by": st.session_state.username,
                        "message": campaign_message,
                        "filters": {
                            "price_type": price_filter_type,
                            "cities": city_filter,
                            "statuses": status_filter,
                            "payments": payment_filter
                        },
                        "total_customers": len(filtered),
                        "unique_phones": unique_phones,
                        "total_value": total_value,
                        "customers": filtered
                    }
                    
                    campaigns_data["campaigns"].append(new_campaign)
                    
                    with open("moraselaty_campaigns.json", "w", encoding="utf-8") as f:
                        json.dump(campaigns_data, f, ensure_ascii=False, indent=2)
                    
                    st.success(f"✅ تم حفظ الحملة: {campaign_name}")
                    st.balloons()
                    del st.session_state.filtered_customers
                    st.rerun()
    
    with tab3:
        st.markdown("### 📋 الحملات السابقة")
        
        try:
            with open("moraselaty_campaigns.json", "r", encoding="utf-8") as f:
                campaigns_data = json.load(f)
            campaigns = campaigns_data.get("campaigns", [])
        except:
            campaigns = []
        
        if not campaigns:
            st.info("📭 لا توجد حملات محفوظة بعد.")
        else:
            for campaign in reversed(campaigns):
                with st.expander(f"📱 {campaign['name']} - {campaign['created_at'].split()[0]}"):
                    col_c1, col_c2 = st.columns([2, 1])
                    
                    with col_c1:
                        st.markdown(f"**👤 المنشئ:** {campaign['created_by']}")
                        st.markdown(f"**📅 التاريخ:** {campaign['created_at']}")
                        st.markdown(f"**👥 العملاء:** {campaign['total_customers']:,}")
                        st.markdown(f"**📱 أرقام فريدة:** {campaign['unique_phones']:,}")
                        st.markdown(f"**💰 إجمالي القيمة:** {campaign['total_value']:,.0f} ر.س")
                    
                    with col_c2:
                        if st.button("📥 تصدير Excel", key=f"export_{campaign['id']}"):
                            # تصدير عمودين فقط: اسم العميل ورقم الجوال
                            df_export = pd.DataFrame(campaign['customers'])
                            df_export_filtered = df_export[['اسم العميل', 'رقم الهاتف']].copy()
                            df_export_filtered.columns = ['اسم العميل', 'رقم الجوال']
                            st.download_button(
                                "⬇️ تحميل",
                                df_export_filtered.to_csv(index=False, encoding='utf-8-sig'),
                                f"campaign_{campaign['id']}_contacts.csv",
                                "text/csv"
                            )
                    
                    st.markdown("**✍️ نص الرسالة:**")
                    st.text_area("", campaign['message'], height=100, key=f"msg_{campaign['id']}", disabled=True)
    
    with tab3:
        st.markdown("### ✍️ إنشاء حملة تسويقية بالذكاء الاصطناعي")
        st.info("🤖 سيتم استخدام ChatGPT لإعادة صياغة فكرتك بشكل احترافي ومختصر")
        
        # تحميل قائمة المنتجات
        try:
            with open("options.json", "r", encoding="utf-8") as f:
                options_data = json.load(f)
            products_list = options_data.get("product", [])
        except:
            products_list = []
            st.error("❌ خطأ في تحميل قائمة المنتجات")
        
        st.markdown("#### 1️⃣ اختر المنتجات المشاركة")
        selected_products = st.multiselect(
            "المنتجات:",
            products_list,
            key="marketing_products"
        )
        
        st.markdown("---")
        st.markdown("#### 2️⃣ اكتب فكرة الحملة")
        campaign_idea = st.text_area(
            "الفكرة الأساسية:",
            placeholder="مثال: عرض خاص على منتجات زيت الأرجان لفترة محدودة مع خصم 20%",
            height=100,
            key="campaign_idea"
        )
        
        st.markdown("---")
        st.markdown("#### 3️⃣ روابط المنتجات")
        
        # إنشاء session_state للروابط
        if 'product_links' not in st.session_state:
            st.session_state.product_links = []
        
        # عدد الروابط
        num_links = st.number_input("عدد الروابط:", min_value=1, max_value=10, value=len(selected_products) if selected_products else 1, key="num_links")
        
        product_links = []
        for i in range(int(num_links)):
            col_link1, col_link2 = st.columns([1, 2])
            with col_link1:
                product_name = st.text_input(f"المنتج {i+1}:", value=selected_products[i] if i < len(selected_products) else "", key=f"product_name_{i}")
            with col_link2:
                product_url = st.text_input(f"الرابط {i+1}:", placeholder="https://...", key=f"product_url_{i}")
            
            if product_name and product_url:
                product_links.append({"name": product_name, "url": product_url})
        
        # حفظ في session_state
        st.session_state.saved_product_links = product_links
        
        st.markdown("---")
        st.markdown("#### 4️⃣ معلومات الزر")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            button_name = st.text_input("اسم الزر:", placeholder="مثال: اطلب الآن", key="button_name")
        with col_btn2:
            button_url = st.text_input("رابط الزر:", placeholder="https://...", key="button_url")
        
        st.markdown("---")
        
        # زر توليد النص
        if st.button("🤖 توليد النص بالذكاء الاصطناعي", type="primary", use_container_width=True):
            if not campaign_idea:
                st.error("❌ يرجى كتابة فكرة الحملة!")
            elif not button_name or not button_url:
                st.error("❌ يرجى إدخال معلومات الزر!")
            else:
                with st.spinner("جاري توليد النص..."):
                    try:
                        # استدعاء ChatGPT API
                        import openai
                        import os
                        
                        # إعداد البرومبت
                        prompt = f"""أنت مسوق محترف لمنتجات العناية والتجميل. اكتب رسالة تسويقية احترافية ومختصرة للواتساب بناءً على الفكرة التالية:

الفكرة: {campaign_idea}

المنتجات: {', '.join(selected_products) if selected_products else 'غير محدد'}

المتطلبات:
- الرسالة يجب أن تكون باللغة العربية
- مختصرة وواضحة (لا تتجاوز 150 كلمة)
- احترافية وجذابة
- بدون إيموجي
- بدون عناوين أو تنسيق
- فقط النص التسويقي مباشرة

اكتب الرسالة فقط بدون أي إضافات:"""
                        
                        # استدعاء API
                        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                        response = client.chat.completions.create(
                            model="gpt-4-turbo",
                            messages=[
                                {"role": "system", "content": "أنت مسوق محترف لمنتجات العناية والتجميل."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=500
                        )
                        
                        generated_text = response.choices[0].message.content.strip()
                        
                        # بناء النص النهائي
                        final_text = "أرجو اعتماد الحملة التالية من ميتا وتجهيزها:\n\n"
                        final_text += generated_text + "\n\n"
                        
                        # إضافة روابط المنتجات
                        if product_links:
                            final_text += "روابط المنتجات:\n"
                            for link in product_links:
                                final_text += f"- {link['name']}: {link['url']}\n"
                            final_text += "\n"
                        
                        # إضافة معلومات الزر
                        final_text += f"زر الحملة:\n"
                        final_text += f"الاسم: {button_name}\n"
                        final_text += f"الرابط: {button_url}"
                        
                        # حفظ في session_state
                        st.session_state.generated_campaign_text = final_text
                        
                        st.success("✅ تم توليد النص بنجاح!")
                        
                    except Exception as e:
                        st.error(f"❌ خطأ في توليد النص: {str(e)}")
                        st.info("💡 تأكد من إعداد OPENAI_API_KEY في secrets.toml")
        
        # عرض النص المولد
        if hasattr(st.session_state, 'generated_campaign_text'):
            st.markdown("---")
            st.markdown("### 📋 معاينة النص المولد")
            
            generated_text_area = st.text_area(
                "النص النهائي:",
                st.session_state.generated_campaign_text,
                height=300,
                key="final_text_display"
            )
            
            col_action1, col_action2 = st.columns(2)
            with col_action1:
                if st.button("📋 نسخ النص", use_container_width=True):
                    st.code(st.session_state.generated_campaign_text, language="text")
                    st.success("✅ يمكنك نسخ النص من المربع أعلاه")
            
            with col_action2:
                if st.button("💾 حفظ كحملة", type="primary", use_container_width=True):
                    # حفظ الحملة التسويقية
                    try:
                        with open("moraselaty_campaigns.json", "r", encoding="utf-8") as f:
                            campaigns_data = json.load(f)
                    except:
                        campaigns_data = {"campaigns": []}
                    
                    new_campaign = {
                        "id": len(campaigns_data["campaigns"]) + 1,
                        "name": f"حملة تسويقية - {datetime.now().strftime('%Y-%m-%d')}",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "created_by": st.session_state.get('username', 'مجهول'),
                        "type": "marketing",
                        "products": st.session_state.get('marketing_products', []),
                        "idea": st.session_state.get('campaign_idea', ''),
                        "product_links": st.session_state.get('saved_product_links', []),
                        "button_name": st.session_state.get('button_name', ''),
                        "button_url": st.session_state.get('button_url', ''),
                        "message": st.session_state.get('generated_campaign_text', '')
                    }
                    
                    campaigns_data["campaigns"].append(new_campaign)
                    
                    with open("moraselaty_campaigns.json", "w", encoding="utf-8") as f:
                        json.dump(campaigns_data, f, ensure_ascii=False, indent=2)
                    
                    st.success("✅ تم حفظ الحملة التسويقية بنجاح!")
                    st.balloons()
                    del st.session_state.generated_campaign_text
                    st.rerun()


def logout():
    clear_session()
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
            
            if st.button("💰 تتبع العائد الشهري", use_container_width=True):
                st.session_state.page = "revenue_tracking"
                st.rerun()
            
            if st.button("📱 حملات مراسلاتي", use_container_width=True):
                st.session_state.page = "moraselaty"
                st.rerun()
            
            if st.button("💰 تخطيط التسعير", use_container_width=True):
                st.session_state.page = "pricing_planning"
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
# تحميل الجلسة المحفوظة إن وجدت
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    # محاولة استعادة الجلسة
    saved_session = load_session()
    if saved_session:
        st.session_state.user = saved_session["username"]
        st.session_state.role = saved_session["role"]
        st.session_state.logged_in = True
        st.session_state.page = "home"

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
    elif page == "revenue_tracking" and st.session_state.role == "admin":
        monthly_revenue_tracking()
    elif page == "moraselaty" and st.session_state.role == "admin":
        create_moraselaty_campaign()
    elif page == "pricing_planning" and st.session_state.role == "admin":
        from pricing_planning import pricing_planning
        pricing_planning()
    else:
        home()

