#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحويل كلمات المرور من plain text إلى bcrypt
Argan Smart Generator
"""

import json
import bcrypt
import os
from datetime import datetime


def hash_password(password: str) -> str:
    """تشفير كلمة المرور باستخدام bcrypt"""
    # تحويل كلمة المرور إلى bytes
    password_bytes = password.encode('utf-8')
    
    # إنشاء salt وتشفير
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds = آمن وسريع
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # تحويل إلى string للتخزين
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """التحقق من كلمة المرور"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def migrate_users():
    """تحويل كلمات مرور المستخدمين"""
    
    print("=" * 60)
    print("🔒 تحويل كلمات المرور إلى bcrypt")
    print("=" * 60)
    
    # قراءة ملف المستخدمين
    users_file = 'users.json'
    
    if not os.path.exists(users_file):
        print("❌ ملف users.json غير موجود!")
        return
    
    # نسخة احتياطية
    backup_file = f'users_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
    
    # تحويل كلمات المرور
    print(f"\n📊 تحويل {len(users_data)} مستخدم...")
    
    migrated_users = {}
    
    for username, user_info in users_data.items():
        plain_password = user_info['password']
        
        # تشفير كلمة المرور
        hashed_password = hash_password(plain_password)
        
        # حفظ البيانات الجديدة
        migrated_users[username] = {
            'password': hashed_password,
            'role': user_info['role'],
            'created_at': datetime.now().isoformat(),
            'password_changed_at': datetime.now().isoformat()
        }
        
        print(f"  ✅ {username} ({user_info['role']})")
        
        # اختبار التحقق
        if verify_password(plain_password, hashed_password):
            print(f"     ✓ التحقق ناجح")
        else:
            print(f"     ✗ خطأ في التحقق!")
    
    # حفظ الملف الجديد
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(migrated_users, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم تحويل جميع كلمات المرور بنجاح!")
    print(f"📁 النسخة الاحتياطية: {backup_file}")
    
    # عرض مثال
    print(f"\n📝 مثال على كلمة مرور مشفرة:")
    example_user = list(migrated_users.keys())[0]
    example_hash = migrated_users[example_user]['password']
    print(f"   المستخدم: {example_user}")
    print(f"   Hash: {example_hash[:50]}...")
    
    print(f"\n" + "=" * 60)
    print(f"✅ اكتمل التحويل!")
    print(f"=" * 60)
    
    return migrated_users


def test_authentication():
    """اختبار نظام المصادقة الجديد"""
    
    print(f"\n" + "=" * 60)
    print(f"🧪 اختبار نظام المصادقة")
    print(f"=" * 60)
    
    # قراءة المستخدمين
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # اختبار كل مستخدم
    test_password = "1234"  # كلمة المرور الأصلية
    
    print(f"\nاختبار تسجيل الدخول بكلمة المرور: {test_password}")
    
    for username, user_info in users.items():
        hashed = user_info['password']
        
        if verify_password(test_password, hashed):
            print(f"  ✅ {username}: تسجيل دخول ناجح")
        else:
            print(f"  ❌ {username}: فشل تسجيل الدخول")
    
    # اختبار كلمة مرور خاطئة
    print(f"\nاختبار كلمة مرور خاطئة: wrong_password")
    
    example_user = list(users.keys())[0]
    example_hash = users[example_user]['password']
    
    if verify_password("wrong_password", example_hash):
        print(f"  ❌ خطأ: قبل كلمة مرور خاطئة!")
    else:
        print(f"  ✅ رفض كلمة المرور الخاطئة بنجاح")
    
    print(f"\n" + "=" * 60)


if __name__ == '__main__':
    # تحويل كلمات المرور
    migrated_users = migrate_users()
    
    # اختبار النظام
    if migrated_users:
        test_authentication()

