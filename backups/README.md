# 📦 نظام النسخ الاحتياطي الاحترافي

## 🎯 نظرة عامة

هذا المجلد يحتوي على جميع النسخ الاحتياطية التلقائية لمشروع Argan Smart Generator.

---

## 🚀 استخدام سكريبت النسخ الاحتياطي

### الأوامر المتاحة:

```bash
# نسخة احتياطية كاملة (افتراضي)
./create_backup.sh full

# نسخ الملفات الأساسية فقط
./create_backup.sh files

# نسخ قواعد البيانات فقط
./create_backup.sh db

# عرض قائمة النسخ المتوفرة
./create_backup.sh list
```

---

## 📋 أنواع النسخ الاحتياطية

### 1. النسخة الكاملة (Full Backup)

**الاسم:** `full-backup-YYYYMMDD-HHMMSS.tar.gz`

**يشمل:**
- جميع ملفات Python (.py)
- جميع ملفات Markdown (.md)
- جميع ملفات JSON (.json)
- جميع ملفات التكوين
- جميع ملفات البيانات

**يستثني:**
- مجلد `.git`
- مجلد `__pycache__`
- ملفات `.pyc`
- مجلد `backups` (لتجنب التكرار)
- مجلد `venv` أو `env`
- مجلد `.streamlit/cache`

**الاستخدام:**
```bash
./create_backup.sh full
```

---

### 2. نسخة الملفات (Files Backup)

**الاسم:** `files-backup-YYYYMMDD-HHMMSS.tar.gz`

**يشمل:**
- ملفات Python (.py)
- ملفات Markdown (.md)
- ملفات النصوص (.txt)
- ملفات JSON (.json)
- ملفات YAML (.yaml, .yml)
- ملف requirements.txt

**الاستخدام:**
```bash
./create_backup.sh files
```

---

### 3. نسخة قواعد البيانات (Database Backup)

**الاسم:** `db-backup-YYYYMMDD-HHMMSS.tar.gz`

**يشمل:**
- جميع ملفات JSON (.json)
- جميع ملفات SQLite (.db, .sqlite, .sqlite3)

**الاستخدام:**
```bash
./create_backup.sh db
```

---

## 🔄 استعادة النسخة الاحتياطية

### الطريقة 1: استعادة كاملة

```bash
# 1. اذهب إلى مجلد الاستعادة
cd /path/to/restore/location

# 2. فك ضغط النسخة الاحتياطية
tar -xzf full-backup-YYYYMMDD-HHMMSS.tar.gz

# 3. انتقل إلى المجلد المستعاد
cd argan-smart-generator

# 4. ثبت المتطلبات
pip install -r requirements.txt

# 5. شغل التطبيق
streamlit run app.py
```

---

### الطريقة 2: استعادة ملف محدد

```bash
# عرض محتويات النسخة الاحتياطية
tar -tzf full-backup-YYYYMMDD-HHMMSS.tar.gz

# استخراج ملف محدد
tar -xzf full-backup-YYYYMMDD-HHMMSS.tar.gz argan-smart-generator/pricing_planning.py

# نسخ الملف المستعاد
cp argan-smart-generator/pricing_planning.py /path/to/project/
```

---

### الطريقة 3: استعادة قاعدة بيانات فقط

```bash
# فك ضغط نسخة قاعدة البيانات
tar -xzf db-backup-YYYYMMDD-HHMMSS.tar.gz

# نسخ ملفات JSON
cp *.json /path/to/project/
```

---

## 🧹 إدارة النسخ الاحتياطية

### التنظيف التلقائي

السكريبت يحتفظ تلقائياً بآخر **10 نسخ احتياطية** فقط ويحذف الأقدم.

### التنظيف اليدوي

```bash
# حذف نسخة محددة
rm backups/full-backup-20251015-032841.tar.gz
rm backups/full-backup-20251015-032841.info

# حذف جميع النسخ الأقدم من 30 يوم
find backups/ -name "*.tar.gz" -mtime +30 -delete
find backups/ -name "*.info" -mtime +30 -delete
```

---

## 📊 معلومات النسخة الاحتياطية

كل نسخة احتياطية تأتي مع ملف معلومات `.info` يحتوي على:

- اسم الملف
- التاريخ والوقت
- نوع النسخة
- الحجم
- المضيف
- المستخدم
- المسار
- تعليمات الاستعادة

**مثال:**
```bash
cat backups/full-backup-20251015-032841.info
```

---

## ⚙️ الجدولة التلقائية (Cron)

### نسخة احتياطية يومية (كل يوم الساعة 2 صباحاً)

```bash
# فتح crontab
crontab -e

# إضافة السطر التالي
0 2 * * * /path/to/argan-smart-generator/create_backup.sh full >> /path/to/argan-smart-generator/backups/backup.log 2>&1
```

### نسخة احتياطية أسبوعية (كل أحد الساعة 3 صباحاً)

```bash
0 3 * * 0 /path/to/argan-smart-generator/create_backup.sh full >> /path/to/argan-smart-generator/backups/backup.log 2>&1
```

### نسخة احتياطية شهرية (أول كل شهر)

```bash
0 4 1 * * /path/to/argan-smart-generator/create_backup.sh full >> /path/to/argan-smart-generator/backups/backup.log 2>&1
```

---

## 🔐 أفضل الممارسات

### 1. النسخ الاحتياطي المنتظم

- **يومي:** للبيانات الحرجة
- **أسبوعي:** للمشاريع النشطة
- **شهري:** للمشاريع المستقرة

### 2. التخزين الآمن

```bash
# نسخ النسخة الاحتياطية إلى سيرفر آخر
scp backups/full-backup-*.tar.gz user@backup-server:/backups/

# رفع إلى التخزين السحابي
rclone copy backups/ remote:argan-backups/
```

### 3. التحقق من النسخ

```bash
# اختبار سلامة الملف المضغوط
tar -tzf backups/full-backup-20251015-032841.tar.gz > /dev/null && echo "✅ الملف سليم" || echo "❌ الملف تالف"
```

### 4. التوثيق

احتفظ بسجل للنسخ الاحتياطية:
```bash
# إنشاء سجل
./create_backup.sh full >> backups/backup.log 2>&1
```

---

## 📁 هيكل المجلد

```
backups/
├── README.md                                    # هذا الملف
├── full-backup-20251015-032841.tar.gz          # نسخة كاملة
├── full-backup-20251015-032841.info            # معلومات النسخة
├── files-backup-20251014-120000.tar.gz         # نسخة ملفات
├── files-backup-20251014-120000.info           # معلومات
├── db-backup-20251013-180000.tar.gz            # نسخة قواعد بيانات
├── db-backup-20251013-180000.info              # معلومات
└── backup.log                                   # سجل العمليات
```

---

## 🆘 استكشاف الأخطاء

### المشكلة: "Permission denied"

```bash
chmod +x ../create_backup.sh
```

### المشكلة: "No space left on device"

```bash
# حذف النسخ القديمة
rm backups/full-backup-202510*.tar.gz

# أو نقلها إلى مكان آخر
mv backups/*.tar.gz /path/to/external/storage/
```

### المشكلة: الملف المضغوط تالف

```bash
# التحقق من سلامة الملف
tar -tzf backups/full-backup-*.tar.gz

# إذا كان تالفاً، استخدم نسخة أقدم
./create_backup.sh list
```

---

## 📞 الدعم

للمساعدة أو الإبلاغ عن مشاكل:
- راجع ملف `backup.log`
- تواصل مع فريق التطوير

---

**🌿 Argan Package - النسخ الاحتياطي الاحترافي**

**آخر تحديث:** 15 أكتوبر 2025

