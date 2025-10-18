#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة إدارة البيانات المالية (الإيرادات والمصاريف)
Argan Smart Generator - Revenues Module
"""

import sqlite3
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional, Tuple


DB_PATH = 'database/revenues.db'


@st.cache_data(ttl=300)
def get_all_months() -> List[Dict]:
    """الحصول على قائمة جميع الأشهر"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, month_name, month_number, year, last_update
    FROM months
    ORDER BY year DESC, month_number DESC
    ''')
    
    months = []
    for row in cursor.fetchall():
        months.append({
            'id': row[0],
            'month_name': row[1],
            'month_number': row[2],
            'year': row[3],
            'last_update': row[4]
        })
    
    conn.close()
    return months


@st.cache_data(ttl=300)
def get_month_expenses(month_id: int) -> List[Dict]:
    """الحصول على مصاريف شهر معين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, expense_type, value
    FROM expenses
    WHERE month_id = ?
    ORDER BY value DESC
    ''', (month_id,))
    
    expenses = []
    for row in cursor.fetchall():
        expenses.append({
            'id': row[0],
            'type': row[1],
            'value': row[2]
        })
    
    conn.close()
    return expenses


@st.cache_data(ttl=300)
def get_month_revenues(month_id: int) -> List[Dict]:
    """الحصول على إيرادات شهر معين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, revenue_type, value, roi, orders
    FROM revenues
    WHERE month_id = ?
    ORDER BY value DESC
    ''', (month_id,))
    
    revenues = []
    for row in cursor.fetchall():
        revenues.append({
            'id': row[0],
            'type': row[1],
            'value': row[2],
            'roi': row[3],
            'orders': row[4]
        })
    
    conn.close()
    return revenues


@st.cache_data(ttl=300)
def get_month_summary(month_id: int) -> Dict:
    """الحصول على ملخص شهر معين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # معلومات الشهر
    cursor.execute('SELECT month_name, last_update FROM months WHERE id = ?', (month_id,))
    month_info = cursor.fetchone()
    
    # إجمالي المصاريف
    cursor.execute('SELECT SUM(value) FROM expenses WHERE month_id = ?', (month_id,))
    total_expenses = cursor.fetchone()[0] or 0
    
    # إجمالي الإيرادات
    cursor.execute('SELECT SUM(value) FROM revenues WHERE month_id = ?', (month_id,))
    total_revenues = cursor.fetchone()[0] or 0
    
    # عدد الطلبات
    cursor.execute('SELECT SUM(orders) FROM revenues WHERE month_id = ?', (month_id,))
    total_orders = cursor.fetchone()[0] or 0
    
    conn.close()
    
    net_profit = total_revenues - total_expenses
    profit_margin = (net_profit / total_revenues * 100) if total_revenues > 0 else 0
    
    return {
        'month_name': month_info[0],
        'last_update': month_info[1],
        'total_expenses': total_expenses,
        'total_revenues': total_revenues,
        'net_profit': net_profit,
        'profit_margin': profit_margin,
        'total_orders': int(total_orders)
    }


@st.cache_data(ttl=300)
def get_total_summary() -> Dict:
    """الحصول على الملخص الإجمالي لجميع الأشهر"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # عدد الأشهر
    cursor.execute('SELECT COUNT(*) FROM months')
    months_count = cursor.fetchone()[0]
    
    # إجمالي المصاريف
    cursor.execute('SELECT SUM(value) FROM expenses')
    total_expenses = cursor.fetchone()[0] or 0
    
    # إجمالي الإيرادات
    cursor.execute('SELECT SUM(value) FROM revenues')
    total_revenues = cursor.fetchone()[0] or 0
    
    # إجمالي الطلبات
    cursor.execute('SELECT SUM(orders) FROM revenues')
    total_orders = cursor.fetchone()[0] or 0
    
    conn.close()
    
    net_profit = total_revenues - total_expenses
    profit_margin = (net_profit / total_revenues * 100) if total_revenues > 0 else 0
    avg_revenue_per_month = total_revenues / months_count if months_count > 0 else 0
    
    return {
        'months_count': months_count,
        'total_expenses': total_expenses,
        'total_revenues': total_revenues,
        'net_profit': net_profit,
        'profit_margin': profit_margin,
        'total_orders': int(total_orders),
        'avg_revenue_per_month': avg_revenue_per_month
    }


@st.cache_data(ttl=300)
def get_expenses_by_type() -> List[Dict]:
    """الحصول على المصاريف مجمعة حسب النوع"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT expense_type, SUM(value) as total
    FROM expenses
    GROUP BY expense_type
    ORDER BY total DESC
    ''')
    
    expenses = []
    for row in cursor.fetchall():
        expenses.append({
            'type': row[0],
            'total': row[1]
        })
    
    conn.close()
    return expenses


@st.cache_data(ttl=300)
def get_revenues_by_type() -> List[Dict]:
    """الحصول على الإيرادات مجمعة حسب النوع"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT revenue_type, SUM(value) as total, SUM(orders) as total_orders
    FROM revenues
    GROUP BY revenue_type
    ORDER BY total DESC
    ''')
    
    revenues = []
    for row in cursor.fetchall():
        revenues.append({
            'type': row[0],
            'total': row[1],
            'orders': int(row[2])
        })
    
    conn.close()
    return revenues


@st.cache_data(ttl=300)
def get_monthly_trend() -> List[Dict]:
    """الحصول على اتجاه الإيرادات والمصاريف الشهري"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT 
        m.month_name,
        m.month_number,
        m.year,
        COALESCE(SUM(e.value), 0) as total_expenses,
        COALESCE(SUM(r.value), 0) as total_revenues
    FROM months m
    LEFT JOIN expenses e ON m.id = e.month_id
    LEFT JOIN revenues r ON m.id = r.month_id
    GROUP BY m.id, m.month_name, m.month_number, m.year
    ORDER BY m.year, m.month_number
    ''')
    
    trend = []
    for row in cursor.fetchall():
        revenues = row[4]
        expenses = row[3]
        profit = revenues - expenses
        
        trend.append({
            'month_name': row[0],
            'month_number': row[1],
            'year': row[2],
            'expenses': expenses,
            'revenues': revenues,
            'profit': profit
        })
    
    conn.close()
    return trend


@st.cache_data(ttl=300)
def get_roi_analysis() -> List[Dict]:
    """تحليل العائد على الاستثمار (ROI) لكل قناة"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT 
        revenue_type,
        AVG(roi) as avg_roi,
        SUM(value) as total_revenue,
        SUM(orders) as total_orders
    FROM revenues
    WHERE roi IS NOT NULL
    GROUP BY revenue_type
    ORDER BY avg_roi DESC
    ''')
    
    analysis = []
    for row in cursor.fetchall():
        analysis.append({
            'channel': row[0],
            'avg_roi': row[1],
            'total_revenue': row[2],
            'total_orders': int(row[3])
        })
    
    conn.close()
    return analysis


def add_month(month_name: str, month_number: int, year: int) -> int:
    """إضافة شهر جديد"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO months (month_name, month_number, year, last_update)
        VALUES (?, ?, ?, ?)
        ''', (month_name, month_number, year, datetime.now().strftime('%Y-%m-%d')))
        
        month_id = cursor.lastrowid
        conn.commit()
        
        # مسح الـ cache
        get_all_months.clear()
        get_total_summary.clear()
        
        return month_id
        
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def add_expense(month_id: int, expense_type: str, value: float) -> bool:
    """إضافة مصروف"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO expenses (month_id, expense_type, value)
        VALUES (?, ?, ?)
        ''', (month_id, expense_type, value))
        
        conn.commit()
        
        # مسح الـ cache
        get_month_expenses.clear()
        get_month_summary.clear()
        get_total_summary.clear()
        get_expenses_by_type.clear()
        get_monthly_trend.clear()
        
        return True
        
    except Exception as e:
        print(f"خطأ في إضافة المصروف: {e}")
        return False
    finally:
        conn.close()


def add_revenue(month_id: int, revenue_type: str, value: float, 
                roi: Optional[float] = None, orders: int = 0) -> bool:
    """إضافة إيراد"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO revenues (month_id, revenue_type, value, roi, orders)
        VALUES (?, ?, ?, ?, ?)
        ''', (month_id, revenue_type, value, roi, orders))
        
        conn.commit()
        
        # مسح الـ cache
        get_month_revenues.clear()
        get_month_summary.clear()
        get_total_summary.clear()
        get_revenues_by_type.clear()
        get_monthly_trend.clear()
        get_roi_analysis.clear()
        
        return True
        
    except Exception as e:
        print(f"خطأ في إضافة الإيراد: {e}")
        return False
    finally:
        conn.close()


def update_expense(expense_id: int, value: float) -> bool:
    """تحديث قيمة مصروف"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        UPDATE expenses
        SET value = ?
        WHERE id = ?
        ''', (value, expense_id))
        
        conn.commit()
        
        # مسح الـ cache
        get_month_expenses.clear()
        get_month_summary.clear()
        get_total_summary.clear()
        get_expenses_by_type.clear()
        get_monthly_trend.clear()
        
        return True
        
    except Exception as e:
        print(f"خطأ في تحديث المصروف: {e}")
        return False
    finally:
        conn.close()


def update_revenue(revenue_id: int, value: float, roi: Optional[float] = None, 
                   orders: Optional[int] = None) -> bool:
    """تحديث إيراد"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        if roi is not None and orders is not None:
            cursor.execute('''
            UPDATE revenues
            SET value = ?, roi = ?, orders = ?
            WHERE id = ?
            ''', (value, roi, orders, revenue_id))
        else:
            cursor.execute('''
            UPDATE revenues
            SET value = ?
            WHERE id = ?
            ''', (value, revenue_id))
        
        conn.commit()
        
        # مسح الـ cache
        get_month_revenues.clear()
        get_month_summary.clear()
        get_total_summary.clear()
        get_revenues_by_type.clear()
        get_monthly_trend.clear()
        get_roi_analysis.clear()
        
        return True
        
    except Exception as e:
        print(f"خطأ في تحديث الإيراد: {e}")
        return False
    finally:
        conn.close()


def delete_expense(expense_id: int) -> bool:
    """حذف مصروف"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        
        # مسح الـ cache
        get_month_expenses.clear()
        get_month_summary.clear()
        get_total_summary.clear()
        get_expenses_by_type.clear()
        get_monthly_trend.clear()
        
        return True
        
    except Exception as e:
        print(f"خطأ في حذف المصروف: {e}")
        return False
    finally:
        conn.close()


def delete_revenue(revenue_id: int) -> bool:
    """حذف إيراد"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM revenues WHERE id = ?', (revenue_id,))
        conn.commit()
        
        # مسح الـ cache
        get_month_revenues.clear()
        get_month_summary.clear()
        get_total_summary.clear()
        get_revenues_by_type.clear()
        get_monthly_trend.clear()
        get_roi_analysis.clear()
        
        return True
        
    except Exception as e:
        print(f"خطأ في حذف الإيراد: {e}")
        return False
    finally:
        conn.close()


# دوال مساعدة للتنسيق
def format_currency(value: float) -> str:
    """تنسيق الأرقام كعملة"""
    return f"{value:,.0f} ر.س"


def format_percentage(value: float) -> str:
    """تنسيق النسبة المئوية"""
    return f"{value:.1f}%"


def format_roi(value: float) -> str:
    """تنسيق ROI"""
    return f"{value:.2f}x"

