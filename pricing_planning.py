#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تخطيط التسعير - النسخة النهائية
Argan Smart Generator
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd


def load_products_pricing():
    """تحميل بيانات التسعير"""
    try:
        if os.path.exists("products_pricing.json"):
            with open("products_pricing.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except:
        return {}


def load_pricing_plans():
    """تحميل الخطط المحفوظة"""
    try:
        if os.path.exists("pricing_plans.json"):
            with open("pricing_plans.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []


def save_pricing_plans(plans):
    """حفظ الخطط"""
    try:
        with open("pricing_plans.json", "w", encoding="utf-8") as f:
            json.dump(plans, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False


def pricing_planning():
    """الدالة الرئيسية"""
    
    # CSS بسيط وأنيق
    st.markdown("""
    <style>
        .main {
            direction: rtl;
        }
        .stButton>button {
            width: 100%;
        }
        div[data-testid="stMetricValue"] {
            font-size: 24px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("💰 نظام تخطيط التسعير")
    
    # تحميل البيانات
    products_pricing = load_products_pricing()
    pricing_plans = load_pricing_plans()
    
    if not products_pricing:
        st.error("⚠️ لم يتم العثور على ملف products_pricing.json")
        return
    
    # التبويبات
    tab1, tab2 = st.tabs(["📋 الخطط المحفوظة", "➕ خطة جديدة"])
    
    with tab1:
        show_saved_plans(pricing_plans)
    
    with tab2:
        create_new_plan(products_pricing)


def show_saved_plans(plans):
    """عرض الخطط المحفوظة"""
    st.subheader("📋 الخطط المحفوظة")
    
    if not plans:
        st.info("لا توجد خطط محفوظة")
        return
    
    for idx, plan in enumerate(plans):
        with st.expander(f"{plan['name']} - {plan['created_at']}"):
            st.write(f"**الوصف:** {plan.get('description', '-')}")
            
            if plan['products']:
                df = pd.DataFrame(plan['products'])
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # إحصائيات
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("المنتجات", len(plan['products']))
                col2.metric("الإيرادات", f"{df['after_code'].sum():.0f} ر.س")
                col3.metric("التكلفة", f"{df['cost'].sum():.0f} ر.س")
                col4.metric("الربح", f"{df['net_profit'].sum():.0f} ر.س")
            
            if st.button("🗑️ حذف", key=f"del_{idx}"):
                plans.pop(idx)
                save_pricing_plans(plans)
                st.rerun()


def create_new_plan(products_pricing):
    """إنشاء خطة جديدة"""
    st.subheader("➕ خطة جديدة")
    
    # معلومات الخطة
    col1, col2 = st.columns(2)
    with col1:
        plan_name = st.text_input("اسم الخطة:", placeholder="مثال: خطة نوفمبر")
    with col2:
        plan_desc = st.text_input("الوصف:", placeholder="وصف مختصر")
    
    st.markdown("---")
    
    # تهيئة session_state
    if 'pricing_products' not in st.session_state:
        st.session_state.pricing_products = []
    
    # قسم إضافة المنتجات
    st.subheader("🛍️ إضافة المنتجات")
    
    col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1.5, 1])
    
    with col1:
        selected_product = st.selectbox(
            "اختر المنتج:",
            options=[""] + list(products_pricing.keys()),
            key="product_select"
        )
    
    if selected_product:
        product_data = products_pricing[selected_product]
        
        with col2:
            base_price = st.number_input(
                "السعر الأساسي:",
                value=float(product_data['base_price']),
                disabled=True,
                key="base_price_show"
            )
        
        with col3:
            cost = st.number_input(
                "التكلفة:",
                min_value=0.0,
                value=product_data['after_code'] * 0.5,
                step=1.0,
                key="cost_input"
            )
        
        with col4:
            # نسبة الخصم الإجمالية (قابلة للتعديل)
            default_discount = ((product_data['base_price'] - product_data['after_code']) / product_data['base_price']) * 100
            discount_percent = st.number_input(
                "نسبة الخصم %:",
                min_value=0.0,
                max_value=100.0,
                value=float(default_discount),
                step=0.1,
                key="discount_input"
            )
        
        with col5:
            st.write("")
            st.write("")
            if st.button("➕ إضافة", type="primary"):
                # حساب السعر بعد الخصم
                after_discount = base_price * (1 - discount_percent / 100)
                net_profit = after_discount - cost
                profit_margin = (net_profit / after_discount) * 100 if after_discount > 0 else 0
                
                # تحديد الحالة
                if profit_margin >= 30:
                    status = "ممتاز 🟢"
                elif profit_margin >= 15:
                    status = "جيد 🟠"
                else:
                    status = "تحذير 🔴"
                
                new_product = {
                    'المنتج': selected_product,
                    'السعر الأساسي': base_price,
                    'نسبة الخصم %': round(discount_percent, 2),
                    'السعر بعد الخصم': round(after_discount, 2),
                    'التكلفة': cost,
                    'الربح الصافي': round(net_profit, 2),
                    'نسبة الربح %': round(profit_margin, 2),
                    'الحالة': status,
                    # بيانات داخلية للحفظ
                    'name': selected_product,
                    'base_price': base_price,
                    'discount_percent': discount_percent,
                    'after_code': after_discount,
                    'cost': cost,
                    'net_profit': net_profit,
                    'profit_margin': profit_margin
                }
                
                st.session_state.pricing_products.append(new_product)
                st.success(f"✅ تمت إضافة {selected_product}")
                st.rerun()
    
    st.markdown("---")
    
    # عرض المنتجات المضافة
    if st.session_state.pricing_products:
        st.subheader("📦 المنتجات المضافة")
        
        # إنشاء DataFrame للعرض
        display_df = pd.DataFrame([
            {
                'المنتج': p['المنتج'],
                'السعر الأساسي': f"{p['السعر الأساسي']:.0f}",
                'نسبة الخصم %': f"{p['نسبة الخصم %']:.1f}",
                'السعر النهائي': f"{p['السعر بعد الخصم']:.0f}",
                'التكلفة': f"{p['التكلفة']:.0f}",
                'الربح الصافي': f"{p['الربح الصافي']:.0f}",
                'نسبة الربح %': f"{p['نسبة الربح %']:.1f}",
                'الحالة': p['الحالة']
            }
            for p in st.session_state.pricing_products
        ])
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # أزرار التعديل والحذف
        st.write("**تعديل المنتجات:**")
        cols = st.columns(len(st.session_state.pricing_products))
        
        for idx, col in enumerate(cols):
            with col:
                product = st.session_state.pricing_products[idx]
                st.write(f"**{product['المنتج'][:20]}...**" if len(product['المنتج']) > 20 else f"**{product['المنتج']}**")
                
                # تعديل التكلفة
                new_cost = st.number_input(
                    "تكلفة:",
                    min_value=0.0,
                    value=float(product['cost']),
                    step=1.0,
                    key=f"edit_cost_{idx}"
                )
                
                # تعديل نسبة الخصم
                new_discount = st.number_input(
                    "خصم %:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(product['discount_percent']),
                    step=0.1,
                    key=f"edit_discount_{idx}"
                )
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("🔄", key=f"update_{idx}", help="تحديث"):
                        # إعادة الحساب
                        after_discount = product['base_price'] * (1 - new_discount / 100)
                        net_profit = after_discount - new_cost
                        profit_margin = (net_profit / after_discount) * 100 if after_discount > 0 else 0
                        
                        if profit_margin >= 30:
                            status = "ممتاز 🟢"
                        elif profit_margin >= 15:
                            status = "جيد 🟠"
                        else:
                            status = "تحذير 🔴"
                        
                        st.session_state.pricing_products[idx].update({
                            'نسبة الخصم %': round(new_discount, 2),
                            'السعر بعد الخصم': round(after_discount, 2),
                            'التكلفة': new_cost,
                            'الربح الصافي': round(net_profit, 2),
                            'نسبة الربح %': round(profit_margin, 2),
                            'الحالة': status,
                            'discount_percent': new_discount,
                            'after_code': after_discount,
                            'cost': new_cost,
                            'net_profit': net_profit,
                            'profit_margin': profit_margin
                        })
                        st.rerun()
                
                with col_b:
                    if st.button("🗑️", key=f"delete_{idx}", help="حذف"):
                        st.session_state.pricing_products.pop(idx)
                        st.rerun()
        
        st.markdown("---")
        
        # الإحصائيات
        st.subheader("📊 الإحصائيات الإجمالية")
        
        total_products = len(st.session_state.pricing_products)
        total_revenue = sum(p['after_code'] for p in st.session_state.pricing_products)
        total_cost = sum(p['cost'] for p in st.session_state.pricing_products)
        total_profit = sum(p['net_profit'] for p in st.session_state.pricing_products)
        avg_profit_margin = sum(p['profit_margin'] for p in st.session_state.pricing_products) / total_products if total_products > 0 else 0
        avg_discount = sum(p['discount_percent'] for p in st.session_state.pricing_products) / total_products if total_products > 0 else 0
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        col1.metric("📦 المنتجات", total_products)
        col2.metric("💰 الإيرادات", f"{total_revenue:.0f} ر.س")
        col3.metric("💵 التكلفة", f"{total_cost:.0f} ر.س")
        col4.metric("📈 الربح", f"{total_profit:.0f} ر.س")
        col5.metric("📊 متوسط الربح", f"{avg_profit_margin:.1f}%")
        col6.metric("🎯 متوسط الخصم", f"{avg_discount:.1f}%")
        
        st.markdown("---")
        
        # حفظ الخطة
        if st.button("💾 حفظ الخطة", type="primary", use_container_width=True):
            if not plan_name:
                st.error("⚠️ يرجى إدخال اسم للخطة")
            else:
                new_plan = {
                    'name': plan_name,
                    'description': plan_desc,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'products': st.session_state.pricing_products
                }
                
                plans = load_pricing_plans()
                plans.append(new_plan)
                
                if save_pricing_plans(plans):
                    st.success("✅ تم حفظ الخطة بنجاح!")
                    st.session_state.pricing_products = []
                    st.rerun()
    else:
        st.info("👆 اختر منتجاً من الأعلى لإضافته")

