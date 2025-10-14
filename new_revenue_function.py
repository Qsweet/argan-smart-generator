# ============================================
# 💰 تتبع العائد الشهري - النسخة المحسّنة v5.5
# ============================================
def monthly_revenue_tracking():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>💰 تتبع العائد الشهري</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>إدارة ومتابعة المصاريف والمداخيل والعائد على الاستثمار</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    try:
        with open("revenue_data.json", "r", encoding="utf-8") as f:
            revenue_data = json.load(f)
    except FileNotFoundError:
        revenue_data = {}
    except json.JSONDecodeError:
        st.error("⚠️ ملف البيانات تالف")
        revenue_data = {}
    
    if not revenue_data:
        st.warning("⚠️ لا توجد بيانات بعد. ابدأ بإضافة شهر جديد.")
        revenue_data = {}
    
    # الحصول على قائمة الأشهر
    months = list(revenue_data.keys())
    
    # ============================================
    # 📊 عرض البيانات الحالية
    # ============================================
    if months:
        current_month = months[0]
        month_data = revenue_data[current_month]
        
        st.markdown(f"### 📅 الشهر الحالي: **{current_month}**")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"📅 **الشهر:** {current_month}")
        with col_info2:
            st.info(f"⏰ **آخر تحديث:** {month_data.get('last_update', 'غير محدد')}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # حساب الإحصائيات
        total_expenses = sum([e['value'] for e in month_data.get('expenses', [])])
        total_revenue = sum([r['value'] for r in month_data.get('revenues', [])])
        total_orders = sum([r.get('orders', 0) for r in month_data.get('revenues', [])])
        net_profit = total_revenue - total_expenses
        roi = (net_profit / total_expenses * 100) if total_expenses > 0 else 0
        
        # عرض الإحصائيات الرئيسية
        st.markdown("### 📊 الإحصائيات الرئيسية")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>📈 إجمالي المداخيل</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{total_revenue:,.0f}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>ر.س</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>📉 إجمالي المصاريف</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{total_expenses:,.0f}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>ر.س</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            profit_color = "#28a745" if net_profit > 0 else "#dc3545"
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>💰 صافي الربح</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{net_profit:,.0f}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>ROI: {roi:.1f}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>📦 عدد الطلبات</h3>
                    <h2 style='margin: 0.5rem 0 0 0; font-size: 1.8rem;'>{int(total_orders):,}</h2>
                    <p style='margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8;'>طلب</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # عرض تفصيلي للمصاريف والمداخيل
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 📉 المصاريف")
            if month_data.get('expenses'):
                for exp in month_data['expenses']:
                    st.markdown(f"""
                        <div style='background: #fff3cd; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #ffc107;'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='font-weight: 600; color: #856404;'>{exp['type']}</span>
                                <span style='font-size: 1.1rem; font-weight: 700; color: #856404;'>{exp['value']:,.0f} ر.س</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("لا توجد مصاريف")
        
        with col_right:
            st.markdown("### 📈 المداخيل")
            if month_data.get('revenues'):
                for rev in month_data['revenues']:
                    roi_val = rev.get('roi', 0)
                    roi_color = "#28a745" if roi_val >= 2.0 else "#17a2b8" if roi_val >= 1.0 else "#ffc107"
                    roi_bg = "#d4edda" if roi_val >= 2.0 else "#d1ecf1" if roi_val >= 1.0 else "#fff3cd"
                    
                    st.markdown(f"""
                        <div style='background: {roi_bg}; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {roi_color};'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <div style='font-weight: 600; color: #333;'>{rev['type']}</div>
                                    <div style='font-size: 0.85rem; color: #666; margin-top: 0.2rem;'>
                                        ROI: {roi_val:.2f} | الطلبات: {rev.get('orders', 0)}
                                    </div>
                                </div>
                                <span style='font-size: 1.1rem; font-weight: 700; color: {roi_color};'>{rev['value']:,.0f} ر.س</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("لا توجد مداخيل")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
    
    # ============================================
    # ➕ إضافة/تعديل بيانات الشهر
    # ============================================
    st.markdown("### ⚙️ إدارة البيانات")
    
    tab1, tab2, tab3 = st.tabs(["➕ إضافة شهر جديد", "✏️ تعديل شهر موجود", "📅 عرض الأشهر السابقة"])
    
    with tab1:
        st.markdown("#### ➕ إضافة شهر جديد")
        
        new_month_name = st.text_input("📅 اسم الشهر:", placeholder="مثال: شهر سبتمبر 2025", key="new_month")
        
        if new_month_name and new_month_name not in revenue_data:
            st.markdown("##### 📉 المصاريف")
            
            num_expenses = st.number_input("عدد بنود المصاريف:", min_value=1, max_value=20, value=3, key="num_exp")
            
            expenses = []
            for i in range(int(num_expenses)):
                col_exp1, col_exp2 = st.columns([2, 1])
                with col_exp1:
                    exp_type = st.text_input(f"نوع المصروف {i+1}:", key=f"exp_type_{i}")
                with col_exp2:
                    exp_value = st.number_input(f"القيمة (ر.س):", min_value=0.0, key=f"exp_val_{i}")
                
                if exp_type and exp_value > 0:
                    expenses.append({"type": exp_type, "value": exp_value})
            
            st.markdown("##### 📈 المداخيل")
            
            num_revenues = st.number_input("عدد بنود المداخيل:", min_value=1, max_value=20, value=3, key="num_rev")
            
            revenues = []
            for i in range(int(num_revenues)):
                col_rev1, col_rev2, col_rev3, col_rev4 = st.columns([2, 1, 1, 1])
                with col_rev1:
                    rev_type = st.text_input(f"نوع المدخول {i+1}:", key=f"rev_type_{i}")
                with col_rev2:
                    rev_value = st.number_input(f"القيمة (ر.س):", min_value=0.0, key=f"rev_val_{i}")
                with col_rev3:
                    rev_orders = st.number_input(f"الطلبات:", min_value=0, key=f"rev_ord_{i}")
                with col_rev4:
                    rev_roi = st.number_input(f"ROI:", min_value=0.0, key=f"rev_roi_{i}")
                
                if rev_type and rev_value > 0:
                    revenues.append({
                        "type": rev_type,
                        "value": rev_value,
                        "orders": int(rev_orders),
                        "roi": rev_roi
                    })
            
            if st.button("💾 حفظ الشهر الجديد", use_container_width=True, type="primary"):
                revenue_data[new_month_name] = {
                    "month_name": new_month_name,
                    "last_update": datetime.now().strftime("%Y-%m-%d"),
                    "expenses": expenses,
                    "revenues": revenues
                }
                
                # إعادة ترتيب الأشهر (الأحدث أولاً)
                revenue_data = {k: revenue_data[k] for k in sorted(revenue_data.keys(), reverse=True)}
                
                with open("revenue_data.json", "w", encoding="utf-8") as f:
                    json.dump(revenue_data, f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ تم إضافة الشهر: {new_month_name}")
                st.rerun()
        elif new_month_name in revenue_data:
            st.warning("⚠️ هذا الشهر موجود بالفعل. استخدم تبويب 'تعديل شهر موجود'")
    
    with tab2:
        st.markdown("#### ✏️ تعديل شهر موجود")
        
        if months:
            selected_month = st.selectbox("📅 اختر الشهر:", months, key="edit_month")
            
            if selected_month:
                month_data = revenue_data[selected_month]
                
                st.markdown("##### 📉 المصاريف الحالية")
                
                expenses_to_keep = []
                for i, exp in enumerate(month_data.get('expenses', [])):
                    col1, col2, col3 = st.columns([2, 1, 0.5])
                    with col1:
                        exp_type = st.text_input(f"نوع:", value=exp['type'], key=f"edit_exp_type_{i}")
                    with col2:
                        exp_value = st.number_input(f"القيمة:", value=float(exp['value']), key=f"edit_exp_val_{i}")
                    with col3:
                        if st.button("🗑️", key=f"del_exp_{i}"):
                            continue
                    
                    if exp_type and exp_value > 0:
                        expenses_to_keep.append({"type": exp_type, "value": exp_value})
                
                if st.button("➕ إضافة مصروف جديد", key="add_exp_btn"):
                    st.session_state.adding_expense = True
                
                if st.session_state.get('adding_expense'):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        new_exp_type = st.text_input("نوع المصروف:", key="new_exp_type")
                    with col2:
                        new_exp_value = st.number_input("القيمة:", min_value=0.0, key="new_exp_value")
                    
                    if new_exp_type and new_exp_value > 0:
                        expenses_to_keep.append({"type": new_exp_type, "value": new_exp_value})
                        st.session_state.adding_expense = False
                
                st.markdown("##### 📈 المداخيل الحالية")
                
                revenues_to_keep = []
                for i, rev in enumerate(month_data.get('revenues', [])):
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
                    with col1:
                        rev_type = st.text_input(f"نوع:", value=rev['type'], key=f"edit_rev_type_{i}")
                    with col2:
                        rev_value = st.number_input(f"القيمة:", value=float(rev['value']), key=f"edit_rev_val_{i}")
                    with col3:
                        rev_orders = st.number_input(f"الطلبات:", value=int(rev.get('orders', 0)), key=f"edit_rev_ord_{i}")
                    with col4:
                        rev_roi = st.number_input(f"ROI:", value=float(rev.get('roi', 0)), key=f"edit_rev_roi_{i}")
                    with col5:
                        if st.button("🗑️", key=f"del_rev_{i}"):
                            continue
                    
                    if rev_type and rev_value > 0:
                        revenues_to_keep.append({
                            "type": rev_type,
                            "value": rev_value,
                            "orders": rev_orders,
                            "roi": rev_roi
                        })
                
                if st.button("➕ إضافة مدخول جديد", key="add_rev_btn"):
                    st.session_state.adding_revenue = True
                
                if st.session_state.get('adding_revenue'):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        new_rev_type = st.text_input("نوع المدخول:", key="new_rev_type")
                    with col2:
                        new_rev_value = st.number_input("القيمة:", min_value=0.0, key="new_rev_value")
                    with col3:
                        new_rev_orders = st.number_input("الطلبات:", min_value=0, key="new_rev_orders")
                    with col4:
                        new_rev_roi = st.number_input("ROI:", min_value=0.0, key="new_rev_roi")
                    
                    if new_rev_type and new_rev_value > 0:
                        revenues_to_keep.append({
                            "type": new_rev_type,
                            "value": new_rev_value,
                            "orders": int(new_rev_orders),
                            "roi": new_rev_roi
                        })
                        st.session_state.adding_revenue = False
                
                col_save, col_delete = st.columns([3, 1])
                
                with col_save:
                    if st.button("💾 حفظ التعديلات", use_container_width=True, type="primary"):
                        revenue_data[selected_month] = {
                            "month_name": selected_month,
                            "last_update": datetime.now().strftime("%Y-%m-%d"),
                            "expenses": expenses_to_keep,
                            "revenues": revenues_to_keep
                        }
                        
                        with open("revenue_data.json", "w", encoding="utf-8") as f:
                            json.dump(revenue_data, f, ensure_ascii=False, indent=2)
                        
                        st.success(f"✅ تم تحديث الشهر: {selected_month}")
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️ حذف الشهر", use_container_width=True, type="secondary"):
                        del revenue_data[selected_month]
                        
                        with open("revenue_data.json", "w", encoding="utf-8") as f:
                            json.dump(revenue_data, f, ensure_ascii=False, indent=2)
                        
                        st.warning(f"⚠️ تم حذف الشهر: {selected_month}")
                        st.rerun()
        else:
            st.info("لا توجد أشهر لتعديلها")
    
    with tab3:
        st.markdown("#### 📅 عرض الأشهر السابقة")
        
        if len(months) > 1:
            previous_months = months[1:]
            selected_prev_month = st.selectbox("📅 اختر الشهر:", previous_months, key="prev_month")
            
            if selected_prev_month:
                prev_data = revenue_data[selected_prev_month]
                
                # حساب الإحصائيات
                prev_expenses = sum([e['value'] for e in prev_data.get('expenses', [])])
                prev_revenue = sum([r['value'] for r in prev_data.get('revenues', [])])
                prev_orders = sum([r.get('orders', 0) for r in prev_data.get('revenues', [])])
                prev_profit = prev_revenue - prev_expenses
                prev_roi = (prev_profit / prev_expenses * 100) if prev_expenses > 0 else 0
                
                st.markdown(f"### 📅 {selected_prev_month}")
                st.info(f"⏰ آخر تحديث: {prev_data.get('last_update', 'غير محدد')}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📈 المداخيل", f"{prev_revenue:,.0f} ر.س")
                with col2:
                    st.metric("📉 المصاريف", f"{prev_expenses:,.0f} ر.س")
                with col3:
                    st.metric("💰 الربح", f"{prev_profit:,.0f} ر.س", delta=f"{prev_roi:.1f}% ROI")
                with col4:
                    st.metric("📦 الطلبات", f"{int(prev_orders):,}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("**📉 المصاريف:**")
                    for exp in prev_data.get('expenses', []):
                        st.markdown(f"- **{exp['type']}:** {exp['value']:,.0f} ر.س")
                
                with col_right:
                    st.markdown("**📈 المداخيل:**")
                    for rev in prev_data.get('revenues', []):
                        st.markdown(f"- **{rev['type']}:** {rev['value']:,.0f} ر.س (ROI: {rev.get('roi', 0):.2f})")
        else:
            st.info("لا توجد أشهر سابقة")
