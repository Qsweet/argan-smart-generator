#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تخطيط التسعير المحسّن - النسخة 2.0
Argan Smart Generator - Pricing Planning System

التحسينات:
- تحميل تلقائي للأسعار من products_pricing.json
- نسبة خصم منفصلة لكل منتج
- إمكانية تعديل كامل للبيانات
- تصميم احترافي وجذاب
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd


def load_products_pricing():
    """تحميل بيانات التسعير من ملف JSON"""
    try:
        if os.path.exists("products_pricing.json"):
            with open("products_pricing.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"خطأ في تحميل بيانات التسعير: {str(e)}")
        return {}


def load_pricing_plans():
    """تحميل خطط التسعير المحفوظة"""
    try:
        if os.path.exists("pricing_plans.json"):
            with open("pricing_plans.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"خطأ في تحميل الخطط: {str(e)}")
        return []


def save_pricing_plans(plans):
    """حفظ خطط التسعير"""
    try:
        with open("pricing_plans.json", "w", encoding="utf-8") as f:
            json.dump(plans, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الخطط: {str(e)}")
        return False


def calculate_product_metrics(product_data, cost):
    """حساب جميع مقاييس المنتج"""
    base_price = product_data['base_price']
    after_discount = product_data['after_discount']
    after_code = product_data['after_code']
    
    # حساب الأرباح
    net_profit = after_code - cost
    profit_margin = (net_profit / after_code) * 100 if after_code > 0 else 0
    
    # حساب نسبة الخصم الإجمالية
    total_discount_percent = ((base_price - after_code) / base_price) * 100 if base_price > 0 else 0
    
    # تحديد الحالة
    if profit_margin >= 30:
        status = "ممتاز"
        status_color = "🟢"
    elif profit_margin >= 15:
        status = "جيد"
        status_color = "🟠"
    else:
        status = "تحذير"
        status_color = "🔴"
    
    return {
        'net_profit': net_profit,
        'profit_margin': profit_margin,
        'total_discount_percent': total_discount_percent,
        'status': status,
        'status_color': status_color
    }


def pricing_planning():
    """الدالة الرئيسية لنظام تخطيط التسعير"""
    
    # تطبيق CSS مخصص للتصميم الاحترافي
    st.markdown("""
    <style>
        /* تحسين الخطوط والألوان */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* بطاقات المنتجات */
        .product-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 5px solid #4CAF50;
            transition: transform 0.2s;
        }
        
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* عناوين الأقسام */
        .section-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* مقاييس الأداء */
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        /* حالات الربح */
        .status-excellent {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .status-good {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .status-warning {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        /* جدول البيانات */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* أزرار مخصصة */
        .stButton>button {
            border-radius: 10px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
        }
        
        /* حقول الإدخال */
        .stNumberInput>div>div>input {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: border-color 0.3s;
        }
        
        .stNumberInput>div>div>input:focus {
            border-color: #667eea;
        }
        
        /* التبويبات */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # العنوان الرئيسي
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h1 style='color: white; margin: 0;'>💰 نظام تخطيط التسعير الذكي</h1>
        <p style='color: #f0f0f0; margin: 10px 0 0 0;'>خطط أسعارك واحسب أرباحك بدقة واحترافية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    products_pricing = load_products_pricing()
    pricing_plans = load_pricing_plans()
    
    if not products_pricing:
        st.error("⚠️ لم يتم العثور على ملف بيانات التسعير (products_pricing.json)")
        return
    
    # التبويبات
    tab1, tab2 = st.tabs(["📋 خطط التسعير المحفوظة", "➕ خطة تسعير جديدة"])
    
    with tab1:
        show_saved_plans(pricing_plans)
    
    with tab2:
        create_new_plan(products_pricing)


def show_saved_plans(plans):
    """عرض الخطط المحفوظة"""
    st.markdown('<div class="section-header">📋 خطط التسعير المحفوظة</div>', unsafe_allow_html=True)
    
    if not plans:
        st.info("📭 لا توجد خطط محفوظة بعد. قم بإنشاء خطة جديدة من التبويب الثاني!")
        return
    
    for idx, plan in enumerate(plans):
        with st.expander(f"📦 {plan['name']} - {plan['created_at']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**📝 الوصف:** {plan.get('description', 'لا يوجد')}")
                st.markdown(f"**📅 تاريخ الإنشاء:** {plan['created_at']}")
                st.markdown(f"**📦 عدد المنتجات:** {len(plan['products'])}")
            
            with col2:
                if st.button("🗑️ حذف", key=f"delete_plan_{idx}", type="secondary"):
                    plans.pop(idx)
                    save_pricing_plans(plans)
                    st.success("✅ تم حذف الخطة!")
                    st.rerun()
            
            # عرض المنتجات
            if plan['products']:
                df = pd.DataFrame(plan['products'])
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # الإحصائيات
                total_revenue = df['after_code'].sum()
                total_cost = df['cost'].sum()
                total_profit = df['net_profit'].sum()
                avg_profit_margin = df['profit_margin'].mean()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("💰 الإيرادات المتوقعة", f"{total_revenue:.2f} ر.س")
                with col2:
                    st.metric("💵 إجمالي التكلفة", f"{total_cost:.2f} ر.س")
                with col3:
                    st.metric("📈 الربح المتوقع", f"{total_profit:.2f} ر.س")
                with col4:
                    st.metric("📊 متوسط نسبة الربح", f"{avg_profit_margin:.2f}%")


def create_new_plan(products_pricing):
    """إنشاء خطة تسعير جديدة"""
    st.markdown('<div class="section-header">➕ إنشاء خطة تسعير جديدة</div>', unsafe_allow_html=True)
    
    # معلومات الخطة
    with st.container():
        st.markdown("### 📝 معلومات الخطة")
        col1, col2 = st.columns(2)
        
        with col1:
            plan_name = st.text_input(
                "اسم الخطة:",
                placeholder="مثال: خطة العروض الشهرية",
                help="أدخل اسماً مميزاً للخطة"
            )
        
        with col2:
            plan_description = st.text_area(
                "وصف الخطة:",
                placeholder="وصف مختصر للخطة...",
                height=100
            )
    
    st.markdown("---")
    
    # إضافة المنتجات
    st.markdown("### 🛍️ إضافة المنتجات")
    
    # تهيئة session_state
    if 'pricing_products' not in st.session_state:
        st.session_state.pricing_products = []
    
    # نموذج إضافة منتج
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            selected_product = st.selectbox(
                "اختر المنتج:",
                options=[""] + list(products_pricing.keys()),
                key="new_product_select",
                help="اختر المنتج من القائمة"
            )
        
        # عرض البيانات التلقائية عند اختيار المنتج
        if selected_product and selected_product in products_pricing:
            product_data = products_pricing[selected_product]
            
            with col2:
                st.metric(
                    "السعر الأساسي",
                    f"{product_data['base_price']:.0f} ر.س",
                    help="السعر الأساسي للمنتج"
                )
            
            with col3:
                st.metric(
                    "بعد الكود",
                    f"{product_data['after_code']:.0f} ر.س",
                    delta=f"-{product_data['base_discount_percent'] + product_data['code_discount_percent']:.1f}%",
                    help="السعر النهائي بعد جميع الخصومات"
                )
            
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                add_product = st.button("➕ إضافة", type="primary", use_container_width=True)
            
            # إضافة المنتج
            if add_product:
                # طلب التكلفة
                cost_input = st.number_input(
                    "💵 أدخل تكلفة المنتج:",
                    min_value=0.0,
                    value=product_data['after_code'] * 0.5,  # تكلفة افتراضية 50%
                    step=1.0,
                    key="cost_input_temp"
                )
                
                if st.button("✅ تأكيد الإضافة", type="primary"):
                    metrics = calculate_product_metrics(product_data, cost_input)
                    
                    new_product = {
                        'name': selected_product,
                        'base_price': product_data['base_price'],
                        'after_discount': product_data['after_discount'],
                        'after_code': product_data['after_code'],
                        'cost': cost_input,
                        'base_discount_percent': product_data['base_discount_percent'],
                        'code_discount_percent': product_data['code_discount_percent'],
                        'total_discount_percent': metrics['total_discount_percent'],
                        'net_profit': metrics['net_profit'],
                        'profit_margin': metrics['profit_margin'],
                        'status': metrics['status']
                    }
                    
                    st.session_state.pricing_products.append(new_product)
                    st.success(f"✅ تمت إضافة {selected_product} بنجاح!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # عرض المنتجات المضافة
    if st.session_state.pricing_products:
        st.markdown("### 📦 المنتجات المضافة")
        
        # عرض كل منتج في بطاقة قابلة للتعديل
        for idx, product in enumerate(st.session_state.pricing_products):
            with st.expander(f"📦 {product['name']}", expanded=True):
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**المنتج:** {product['name']}")
                
                with col2:
                    new_cost = st.number_input(
                        "التكلفة:",
                        min_value=0.0,
                        value=float(product['cost']),
                        step=1.0,
                        key=f"edit_cost_{idx}"
                    )
                
                with col3:
                    st.markdown(f"**السعر الأساسي:**<br>{product['base_price']:.0f} ر.س", unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"**بعد الكود:**<br>{product['after_code']:.0f} ر.س", unsafe_allow_html=True)
                
                with col5:
                    if st.button("🔄", key=f"update_{idx}", help="تحديث الحسابات"):
                        # إعادة حساب المقاييس
                        product_data = {
                            'base_price': product['base_price'],
                            'after_discount': product['after_discount'],
                            'after_code': product['after_code']
                        }
                        metrics = calculate_product_metrics(product_data, new_cost)
                        
                        st.session_state.pricing_products[idx]['cost'] = new_cost
                        st.session_state.pricing_products[idx]['net_profit'] = metrics['net_profit']
                        st.session_state.pricing_products[idx]['profit_margin'] = metrics['profit_margin']
                        st.session_state.pricing_products[idx]['status'] = metrics['status']
                        
                        st.success("✅ تم التحديث!")
                        st.rerun()
                
                # عرض المقاييس
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("الربح الصافي", f"{product['net_profit']:.2f} ر.س")
                
                with col2:
                    profit_color = "green" if product['profit_margin'] >= 30 else "orange" if product['profit_margin'] >= 15 else "red"
                    st.metric("نسبة الربح", f"{product['profit_margin']:.2f}%")
                
                with col3:
                    st.metric("نسبة الخصم الكلية", f"{product['total_discount_percent']:.2f}%")
                
                with col4:
                    status_class = "excellent" if product['status'] == "ممتاز" else "good" if product['status'] == "جيد" else "warning"
                    st.markdown(f'<div class="status-{status_class}">{product["status"]}</div>', unsafe_allow_html=True)
                
                # زر الحذف
                if st.button("🗑️ حذف المنتج", key=f"delete_{idx}", type="secondary"):
                    st.session_state.pricing_products.pop(idx)
                    st.rerun()
        
        st.markdown("---")
        
        # جدول الملخص
        st.markdown("### 📊 جدول الملخص")
        df = pd.DataFrame(st.session_state.pricing_products)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # الإحصائيات الإجمالية
        st.markdown("### 📈 الإحصائيات الإجمالية")
        
        total_products = len(st.session_state.pricing_products)
        total_revenue = df['after_code'].sum()
        total_cost = df['cost'].sum()
        total_profit = df['net_profit'].sum()
        avg_profit_margin = df['profit_margin'].mean()
        avg_discount = df['total_discount_percent'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📦 إجمالي المنتجات", total_products)
            st.metric("💰 الإيرادات المتوقعة", f"{total_revenue:.2f} ر.س")
        
        with col2:
            st.metric("💵 إجمالي التكلفة", f"{total_cost:.2f} ر.س")
            st.metric("📈 الربح المتوقع", f"{total_profit:.2f} ر.س")
        
        with col3:
            st.metric("📊 متوسط نسبة الربح", f"{avg_profit_margin:.2f}%")
            st.metric("🎯 متوسط نسبة الخصم", f"{avg_discount:.2f}%")
        
        # حفظ الخطة
        st.markdown("---")
        
        if st.button("💾 حفظ الخطة", type="primary", use_container_width=True):
            if not plan_name:
                st.error("⚠️ يرجى إدخال اسم للخطة!")
            else:
                new_plan = {
                    'name': plan_name,
                    'description': plan_description,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'products': st.session_state.pricing_products
                }
                
                plans = load_pricing_plans()
                plans.append(new_plan)
                
                if save_pricing_plans(plans):
                    st.success("✅ تم حفظ الخطة بنجاح!")
                    st.session_state.pricing_products = []
                    st.rerun()

