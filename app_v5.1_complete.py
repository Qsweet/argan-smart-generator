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
# 📅 صفحة تخطيط الحملات (محسّنة ومتقدمة v5.1)
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
                    "created_by": st.session_state.get("user", "admin"),
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "products": []
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
    
    for i, camp in enumerate(campaigns):
        with st.container():
            # عنوان الحملة
            col_title, col_delete = st.columns([5, 1])
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
                if st.button("🗑️", key=f"del_camp_{i}", help="حذف الحملة"):
                    campaigns.pop(i)
                    save_json("campaign_plans.json", campaigns)
                    st.rerun()
            
            # إضافة منتج للحملة
            with st.expander("➕ إضافة منتج إلى الحملة", expanded=False):
                # اختيار المنتج
                selected_product = st.selectbox(
                    "🧴 اختر المنتج:",
                    product_list,
                    key=f"prod_{i}",
                    help="اختر المنتج من القائمة"
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
                if st.button("💾 إضافة المنتج", key=f"add_prod_{i}", use_container_width=True, type="primary"):
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
                    videos_str = ", ".join([f"{v['type']} ({v['count']})" for v in p.get("videos", [])])
                    designs_str = ", ".join([f"{d['type']} ({d['count']})" for d in p.get("designs", [])])
                    
                    products_data.append({
                        "المنتج": p["product_name"],
                        "السعر الحالي": f"{p['current_price']} ر.س",
                        "سعر الحملة": f"{p['campaign_price']} ر.س",
                        "نوع الخصم": p["discount_type"],
                        "الكود": p.get("discount_code", "—"),
                        "الفيديوهات": videos_str if videos_str else "—",
                        "التصاميم": designs_str if designs_str else "—"
                    })
                
                df = pd.DataFrame(products_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # خيارات التعديل
                st.markdown("##### ✏️ تعديل المنتجات")
                product_to_edit = st.selectbox(
                    "اختر منتج للتعديل:",
                    [p["product_name"] for p in camp["products"]],
                    key=f"edit_select_{i}"
                )
                
                col_edit, col_del = st.columns(2)
                
                with col_edit:
                    if st.button("✏️ تعديل", key=f"edit_btn_{i}", use_container_width=True):
                        st.info("💡 قريباً: سيتم إضافة واجهة تعديل تفاعلية")
                
                with col_del:
                    if st.button("🗑️ حذف المنتج", key=f"del_prod_{i}", use_container_width=True, type="secondary"):
                        camp["products"] = [p for p in camp["products"] if p["product_name"] != product_to_edit]
                        save_json("campaign_plans.json", campaigns)
                        st.success(f"✅ تم حذف {product_to_edit}")
                        st.rerun()
            else:
                st.info("📭 لم تتم إضافة أي منتجات بعد")
            
            st.markdown("---")

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

