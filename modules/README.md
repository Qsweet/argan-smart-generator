# 📦 وحدات Argan Smart Generator

هذا المجلد يحتوي على الوحدات البرمجية المنفصلة للمشروع.

---

## 📁 الوحدات المتاحة

### 1. `auth.py` - وحدة المصادقة والجلسات

**الوظائف الرئيسية:**

```python
from modules.auth import *

# تهيئة الجلسة
init_session_state()

# تسجيل الدخول
login(username, role)
logout()

# التحقق
is_logged_in()          # هل المستخدم مسجل دخول؟
is_admin()              # هل المستخدم مدير؟
get_current_user()      # الحصول على اسم المستخدم
get_current_role()      # الحصول على دور المستخدم

# المصادقة
user = authenticate(username, password)

# إدارة المستخدمين
add_user(username, password, role, name)
update_user(username, password=new_password)
delete_user(username)

# Decorators
@require_login
def my_function():
    # يتطلب تسجيل دخول
    pass

@require_admin
def admin_function():
    # يتطلب صلاحيات مدير
    pass
```

---

### 2. `utils.py` - وحدة الأدوات المساعدة

**الوظائف الرئيسية:**

```python
from modules.utils import *

# تحميل وحفظ JSON
data = load_json("file.json")
save_json("file.json", data)

# التقويم
hijri_date = gregorian_to_hijri(datetime.now())
gregorian_date = hijri_to_gregorian(1, 1, 1446)

# الحسابات
days = calculate_days_remaining("2025-12-31")
days = calculate_days_until_start("2025-01-01")

# التنسيق
formatted = format_currency(1000.50)      # "1,000.50 ر.س"
formatted = format_number(1234.567, 2)    # "1,234.57"
formatted = format_percentage(75.5)       # "75.5%"

# الألوان والرموز
color = get_status_color("ممتاز")        # "green"
emoji = get_status_emoji("ممتاز")        # "🟢"

# التحقق من الهاتف
valid = validate_phone("0501234567")      # True
normalized = normalize_phone("0501234567") # "966501234567"

# أخرى
truncated = truncate_text("نص طويل جداً...", 10)
timestamp = get_current_timestamp()
date = get_current_date()
```

---

### 3. `database.py` - وحدة قاعدة البيانات

**الوظائف الرئيسية:**

```python
from modules.database import *

# الإحصائيات
count = get_orders_count()           # 8,462
customers = get_customers_count()    # 6,905
revenue = get_total_revenue()        # 2,318,437.79

# البحث والعرض
orders, total = get_orders_paginated(page=1, per_page=100)
results = search_orders("محمد", search_by='customer_name')
order = get_order_details(304319)

# التحليلات
df_cities = get_orders_by_city()        # DataFrame
df_months = get_orders_by_month()       # DataFrame
df_customers = get_top_customers(10)    # DataFrame

# مسح الـ cache
clear_cache()
```

---

### 4. `logger.py` - وحدة نظام السجلات

**الوظائف الرئيسية:**

```python
from modules.logger import *

# تسجيل بسيط
log_info("رسالة معلومات", user="admin")
log_warning("رسالة تحذير", user="admin")
log_error("رسالة خطأ", user="admin")

# تسجيل متقدم
logger.log_login("admin", success=True)
logger.log_logout("admin")
logger.log_action("إضافة منتج", "admin", "منتج: زيت الأرغان")
logger.log_api_call("OpenAI GPT-4", "user1", success=True)
logger.log_file_operation("save", "data.json", "admin")
logger.log_database_operation("insert", "orders", "admin")

# قراءة السجلات
recent = get_recent_logs(lines=100, log_type='app')
user_logs = get_logs_by_user("admin", lines=50)
error_count = get_error_count_today()
```

**ملفات السجلات:**
- `logs/app.log` - جميع السجلات
- `logs/errors.log` - الأخطاء فقط

**الحجم الأقصى:** 5 MB لكل ملف، يحتفظ بـ 3 ملفات احتياطية

---

## 🎯 كيفية الاستخدام

### في app.py:

```python
# بدلاً من:
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# استخدم:
from modules.auth import hash_password
```

### في الدوال:

```python
from modules.logger import logger
from modules.auth import get_current_user

def my_function():
    user = get_current_user()
    
    try:
        # ... الكود
        logger.log_action("عملية ناجحة", user)
    except Exception as e:
        logger.log_error_with_context(e, "فشل في العملية", user)
```

---

## 📊 الفوائد

### قبل:
- كود مكرر في app.py (2,594 سطر)
- صعوبة الصيانة
- لا يوجد logging منظم

### بعد:
- كود منظم في وحدات
- سهولة الصيانة والتطوير
- نظام logging احترافي
- إمكانية إعادة الاستخدام

---

## 🔄 التحديثات المستقبلية

يمكن إضافة وحدات جديدة:
- `campaigns.py` - إدارة الحملات
- `revenue.py` - تتبع الإيرادات
- `notifications.py` - نظام الإشعارات
- `reports.py` - تقارير احترافية

---

## 📝 ملاحظات

- جميع الوحدات تستخدم `@st.cache_data` للأداء
- الوحدات مستقلة ويمكن استخدامها منفصلة
- التوثيق موجود في كل دالة (docstrings)
- متوافقة مع Python 3.8+

---

**تم إنشاء هذه الوحدات في:** 15 أكتوبر 2025  
**الإصدار:** v7.1 - Performance Optimization Phase 2

