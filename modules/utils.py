#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة الأدوات المساعدة
Argan Smart Generator
"""

import streamlit as st
import json
import os
from datetime import datetime
from hijri_converter import Hijri, Gregorian
from typing import Any, Dict, List, Optional


@st.cache_data(ttl=300)
def load_json(path: str) -> Any:
    """
    تحميل ملف JSON مع معالجة أفضل للأخطاء (cached)
    
    Args:
        path: مسار الملف
    
    Returns:
        محتوى الملف (dict أو list)
    """
    try:
        if not os.path.exists(path):
            # إنشاء ملف فارغ إذا لم يكن موجوداً
            default_data = [] if 'logs' in path else {}
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


def save_json(path: str, data: Any) -> bool:
    """
    حفظ البيانات إلى ملف JSON مع معالجة الأخطاء
    
    Args:
        path: مسار الملف
        data: البيانات المراد حفظها
    
    Returns:
        True إذا نجح الحفظ، False إذا فشل
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # مسح الـ cache لإعادة التحميل
        load_json.clear()
        return True
    except Exception as e:
        st.error(f"⚠️ فشل حفظ البيانات: {e}")
        return False


def gregorian_to_hijri(date: datetime) -> str:
    """
    تحويل التاريخ الميلادي إلى هجري
    
    Args:
        date: التاريخ الميلادي
    
    Returns:
        التاريخ الهجري بصيغة نصية
    """
    try:
        hijri = Gregorian(date.year, date.month, date.day).to_hijri()
        return f"{hijri.day}/{hijri.month}/{hijri.year}"
    except:
        return "تاريخ غير صحيح"


def hijri_to_gregorian(day: int, month: int, year: int) -> Optional[datetime]:
    """
    تحويل التاريخ الهجري إلى ميلادي
    
    Args:
        day: اليوم
        month: الشهر
        year: السنة
    
    Returns:
        التاريخ الميلادي أو None إذا فشل التحويل
    """
    try:
        gregorian = Hijri(year, month, day).to_gregorian()
        return datetime(gregorian.year, gregorian.month, gregorian.day)
    except:
        return None


def calculate_days_remaining(end_date_str: str) -> int:
    """
    حساب الأيام المتبقية حتى تاريخ معين
    
    Args:
        end_date_str: التاريخ بصيغة YYYY-MM-DD
    
    Returns:
        عدد الأيام المتبقية
    """
    try:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = end_date - today
        return delta.days
    except:
        return 0


def calculate_days_until_start(start_date_str: str) -> int:
    """
    حساب الأيام حتى بداية تاريخ معين
    
    Args:
        start_date_str: التاريخ بصيغة YYYY-MM-DD
    
    Returns:
        عدد الأيام حتى البداية
    """
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = start_date - today
        return delta.days
    except:
        return 0


def format_currency(amount: float, currency: str = "ر.س") -> str:
    """
    تنسيق المبلغ المالي
    
    Args:
        amount: المبلغ
        currency: العملة
    
    Returns:
        المبلغ منسق
    """
    return f"{amount:,.2f} {currency}"


def format_number(number: float, decimals: int = 2) -> str:
    """
    تنسيق الأرقام
    
    Args:
        number: الرقم
        decimals: عدد الخانات العشرية
    
    Returns:
        الرقم منسق
    """
    return f"{number:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    تنسيق النسبة المئوية
    
    Args:
        value: القيمة
        decimals: عدد الخانات العشرية
    
    Returns:
        النسبة منسقة
    """
    return f"{value:.{decimals}f}%"


def get_status_color(status: str) -> str:
    """
    الحصول على لون الحالة
    
    Args:
        status: الحالة
    
    Returns:
        اسم اللون
    """
    status_colors = {
        'ممتاز': 'green',
        'جيد': 'orange',
        'تحذير': 'red',
        'نشط': 'green',
        'منتهي': 'gray',
        'قريباً': 'blue'
    }
    return status_colors.get(status, 'gray')


def get_status_emoji(status: str) -> str:
    """
    الحصول على رمز الحالة
    
    Args:
        status: الحالة
    
    Returns:
        الرمز التعبيري
    """
    status_emojis = {
        'ممتاز': '🟢',
        'جيد': '🟠',
        'تحذير': '🔴',
        'نشط': '✅',
        'منتهي': '⚫',
        'قريباً': '🔵'
    }
    return status_emojis.get(status, '⚪')


def validate_phone(phone: str) -> bool:
    """
    التحقق من صحة رقم الهاتف السعودي
    
    Args:
        phone: رقم الهاتف
    
    Returns:
        True إذا كان صحيحاً
    """
    # إزالة المسافات والرموز
    phone = phone.replace(' ', '').replace('-', '').replace('+', '')
    
    # التحقق من أنه يبدأ بـ 966 أو 05
    if phone.startswith('966'):
        return len(phone) == 12 and phone[3] == '5'
    elif phone.startswith('05'):
        return len(phone) == 10
    
    return False


def normalize_phone(phone: str) -> str:
    """
    تنسيق رقم الهاتف إلى الصيغة الدولية
    
    Args:
        phone: رقم الهاتف
    
    Returns:
        رقم الهاتف منسق
    """
    phone = phone.replace(' ', '').replace('-', '').replace('+', '')
    
    if phone.startswith('05'):
        return '966' + phone[1:]
    elif phone.startswith('5'):
        return '966' + phone
    
    return phone


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    اختصار النص الطويل
    
    Args:
        text: النص
        max_length: الطول الأقصى
    
    Returns:
        النص مختصر
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def get_current_timestamp() -> str:
    """الحصول على الطابع الزمني الحالي"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_date() -> str:
    """الحصول على التاريخ الحالي"""
    return datetime.now().strftime("%Y-%m-%d")


def parse_date(date_str: str) -> Optional[datetime]:
    """
    تحليل تاريخ من نص
    
    Args:
        date_str: التاريخ كنص
    
    Returns:
        كائن datetime أو None
    """
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    return None


def clear_all_cache():
    """مسح جميع الـ cache"""
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("✅ تم مسح الـ cache بنجاح!")

