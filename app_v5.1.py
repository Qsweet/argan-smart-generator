# ============================================
# 🌿 Argan Package Smart Script Generator v5.1
# المطور: د. محمد القضاه
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
# 🔐 دوال الأمان
# ============================================
def hash_password(password):
    """تشفير كلمة المرور باستخدام SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """التحقق من كلمة المرور"""
    return hash_password(password) == hashed

# ============================================
# 💾 دوال حفظ وتحميل البيانات
# ============================================
def save_json(filename, data):
    """حفظ البيانات في ملف JSON بشكل آمن"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"❌ خطأ في حفظ الملف: {str(e)}")
        return False

def load_json(filename, default=None):
    """تحميل البيانات من ملف JSON بشكل آمن"""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # إنشاء الملف إذا لم يكن موجوداً
            if default is not None:
                save_json(filename, default)
            return default if default is not None else {}
    except json.JSONDecodeError:
        st.warning(f"⚠️ ملف {filename} تالف، سيتم إنشاء ملف جديد")
        return default if default is not None else {}
    except Exception as e:
        st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
        return default if default is not None else {}

# ============================================
# 📊 تحميل البيانات الأساسية
# ============================================
USERS = load_json("users.json", {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"}
})

OPTIONS = load_json("options.json", {
    "offer": ["خصم 20%", "خصم 50%"],
    "product": ["زيت الأرغان"],
    "platform": ["TikTok", "Instagram"],
    "scenario": ["توعوي", "ترفيهي"],
    "shipping": ["مجاني", "مدفوع"],
    "gift": ["لا يوجد", "هدية مجانية"],
    "cashback": ["لا يوجد", "5%", "10%"],
    "tone": ["رسمي", "ودي"]
})

CAMPAIGNS = load_json("campaigns.json", [])

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

# ============================================
# 🗓️ صفحة تخطيط الحملات (محسّنة ومتقدمة)
# ============================================
def campaigns_planning():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>📅 تخطيط الحملات</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>إدارة شاملة لجميع الحملات التسويقية</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    campaigns = load_json("campaign_plans.json", [])
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
                            👤 {camp['created_by']}
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
            if camp["products"]:
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
# 🏠 باقي الصفحات (مختصرة)
# ============================================
def home_page():
    load_custom_css()
    st.markdown("""
        <div class='main-card'>
            <h1>🌿 نظام إدارة المحتوى الذكي</h1>
            <p>شركة Argan Package</p>
        </div>
    """, unsafe_allow_html=True)
    st.success("✅ تم تسجيل الدخول بنجاح!")

def login_screen():
    load_custom_css()
    st.markdown("""
        <div class='main-card'>
            <h1>🌿 نظام Argan Package</h1>
            <p>نظام إدارة المحتوى الذكي</p>
        </div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("🧑‍💼 اسم المستخدم:")
    password = st.text_input("🔒 كلمة المرور:", type="password")
    
    if st.button("🚀 تسجيل الدخول", use_container_width=True, type="primary"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = USERS[username]["role"]
            st.session_state.page = "home"
            st.success("✅ تم تسجيل الدخول بنجاح!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.page = "login"
    st.rerun()

# ============================================
# 🎯 التطبيق الرئيسي
# ============================================
def main():
    # تهيئة الجلسة
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    # التحقق من تسجيل الدخول
    if not st.session_state.logged_in:
        login_screen()
        return
    
    # القائمة الجانبية
    with st.sidebar:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;'>
                <h3 style='margin: 0;'>👋 مرحباً</h3>
                <p style='margin: 0.5rem 0 0 0;'>{st.session_state.user}</p>
                <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>{st.session_state.role.upper()}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🧭 القائمة الرئيسية")
        
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        
        if st.session_state.role == "admin":
            st.markdown("### 🔧 أدوات الإدارة")
            
            if st.button("📅 تخطيط الحملات", use_container_width=True):
                st.session_state.page = "campaigns"
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
            logout()
        
        st.markdown("---")
        st.markdown("**🌿 Argan Package**")
        st.markdown("v5.1")
    
    # عرض الصفحة المطلوبة
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "campaigns":
        campaigns_planning()

if __name__ == "__main__":
    main()

