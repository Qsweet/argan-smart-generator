#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تخطيط التسعير - النسخة النهائية المحسّنة
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
        show_saved_plans(pricing_plans, products_pricing)
    
    with tab2:
        create_new_plan(products_pricing)


def show_saved_plans(plans, products_pricing):
    """عرض وتعديل الخطط المحفوظة"""
    st.subheader("📋 الخطط المحفوظة")
    
    if not plans:
        st.info("لا توجد خطط محفوظة")
        return
    
    for plan_idx, plan in enumerate(plans):
        with st.expander(f"{plan['name']} - {plan['created_at']}", expanded=False):
            st.write(f"**الوصف:** {plan.get('description', '-')}")
            
            if plan['products']:
                # عرض الجدول بدون الحقول الإنجليزية
                display_df = pd.DataFrame([
                    {
                        'المنتج': p.get('المنتج', p.get('name', '')),
                        'السعر الأساسي': f"{p.get('السعر الأساسي', p.get('base_price', 0)):.0f}",
                        'نوع الخصم': p.get('نوع الخصم', 'نسبة مئوية'),
                        'قيمة الخصم': f"{p.get('قيمة الخصم', 0):.0f}" if p.get('نوع الخصم') == 'قيمة ثابتة' else f"{p.get('قيمة الخصم', 0):.1f}%",
                        'السعر النهائي': f"{p.get('السعر بعد الخصم', p.get('after_code', 0)):.0f}",
                        'التكلفة': f"{p.get('التكلفة', p.get('cost', 0)):.0f}",
                        'الربح الصافي': f"{p.get('الربح الصافي', p.get('net_profit', 0)):.0f}",
                        'نسبة الربح %': f"{p.get('نسبة الربح %', p.get('profit_margin', 0)):.1f}",
                        'الحالة': p.get('الحالة', '')
                    }
                    for p in plan['products']
                ])
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # إحصائيات
                total_revenue = sum(p.get('السعر بعد الخصم', p.get('after_code', 0)) for p in plan['products'])
                total_cost = sum(p.get('التكلفة', p.get('cost', 0)) for p in plan['products'])
                total_profit = sum(p.get('الربح الصافي', p.get('net_profit', 0)) for p in plan['products'])
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("المنتجات", len(plan['products']))
                col2.metric("الإيرادات", f"{total_revenue:.0f} ر.س")
                col3.metric("التكلفة", f"{total_cost:.0f} ر.س")
                col4.metric("الربح", f"{total_profit:.0f} ر.س")
                
                # أزرار التعديل والحذف
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ تعديل الخطة", key=f"edit_plan_{plan_idx}", type="primary"):
                        st.session_state.editing_plan = plan_idx
                        st.session_state.pricing_products = plan['products'].copy()
                        st.session_state.edit_plan_name = plan['name']
                        st.session_state.edit_plan_desc = plan.get('description', '')
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ حذف الخطة", key=f"del_plan_{plan_idx}"):
                        plans.pop(plan_idx)
                        save_pricing_plans(plans)
                        st.success("✅ تم حذف الخطة")
                        st.rerun()


def create_new_plan(products_pricing):
    """إنشاء أو تعديل خطة"""
    
    # التحقق من وضع التعديل
    is_editing = 'editing_plan' in st.session_state
    
    if is_editing:
        st.subheader("✏️ تعديل الخطة")
    else:
        st.subheader("➕ خطة جديدة")
    
    # معلومات الخطة
    col1, col2 = st.columns(2)
    with col1:
        plan_name = st.text_input(
            "اسم الخطة:",
            value=st.session_state.get('edit_plan_name', ''),
            placeholder="مثال: خطة نوفمبر",
            key="plan_name_input"
        )
    with col2:
        plan_desc = st.text_input(
            "الوصف:",
            value=st.session_state.get('edit_plan_desc', ''),
            placeholder="وصف مختصر",
            key="plan_desc_input"
        )
    
    st.markdown("---")
    
    # تهيئة session_state
    if 'pricing_products' not in st.session_state:
        st.session_state.pricing_products = []
    
    # قسم إضافة المنتجات
    st.subheader("🛍️ إضافة المنتجات")
    
    col1, col2, col3, col4, col5, col6 = st.columns([3, 1.5, 1, 1.5, 1.5, 1])
    
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
            discount_type = st.selectbox(
                "نوع الخصم:",
                options=["نسبة مئوية", "قيمة ثابتة"],
                key="discount_type_select"
            )
        
        with col4:
            if discount_type == "نسبة مئوية":
                default_discount = ((product_data['base_price'] - product_data['after_code']) / product_data['base_price']) * 100
                discount_value = st.number_input(
                    "قيمة الخصم %:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(default_discount),
                    step=0.1,
                    key="discount_input"
                )
            else:
                default_discount_amount = product_data['base_price'] - product_data['after_code']
                discount_value = st.number_input(
                    "قيمة الخصم (ر.س):",
                    min_value=0.0,
                    max_value=float(base_price),
                    value=float(default_discount_amount),
                    step=1.0,
                    key="discount_amount_input"
                )
        
        with col5:
            cost = st.number_input(
                "التكلفة:",
                min_value=0.0,
                value=product_data['after_code'] * 0.5,
                step=1.0,
                key="cost_input"
            )
        
        with col6:
            st.write("")
            st.write("")
            if st.button("➕ إضافة", type="primary"):
                # حساب السعر بعد الخصم
                if discount_type == "نسبة مئوية":
                    after_discount = base_price * (1 - discount_value / 100)
                else:
                    after_discount = base_price - discount_value
                
                # تقريب لأقرب رقم صحيح
                after_discount = round(after_discount)
                
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
                    'السعر الأساسي': round(base_price),
                    'نوع الخصم': discount_type,
                    'قيمة الخصم': round(discount_value, 1) if discount_type == "نسبة مئوية" else round(discount_value),
                    'السعر بعد الخصم': after_discount,
                    'التكلفة': round(cost),
                    'الربح الصافي': round(net_profit),
                    'نسبة الربح %': round(profit_margin, 1),
                    'الحالة': status
                }
                
                st.session_state.pricing_products.append(new_product)
                st.success(f"✅ تمت إضافة {selected_product}")
                st.rerun()
    
    st.markdown("---")
    
    # عرض المنتجات المضافة
    if st.session_state.pricing_products:
        st.subheader("📦 المنتجات المضافة")
        
        # إنشاء DataFrame للعرض (بدون حقول إنجليزية)
        display_df = pd.DataFrame([
            {
                'المنتج': p['المنتج'],
                'السعر الأساسي': f"{p['السعر الأساسي']:.0f}",
                'نوع الخصم': p['نوع الخصم'],
                'قيمة الخصم': f"{p['قيمة الخصم']:.0f}" if p['نوع الخصم'] == 'قيمة ثابتة' else f"{p['قيمة الخصم']:.1f}%",
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
        
        num_products = len(st.session_state.pricing_products)
        cols_per_row = min(3, num_products)  # 3 منتجات كحد أقصى في الصف
        
        for i in range(0, num_products, cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                idx = i + j
                if idx >= num_products:
                    break
                    
                with col:
                    product = st.session_state.pricing_products[idx]
                    product_name = product['المنتج']
                    
                    st.write(f"**{product_name[:25]}...**" if len(product_name) > 25 else f"**{product_name}**")
                    
                    # نوع الخصم
                    new_discount_type = st.selectbox(
                        "نوع الخصم:",
                        options=["نسبة مئوية", "قيمة ثابتة"],
                        index=0 if product['نوع الخصم'] == "نسبة مئوية" else 1,
                        key=f"edit_discount_type_{idx}"
                    )
                    
                    # قيمة الخصم
                    if new_discount_type == "نسبة مئوية":
                        new_discount = st.number_input(
                            "خصم %:",
                            min_value=0.0,
                            max_value=100.0,
                            value=float(product['قيمة الخصم']) if product['نوع الخصم'] == "نسبة مئوية" else 10.0,
                            step=0.1,
                            key=f"edit_discount_{idx}"
                        )
                    else:
                        new_discount = st.number_input(
                            "خصم (ر.س):",
                            min_value=0.0,
                            max_value=float(product['السعر الأساسي']),
                            value=float(product['قيمة الخصم']) if product['نوع الخصم'] == "قيمة ثابتة" else 10.0,
                            step=1.0,
                            key=f"edit_discount_amount_{idx}"
                        )
                    
                    # تعديل التكلفة
                    new_cost = st.number_input(
                        "تكلفة:",
                        min_value=0.0,
                        value=float(product['التكلفة']),
                        step=1.0,
                        key=f"edit_cost_{idx}"
                    )
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("🔄", key=f"update_{idx}", help="تحديث"):
                            # إعادة الحساب
                            if new_discount_type == "نسبة مئوية":
                                after_discount = product['السعر الأساسي'] * (1 - new_discount / 100)
                            else:
                                after_discount = product['السعر الأساسي'] - new_discount
                            
                            # تقريب لأقرب رقم صحيح
                            after_discount = round(after_discount)
                            
                            net_profit = after_discount - new_cost
                            profit_margin = (net_profit / after_discount) * 100 if after_discount > 0 else 0
                            
                            if profit_margin >= 30:
                                status = "ممتاز 🟢"
                            elif profit_margin >= 15:
                                status = "جيد 🟠"
                            else:
                                status = "تحذير 🔴"
                            
                            st.session_state.pricing_products[idx].update({
                                'نوع الخصم': new_discount_type,
                                'قيمة الخصم': round(new_discount, 1) if new_discount_type == "نسبة مئوية" else round(new_discount),
                                'السعر بعد الخصم': after_discount,
                                'التكلفة': round(new_cost),
                                'الربح الصافي': round(net_profit),
                                'نسبة الربح %': round(profit_margin, 1),
                                'الحالة': status
                            })
                            st.success("✅ تم التحديث!")
                            st.rerun()
                    
                    with col_b:
                        if st.button("🗑️", key=f"delete_{idx}", help="حذف"):
                            st.session_state.pricing_products.pop(idx)
                            st.rerun()
        
        st.markdown("---")
        
        # الإحصائيات
        st.subheader("📊 الإحصائيات الإجمالية")
        
        total_products = len(st.session_state.pricing_products)
        total_revenue = sum(p['السعر بعد الخصم'] for p in st.session_state.pricing_products)
        total_cost = sum(p['التكلفة'] for p in st.session_state.pricing_products)
        total_profit = sum(p['الربح الصافي'] for p in st.session_state.pricing_products)
        avg_profit_margin = sum(p['نسبة الربح %'] for p in st.session_state.pricing_products) / total_products if total_products > 0 else 0
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("📦 المنتجات", total_products)
        col2.metric("💰 الإيرادات", f"{total_revenue:.0f} ر.س")
        col3.metric("💵 التكلفة", f"{total_cost:.0f} ر.س")
        col4.metric("📈 الربح", f"{total_profit:.0f} ر.س")
        col5.metric("📊 متوسط الربح", f"{avg_profit_margin:.1f}%")
        
        st.markdown("---")
        
        # حفظ أو تحديث الخطة
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if is_editing:
                if st.button("💾 حفظ التعديلات", type="primary", use_container_width=True):
                    if not plan_name:
                        st.error("⚠️ يرجى إدخال اسم للخطة")
                    else:
                        plans = load_pricing_plans()
                        plans[st.session_state.editing_plan] = {
                            'name': plan_name,
                            'description': plan_desc,
                            'created_at': plans[st.session_state.editing_plan]['created_at'],
                            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'products': st.session_state.pricing_products
                        }
                        
                        if save_pricing_plans(plans):
                            st.success("✅ تم حفظ التعديلات بنجاح!")
                            # تنظيف session_state
                            del st.session_state.editing_plan
                            del st.session_state.edit_plan_name
                            del st.session_state.edit_plan_desc
                            st.session_state.pricing_products = []
                            st.rerun()
            else:
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
        
        with col2:
            if is_editing:
                if st.button("❌ إلغاء التعديل", use_container_width=True):
                    del st.session_state.editing_plan
                    del st.session_state.edit_plan_name
                    del st.session_state.edit_plan_desc
                    st.session_state.pricing_products = []
                    st.rerun()
    else:
        st.info("👆 اختر منتجاً من الأعلى لإضافته")

