#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحويل revenue_data.json إلى SQLite
Argan Smart Generator
"""

import sqlite3
import json
import os
from datetime import datetime


def create_database():
    """إنشاء قاعدة البيانات والجداول"""
    
    # حذف قاعدة البيانات القديمة إن وجدت
    db_path = 'database/revenues.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ تم حذف قاعدة البيانات القديمة")
    
    # إنشاء الاتصال
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # جدول الأشهر
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS months (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_name TEXT UNIQUE NOT NULL,
        month_number INTEGER,
        year INTEGER,
        last_update DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # جدول المصاريف
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_id INTEGER NOT NULL,
        expense_type TEXT NOT NULL,
        value REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (month_id) REFERENCES months(id)
    )
    ''')
    
    # جدول الإيرادات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS revenues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_id INTEGER NOT NULL,
        revenue_type TEXT NOT NULL,
        value REAL NOT NULL,
        roi REAL,
        orders INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (month_id) REFERENCES months(id)
    )
    ''')
    
    # إنشاء فهارس للأداء
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_expenses_month ON expenses(month_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_revenues_month ON revenues(month_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_months_name ON months(month_name)')
    
    conn.commit()
    print(f"✅ تم إنشاء قاعدة البيانات والجداول")
    
    return conn


def parse_month_info(month_name):
    """استخراج رقم الشهر والسنة من اسم الشهر"""
    month_mapping = {
        'يناير': 1, 'فبراير': 2, 'مارس': 3, 'ابريل': 4,
        'مايو': 5, 'يونيو': 6, 'يوليو': 7, 'أغسطس': 8,
        'سبتمبر': 9, 'أكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12
    }
    
    # محاولة استخراج السنة
    year = 2025  # افتراضي
    if '2025' in month_name:
        year = 2025
    elif '2024' in month_name:
        year = 2024
    
    # محاولة استخراج رقم الشهر
    month_number = None
    
    # إذا كان بصيغة "شهر 8"
    if 'شهر' in month_name:
        parts = month_name.split()
        for part in parts:
            if part.isdigit():
                month_number = int(part)
                break
    
    # إذا كان باسم الشهر
    for ar_month, num in month_mapping.items():
        if ar_month in month_name:
            month_number = num
            break
    
    return month_number, year


def migrate_data(conn):
    """تحويل البيانات من JSON إلى SQLite"""
    
    cursor = conn.cursor()
    
    # قراءة ملف JSON
    with open('revenue_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📊 بدء تحويل {len(data)} شهر...")
    
    total_expenses = 0
    total_revenues = 0
    
    for month_name, month_data in data.items():
        # إضافة الشهر
        month_number, year = parse_month_info(month_name)
        last_update = month_data.get('last_update', datetime.now().strftime('%Y-%m-%d'))
        
        cursor.execute('''
        INSERT INTO months (month_name, month_number, year, last_update)
        VALUES (?, ?, ?, ?)
        ''', (month_name, month_number, year, last_update))
        
        month_id = cursor.lastrowid
        
        # إضافة المصاريف
        if 'expenses' in month_data:
            for expense in month_data['expenses']:
                cursor.execute('''
                INSERT INTO expenses (month_id, expense_type, value)
                VALUES (?, ?, ?)
                ''', (month_id, expense['type'], expense['value']))
                total_expenses += 1
        
        # إضافة الإيرادات
        if 'revenues' in month_data:
            for revenue in month_data['revenues']:
                cursor.execute('''
                INSERT INTO revenues (month_id, revenue_type, value, roi, orders)
                VALUES (?, ?, ?, ?, ?)
                ''', (month_id, revenue['type'], revenue['value'], 
                      revenue.get('roi'), revenue.get('orders', 0)))
                total_revenues += 1
        
        print(f"  ✅ {month_name}")
    
    conn.commit()
    
    print(f"\n✅ تم تحويل:")
    print(f"   - {len(data)} شهر")
    print(f"   - {total_expenses} مصروف")
    print(f"   - {total_revenues} إيراد")
    
    return len(data), total_expenses, total_revenues


def verify_data(conn):
    """التحقق من البيانات"""
    
    cursor = conn.cursor()
    
    print(f"\n🔍 التحقق من البيانات...")
    
    # عدد الأشهر
    cursor.execute('SELECT COUNT(*) FROM months')
    months_count = cursor.fetchone()[0]
    print(f"   ✅ الأشهر: {months_count}")
    
    # عدد المصاريف
    cursor.execute('SELECT COUNT(*) FROM expenses')
    expenses_count = cursor.fetchone()[0]
    print(f"   ✅ المصاريف: {expenses_count}")
    
    # عدد الإيرادات
    cursor.execute('SELECT COUNT(*) FROM revenues')
    revenues_count = cursor.fetchone()[0]
    print(f"   ✅ الإيرادات: {revenues_count}")
    
    # إجمالي المصاريف
    cursor.execute('SELECT SUM(value) FROM expenses')
    total_expenses = cursor.fetchone()[0] or 0
    print(f"   💰 إجمالي المصاريف: {total_expenses:,.2f} ر.س")
    
    # إجمالي الإيرادات
    cursor.execute('SELECT SUM(value) FROM revenues')
    total_revenues = cursor.fetchone()[0] or 0
    print(f"   💰 إجمالي الإيرادات: {total_revenues:,.2f} ر.س")
    
    # صافي الربح
    net_profit = total_revenues - total_expenses
    print(f"   💰 صافي الربح: {net_profit:,.2f} ر.س")
    
    return {
        'months': months_count,
        'expenses': expenses_count,
        'revenues': revenues_count,
        'total_expenses': total_expenses,
        'total_revenues': total_revenues,
        'net_profit': net_profit
    }


def get_database_size():
    """الحصول على حجم قاعدة البيانات"""
    db_path = 'database/revenues.db'
    if os.path.exists(db_path):
        size_bytes = os.path.getsize(db_path)
        size_kb = size_bytes / 1024
        return size_kb
    return 0


def main():
    """الدالة الرئيسية"""
    
    print("=" * 60)
    print("🚀 تحويل revenue_data.json إلى SQLite")
    print("=" * 60)
    
    # إنشاء قاعدة البيانات
    conn = create_database()
    
    # تحويل البيانات
    months, expenses, revenues = migrate_data(conn)
    
    # التحقق من البيانات
    stats = verify_data(conn)
    
    # إغلاق الاتصال
    conn.close()
    
    # حجم قاعدة البيانات
    db_size = get_database_size()
    
    # حجم ملف JSON الأصلي
    json_size = os.path.getsize('revenue_data.json') / 1024
    
    print(f"\n📦 الأحجام:")
    print(f"   - JSON: {json_size:.2f} KB")
    print(f"   - SQLite: {db_size:.2f} KB")
    
    if db_size < json_size:
        savings = ((json_size - db_size) / json_size) * 100
        print(f"   ✅ توفير: {savings:.1f}%")
    
    print(f"\n" + "=" * 60)
    print(f"✅ تم التحويل بنجاح!")
    print(f"=" * 60)
    
    return stats


if __name__ == '__main__':
    main()

