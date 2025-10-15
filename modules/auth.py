#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة المصادقة والجلسات
Argan Smart Generator
"""

import streamlit as st
import hashlib
import json
import os
from typing import Optional, Dict


def hash_password(password: str) -> str:
    """تشفير كلمة المرور باستخدام MD5"""
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """التحقق من كلمة المرور"""
    return hash_password(password) == hashed


def init_session_state():
    """تهيئة session_state بالقيم الافتراضية"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'


def login(username: str, role: str):
    """تسجيل دخول المستخدم"""
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.role = role
    st.session_state.page = 'home'


def logout():
    """تسجيل خروج المستخدم"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = 'home'


def is_logged_in() -> bool:
    """التحقق من تسجيل الدخول"""
    return st.session_state.get('logged_in', False)


def get_current_user() -> Optional[str]:
    """الحصول على اسم المستخدم الحالي"""
    return st.session_state.get('username')


def get_current_role() -> Optional[str]:
    """الحصول على دور المستخدم الحالي"""
    return st.session_state.get('role')


def is_admin() -> bool:
    """التحقق من أن المستخدم مدير"""
    return st.session_state.get('role') == 'admin'


def require_login(func):
    """Decorator للتحقق من تسجيل الدخول"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.warning("⚠️ يجب تسجيل الدخول أولاً")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    """Decorator للتحقق من صلاحيات المدير"""
    def wrapper(*args, **kwargs):
        if not is_admin():
            st.error("⛔ هذه الصفحة متاحة للمديرين فقط")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


@st.cache_data(ttl=300)
def load_users() -> Dict:
    """تحميل بيانات المستخدمين"""
    try:
        if not os.path.exists("users.json"):
            default_users = {
                "admin": {
                    "password": hash_password("admin123"),
                    "role": "admin",
                    "name": "المدير"
                }
            }
            with open("users.json", "w", encoding="utf-8") as f:
                json.dump(default_users, f, ensure_ascii=False, indent=2)
            return default_users
        
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"⚠️ خطأ في تحميل المستخدمين: {e}")
        return {}


def save_users(users: Dict) -> bool:
    """حفظ بيانات المستخدمين"""
    try:
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        # مسح الـ cache لإعادة التحميل
        load_users.clear()
        return True
    except Exception as e:
        st.error(f"⚠️ فشل حفظ المستخدمين: {e}")
        return False


def authenticate(username: str, password: str) -> Optional[Dict]:
    """
    المصادقة على المستخدم
    
    Returns:
        بيانات المستخدم إذا نجحت المصادقة، None إذا فشلت
    """
    users = load_users()
    
    if username not in users:
        return None
    
    user = users[username]
    if verify_password(password, user['password']):
        return {
            'username': username,
            'role': user['role'],
            'name': user.get('name', username)
        }
    
    return None


def add_user(username: str, password: str, role: str, name: str) -> bool:
    """إضافة مستخدم جديد"""
    users = load_users()
    
    if username in users:
        st.error("⚠️ اسم المستخدم موجود مسبقاً")
        return False
    
    users[username] = {
        'password': hash_password(password),
        'role': role,
        'name': name
    }
    
    return save_users(users)


def update_user(username: str, **kwargs) -> bool:
    """تحديث بيانات مستخدم"""
    users = load_users()
    
    if username not in users:
        st.error("⚠️ المستخدم غير موجود")
        return False
    
    # تحديث الحقول المطلوبة
    if 'password' in kwargs:
        users[username]['password'] = hash_password(kwargs['password'])
    if 'role' in kwargs:
        users[username]['role'] = kwargs['role']
    if 'name' in kwargs:
        users[username]['name'] = kwargs['name']
    
    return save_users(users)


def delete_user(username: str) -> bool:
    """حذف مستخدم"""
    users = load_users()
    
    if username not in users:
        st.error("⚠️ المستخدم غير موجود")
        return False
    
    if username == 'admin':
        st.error("⚠️ لا يمكن حذف حساب المدير الرئيسي")
        return False
    
    del users[username]
    return save_users(users)

