#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة قاعدة البيانات - SQLite
Argan Smart Generator
"""

import sqlite3
import streamlit as st
from typing import List, Dict, Optional, Tuple
import pandas as pd


@st.cache_resource
def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات (cached)"""
    return sqlite3.connect('database/customers.db', check_same_thread=False)


def get_orders_count() -> int:
    """الحصول على عدد الطلبات الإجمالي"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM orders')
        return cursor.fetchone()[0]
    except Exception as e:
        st.error(f"خطأ في الحصول على عدد الطلبات: {e}")
        return 0


def get_customers_count() -> int:
    """الحصول على عدد العملاء الفريدين"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(DISTINCT customer_name) FROM orders')
        return cursor.fetchone()[0]
    except Exception as e:
        st.error(f"خطأ في الحصول على عدد العملاء: {e}")
        return 0


def get_total_revenue() -> float:
    """الحصول على إجمالي الإيرادات"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(total_amount) FROM orders')
        result = cursor.fetchone()[0]
        return result if result else 0.0
    except Exception as e:
        st.error(f"خطأ في الحصول على الإيرادات: {e}")
        return 0.0


@st.cache_data(ttl=300)
def get_orders_paginated(page: int = 1, per_page: int = 100) -> Tuple[List[Dict], int]:
    """
    الحصول على الطلبات مع pagination
    
    Args:
        page: رقم الصفحة (يبدأ من 1)
        per_page: عدد الطلبات في الصفحة
    
    Returns:
        (قائمة الطلبات, العدد الإجمالي)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # الحصول على العدد الإجمالي
        cursor.execute('SELECT COUNT(*) FROM orders')
        total = cursor.fetchone()[0]
        
        # الحصول على الطلبات
        offset = (page - 1) * per_page
        cursor.execute(f'''
            SELECT 
                order_number, customer_name, total_amount, city, 
                order_date, status, phone
            FROM orders
            ORDER BY id DESC
            LIMIT {per_page} OFFSET {offset}
        ''')
        
        columns = ['رقم الطلب', 'اسم العميل', 'المبلغ', 'المدينة', 'التاريخ', 'الحالة', 'الهاتف']
        orders = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return orders, total
    
    except Exception as e:
        st.error(f"خطأ في الحصول على الطلبات: {e}")
        return [], 0


@st.cache_data(ttl=300)
def search_orders(query: str, search_by: str = 'customer_name') -> List[Dict]:
    """
    البحث في الطلبات
    
    Args:
        query: نص البحث
        search_by: الحقل المراد البحث فيه (customer_name, phone, city, order_number)
    
    Returns:
        قائمة الطلبات المطابقة
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if search_by == 'order_number':
            cursor.execute(f'''
                SELECT 
                    order_number, customer_name, total_amount, city, 
                    order_date, status, phone
                FROM orders
                WHERE order_number = ?
                LIMIT 100
            ''', (query,))
        else:
            cursor.execute(f'''
                SELECT 
                    order_number, customer_name, total_amount, city, 
                    order_date, status, phone
                FROM orders
                WHERE {search_by} LIKE ?
                LIMIT 100
            ''', (f'%{query}%',))
        
        columns = ['رقم الطلب', 'اسم العميل', 'المبلغ', 'المدينة', 'التاريخ', 'الحالة', 'الهاتف']
        orders = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return orders
    
    except Exception as e:
        st.error(f"خطأ في البحث: {e}")
        return []


@st.cache_data(ttl=600)
def get_orders_by_city() -> pd.DataFrame:
    """الحصول على إحصائيات الطلبات حسب المدينة"""
    try:
        conn = get_db_connection()
        query = '''
            SELECT 
                city as المدينة,
                COUNT(*) as عدد_الطلبات,
                SUM(total_amount) as إجمالي_المبيعات,
                AVG(total_amount) as متوسط_قيمة_الطلب
            FROM orders
            WHERE city IS NOT NULL AND city != ''
            GROUP BY city
            ORDER BY عدد_الطلبات DESC
            LIMIT 20
        '''
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"خطأ في الحصول على إحصائيات المدن: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=600)
def get_orders_by_month() -> pd.DataFrame:
    """الحصول على إحصائيات الطلبات حسب الشهر"""
    try:
        conn = get_db_connection()
        query = '''
            SELECT 
                strftime('%Y-%m', order_date) as الشهر,
                COUNT(*) as عدد_الطلبات,
                SUM(total_amount) as إجمالي_المبيعات
            FROM orders
            WHERE order_date IS NOT NULL AND order_date != ''
            GROUP BY strftime('%Y-%m', order_date)
            ORDER BY الشهر DESC
            LIMIT 12
        '''
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"خطأ في الحصول على إحصائيات الأشهر: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=600)
def get_top_customers(limit: int = 10) -> pd.DataFrame:
    """الحصول على أفضل العملاء"""
    try:
        conn = get_db_connection()
        query = f'''
            SELECT 
                customer_name as اسم_العميل,
                COUNT(*) as عدد_الطلبات,
                SUM(total_amount) as إجمالي_المشتريات,
                city as المدينة
            FROM orders
            WHERE customer_name IS NOT NULL AND customer_name != ''
            GROUP BY customer_name
            ORDER BY إجمالي_المشتريات DESC
            LIMIT {limit}
        '''
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"خطأ في الحصول على أفضل العملاء: {e}")
        return pd.DataFrame()


def get_order_details(order_number: int) -> Optional[Dict]:
    """الحصول على تفاصيل طلب معين"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_number = ?', (order_number,))
        
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    except Exception as e:
        st.error(f"خطأ في الحصول على تفاصيل الطلب: {e}")
        return None


def clear_cache():
    """مسح الـ cache لجميع الدوال"""
    st.cache_data.clear()
    st.success("✅ تم مسح الـ cache بنجاح!")




def get_all_orders() -> List[Dict]:
    """الحصول على جميع الطلبات بصيغة قائمة من القواميس (متوافق مع JSON القديم)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # جلب جميع الطلبات
        cursor.execute('''
            SELECT 
                order_id,
                customer_name,
                phone,
                city,
                total_amount,
                order_status,
                payment_method,
                order_date
            FROM orders
            ORDER BY order_id DESC
        ''')
        
        rows = cursor.fetchall()
        
        # تحويل إلى قائمة من القواميس بنفس أسماء الحقول القديمة
        orders = []
        for row in rows:
            orders.append({
                'رقم الطلب': row[0],
                'اسم العميل': row[1],
                'رقم الهاتف': row[2],
                'المدينة': row[3],
                'المبلغ الاجمالي': row[4],
                'حالة الطلب': row[5],
                ' طريقة الدفع': row[6],  # مع المسافة كما في JSON القديم
                'تاريخ الطلب': row[7]
            })
        
        return orders
        
    except Exception as e:
        st.error(f"خطأ في الحصول على الطلبات: {e}")
        return []

