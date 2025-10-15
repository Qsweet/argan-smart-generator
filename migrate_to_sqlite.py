#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحويل moraselaty_customers.json إلى SQLite
Argan Smart Generator - Performance Optimization
"""

import json
import sqlite3
import os
from datetime import datetime


def migrate_customers_to_sqlite():
    """تحويل ملف JSON إلى قاعدة بيانات SQLite"""
    
    print("=" * 60)
    print("🔄 بدء عملية التحويل إلى SQLite")
    print("=" * 60)
    
    # قراءة ملف JSON
    print("\n📖 قراءة ملف moraselaty_customers.json...")
    try:
        with open('moraselaty_customers.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return False
    
    orders = data.get('orders', [])
    total_orders = len(orders)
    print(f"✅ تم قراءة {total_orders:,} طلب")
    
    # إنشاء قاعدة البيانات
    print("\n🗄️  إنشاء قاعدة البيانات...")
    db_path = 'database/customers.db'
    
    # حذف قاعدة البيانات القديمة إن وجدت
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  تم حذف قاعدة البيانات القديمة")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # إنشاء الجدول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number INTEGER,
            customer_name TEXT,
            seller TEXT,
            order_entry TEXT,
            total_amount REAL,
            currency TEXT,
            tax INTEGER,
            phone TEXT,
            receiver_phone TEXT,
            shipping_address TEXT,
            city TEXT,
            country TEXT,
            products_total REAL,
            shipping_fees REAL,
            payment_fees REAL,
            status TEXT,
            order_date TEXT,
            shipping_date TEXT,
            delivery_date TEXT,
            payment_method TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_order_number ON orders(order_number)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_customer_name ON orders(customer_name)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_city ON orders(city)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)
    ''')
    
    print("✅ تم إنشاء الجدول والفهارس")
    
    # إدراج البيانات
    print(f"\n💾 إدراج {total_orders:,} طلب...")
    
    inserted = 0
    errors = 0
    
    for i, order in enumerate(orders, 1):
        try:
            cursor.execute('''
                INSERT INTO orders (
                    order_number, customer_name, seller, order_entry,
                    total_amount, currency, tax, phone, receiver_phone,
                    shipping_address, city, country, products_total,
                    shipping_fees, payment_fees, status, order_date,
                    shipping_date, delivery_date, payment_method, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order.get('رقم الطلب'),
                order.get('اسم العميل'),
                order.get('البائع'),
                order.get('مدخل الطلبيه'),
                order.get('المبلغ الاجمالي'),
                order.get('العملة'),
                order.get('الضريبة'),
                str(order.get('رقم الهاتف', '')),
                str(order.get('هاتف المستلم', '')),
                order.get('عنوان الشحن'),
                order.get('المدينة'),
                order.get('الدولة'),
                order.get('اجمالي المنتجات'),
                order.get('رسوم الشحن'),
                order.get(' رسوم الدفع'),
                order.get('الحالة'),
                order.get('تاريخ الطلب'),
                order.get('تاريخ الشحن'),
                order.get('تاريخ التسليم'),
                order.get('طريقة الدفع'),
                order.get('ملاحظات')
            ))
            inserted += 1
            
            # عرض التقدم
            if i % 1000 == 0:
                print(f"  ⏳ تم إدراج {i:,} / {total_orders:,} ({i/total_orders*100:.1f}%)")
        
        except Exception as e:
            errors += 1
            if errors <= 5:  # عرض أول 5 أخطاء فقط
                print(f"  ⚠️  خطأ في الطلب رقم {order.get('رقم الطلب', 'غير معروف')}: {e}")
    
    # حفظ التغييرات
    conn.commit()
    
    # إحصائيات
    cursor.execute('SELECT COUNT(*) FROM orders')
    total_in_db = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT customer_name) FROM orders')
    unique_customers = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(total_amount) FROM orders')
    total_revenue = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # النتائج
    print("\n" + "=" * 60)
    print("✅ تمت عملية التحويل بنجاح!")
    print("=" * 60)
    print(f"\n📊 الإحصائيات:")
    print(f"  • إجمالي الطلبات: {total_in_db:,}")
    print(f"  • العملاء الفريدون: {unique_customers:,}")
    print(f"  • إجمالي الإيرادات: {total_revenue:,.2f} ر.س")
    print(f"  • الطلبات المدرجة: {inserted:,}")
    print(f"  • الأخطاء: {errors}")
    
    # حجم الملفات
    json_size = os.path.getsize('moraselaty_customers.json') / (1024 * 1024)
    db_size = os.path.getsize(db_path) / (1024 * 1024)
    
    print(f"\n💾 حجم الملفات:")
    print(f"  • JSON: {json_size:.2f} MB")
    print(f"  • SQLite: {db_size:.2f} MB")
    print(f"  • التوفير: {json_size - db_size:.2f} MB ({(1 - db_size/json_size)*100:.1f}%)")
    
    print(f"\n📁 موقع قاعدة البيانات: {db_path}")
    print("\n✨ يمكنك الآن استخدام قاعدة البيانات في التطبيق!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    migrate_customers_to_sqlite()

