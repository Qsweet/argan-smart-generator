#!/bin/bash
#
# سكريبت النسخ الاحتياطي الاحترافي لمشروع Argan Smart Generator
# الاستخدام: ./create_backup.sh [نوع النسخة]
# الأنواع: full (كامل) | files (ملفات فقط) | db (قواعد بيانات فقط)
#

# الألوان للعرض
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # بدون لون

# المتغيرات
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${PROJECT_DIR}/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
DATE_READABLE=$(date '+%Y-%m-%d %H:%M:%S')
BACKUP_TYPE=${1:-full}

# إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً
mkdir -p "${BACKUP_DIR}"

# دالة طباعة رسالة ملونة
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# دالة إنشاء نسخة احتياطية كاملة
create_full_backup() {
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "${BLUE}" "🔄 بدء عملية النسخ الاحتياطي الكامل..."
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    BACKUP_NAME="full-backup-${TIMESTAMP}"
    BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
    
    print_message "${YELLOW}" "📦 جاري ضغط الملفات..."
    
    cd "$(dirname "${PROJECT_DIR}")"
    tar --exclude="$(basename "${PROJECT_DIR}")/backups" \
        --exclude="$(basename "${PROJECT_DIR}")/.git" \
        --exclude="$(basename "${PROJECT_DIR}")/__pycache__" \
        --exclude="$(basename "${PROJECT_DIR}")/**/__pycache__" \
        --exclude="$(basename "${PROJECT_DIR}")/*.pyc" \
        --exclude="$(basename "${PROJECT_DIR}")/**/*.pyc" \
        --exclude="$(basename "${PROJECT_DIR}")/.streamlit/cache" \
        --exclude="$(basename "${PROJECT_DIR}")/venv" \
        --exclude="$(basename "${PROJECT_DIR}")/env" \
        -czf "${BACKUP_FILE}" "$(basename "${PROJECT_DIR}")/" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
        print_message "${GREEN}" "✅ تم إنشاء النسخة الاحتياطية بنجاح!"
        print_message "${GREEN}" "📁 الملف: ${BACKUP_NAME}.tar.gz"
        print_message "${GREEN}" "💾 الحجم: ${BACKUP_SIZE}"
        
        # إنشاء ملف معلومات
        create_backup_info "${BACKUP_NAME}" "full" "${BACKUP_SIZE}"
    else
        print_message "${RED}" "❌ فشل إنشاء النسخة الاحتياطية!"
        return 1
    fi
}

# دالة إنشاء نسخة احتياطية للملفات فقط
create_files_backup() {
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "${BLUE}" "📄 بدء نسخ الملفات الأساسية فقط..."
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    BACKUP_NAME="files-backup-${TIMESTAMP}"
    BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
    
    cd "${PROJECT_DIR}"
    tar -czf "${BACKUP_FILE}" \
        *.py \
        *.md \
        *.txt \
        *.json \
        *.yaml \
        *.yml \
        requirements.txt 2>/dev/null
    
    if [ $? -eq 0 ]; then
        BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
        print_message "${GREEN}" "✅ تم نسخ الملفات بنجاح!"
        print_message "${GREEN}" "📁 الملف: ${BACKUP_NAME}.tar.gz"
        print_message "${GREEN}" "💾 الحجم: ${BACKUP_SIZE}"
        
        create_backup_info "${BACKUP_NAME}" "files" "${BACKUP_SIZE}"
    else
        print_message "${RED}" "❌ فشل نسخ الملفات!"
        return 1
    fi
}

# دالة إنشاء نسخة احتياطية لقواعد البيانات
create_db_backup() {
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "${BLUE}" "🗄️  بدء نسخ قواعد البيانات..."
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    BACKUP_NAME="db-backup-${TIMESTAMP}"
    BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
    
    cd "${PROJECT_DIR}"
    tar -czf "${BACKUP_FILE}" \
        *.json \
        *.db \
        *.sqlite \
        *.sqlite3 2>/dev/null
    
    if [ $? -eq 0 ]; then
        BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
        print_message "${GREEN}" "✅ تم نسخ قواعد البيانات بنجاح!"
        print_message "${GREEN}" "📁 الملف: ${BACKUP_NAME}.tar.gz"
        print_message "${GREEN}" "💾 الحجم: ${BACKUP_SIZE}"
        
        create_backup_info "${BACKUP_NAME}" "database" "${BACKUP_SIZE}"
    else
        print_message "${RED}" "❌ فشل نسخ قواعد البيانات!"
        return 1
    fi
}

# دالة إنشاء ملف معلومات النسخة الاحتياطية
create_backup_info() {
    local backup_name=$1
    local backup_type=$2
    local backup_size=$3
    
    INFO_FILE="${BACKUP_DIR}/${backup_name}.info"
    
    cat > "${INFO_FILE}" << EOF
# معلومات النسخة الاحتياطية
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 اسم الملف: ${backup_name}.tar.gz
📅 التاريخ والوقت: ${DATE_READABLE}
🏷️  نوع النسخة: ${backup_type}
💾 الحجم: ${backup_size}
🖥️  المضيف: $(hostname)
👤 المستخدم: $(whoami)
📂 المسار: ${BACKUP_DIR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## لاستعادة النسخة الاحتياطية:

cd /path/to/restore/location
tar -xzf ${backup_name}.tar.gz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
    
    print_message "${BLUE}" "📝 تم إنشاء ملف المعلومات: ${backup_name}.info"
}

# دالة حذف النسخ القديمة (الاحتفاظ بآخر 10 نسخ)
cleanup_old_backups() {
    print_message "${YELLOW}" "\n🧹 جاري تنظيف النسخ القديمة..."
    
    cd "${BACKUP_DIR}"
    BACKUP_COUNT=$(ls -1 *.tar.gz 2>/dev/null | wc -l)
    
    if [ "${BACKUP_COUNT}" -gt 10 ]; then
        print_message "${YELLOW}" "📊 عدد النسخ الحالية: ${BACKUP_COUNT}"
        print_message "${YELLOW}" "🗑️  حذف النسخ الأقدم من 10..."
        
        ls -t *.tar.gz | tail -n +11 | while read file; do
            rm -f "${file}"
            rm -f "${file%.tar.gz}.info"
            print_message "${YELLOW}" "   ❌ تم حذف: ${file}"
        done
        
        print_message "${GREEN}" "✅ تم التنظيف بنجاح!"
    else
        print_message "${GREEN}" "✅ عدد النسخ (${BACKUP_COUNT}) ضمن الحد المسموح"
    fi
}

# دالة عرض قائمة النسخ الاحتياطية
list_backups() {
    print_message "${BLUE}" "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "${BLUE}" "📋 قائمة النسخ الاحتياطية المتوفرة:"
    print_message "${BLUE}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    cd "${BACKUP_DIR}"
    if [ -n "$(ls -A *.tar.gz 2>/dev/null)" ]; then
        ls -lht *.tar.gz | awk '{printf "%-50s %5s %s %s %s\n", $9, $5, $6, $7, $8}'
    else
        print_message "${YELLOW}" "⚠️  لا توجد نسخ احتياطية متوفرة"
    fi
    
    print_message "${BLUE}" "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# البرنامج الرئيسي
main() {
    print_message "${GREEN}" "\n"
    print_message "${GREEN}" "╔════════════════════════════════════════════════╗"
    print_message "${GREEN}" "║   🌿 Argan Smart Generator Backup System 🌿   ║"
    print_message "${GREEN}" "╚════════════════════════════════════════════════╝"
    print_message "${GREEN}" "\n"
    
    case "${BACKUP_TYPE}" in
        full)
            create_full_backup
            ;;
        files)
            create_files_backup
            ;;
        db)
            create_db_backup
            ;;
        list)
            list_backups
            return 0
            ;;
        *)
            print_message "${RED}" "❌ نوع نسخة غير صحيح: ${BACKUP_TYPE}"
            print_message "${YELLOW}" "\nالاستخدام:"
            print_message "${YELLOW}" "  ./create_backup.sh [full|files|db|list]"
            print_message "${YELLOW}" "\nالأنواع المتاحة:"
            print_message "${YELLOW}" "  full  - نسخة احتياطية كاملة (افتراضي)"
            print_message "${YELLOW}" "  files - نسخ الملفات الأساسية فقط"
            print_message "${YELLOW}" "  db    - نسخ قواعد البيانات فقط"
            print_message "${YELLOW}" "  list  - عرض قائمة النسخ المتوفرة"
            return 1
            ;;
    esac
    
    # تنظيف النسخ القديمة
    cleanup_old_backups
    
    # عرض قائمة النسخ
    list_backups
    
    print_message "${GREEN}" "\n✨ تمت العملية بنجاح!"
    print_message "${GREEN}" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
}

# تشغيل البرنامج
main

