# دالة إنشاء حملات مراسلاتي
def create_moraselaty_campaign():
    load_custom_css()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>📱 إنشاء حملات مراسلاتي</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>تخطيط وإدارة حملات WhatsApp التسويقية</p>
        </div>
    """, unsafe_allow_html=True)
    
    # تحميل بيانات العملاء
    try:
        with open("moraselaty_customers.json", "r", encoding="utf-8") as f:
            customers_data = json.load(f)
        orders = customers_data.get("orders", [])
        last_updated = customers_data.get("last_updated", "غير معروف")
    except:
        st.error("❌ لم يتم العثور على بيانات العملاء!")
        return
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 إجمالي الطلبات", f"{len(orders):,}")
    with col2:
        unique_customers = len(set([o.get('رقم الهاتف', '') for o in orders if o.get('رقم الهاتف')]))
        st.metric("👥 عدد العملاء", f"{unique_customers:,}")
    with col3:
        cities_count = len(set([o.get('المدينة', '') for o in orders if o.get('المدينة')]))
        st.metric("🏙️ عدد المدن", f"{cities_count}")
    with col4:
        st.metric("📅 آخر تحديث", last_updated.split()[0])
    
    st.markdown("---")
    
    # تبويبات
    tab1, tab2, tab3 = st.tabs(["📤 رفع بيانات جديدة", "🎯 إنشاء حملة جديدة", "📋 الحملات السابقة"])
    
    with tab1:
        st.markdown("### 📤 رفع ملف بيانات العملاء")
        st.info("💡 يمكنك رفع ملف Excel يحتوي على بيانات الطلبات. سيتم دمجها مع البيانات الموجودة مع منع التكرار.")
        
        uploaded_file = st.file_uploader("اختر ملف Excel", type=['xlsx', 'xls'], key="moraselaty_upload")
        
        if uploaded_file:
            try:
                import pandas as pd
                df_new = pd.read_excel(uploaded_file)
                
                st.success(f"✅ تم قراءة {len(df_new)} طلب من الملف")
                
                # عرض عينة
                with st.expander("👁️ معاينة البيانات (أول 5 صفوف)"):
                    st.dataframe(df_new.head())
                
                if st.button("💾 حفظ ودمج البيانات", type="primary"):
                    # دمج مع البيانات الموجودة
                    df_existing = pd.DataFrame(orders)
                    df_all = pd.concat([df_existing, df_new], ignore_index=True)
                    
                    # إزالة التكرار
                    df_unique = df_all.drop_duplicates(subset=['رقم الطلب'], keep='first')
                    df_unique = df_unique.fillna("")
                    
                    # حفظ
                    customers_data_new = {
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "total_orders": len(df_unique),
                        "orders": df_unique.to_dict('records')
                    }
                    
                    with open("moraselaty_customers.json", "w", encoding="utf-8") as f:
                        json.dump(customers_data_new, f, ensure_ascii=False, indent=2)
                    
                    st.success(f"✅ تم الدمج بنجاح! الإجمالي الآن: {len(df_unique)} طلب")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
    
    with tab2:
        st.markdown("### 🎯 إنشاء حملة جديدة")
        
        # اسم الحملة
        campaign_name = st.text_input("📝 اسم الحملة:", placeholder="مثال: حملة عيد الفطر 2025")
        
        st.markdown("#### 🔍 تحديد العملاء المستهدفين")
        
        # الفلاتر
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown("##### 💰 قيمة الطلبات")
            price_filter_type = st.selectbox(
                "نوع الفلتر:",
                ["الكل", "أكثر من", "أقل من", "بين"],
                key="price_filter"
            )
            
            if price_filter_type == "أكثر من":
                min_price = st.number_input("القيمة (ر.س):", min_value=0.0, value=100.0, key="min_price")
            elif price_filter_type == "أقل من":
                max_price = st.number_input("القيمة (ر.س):", min_value=0.0, value=500.0, key="max_price")
            elif price_filter_type == "بين":
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    min_price = st.number_input("من (ر.س):", min_value=0.0, value=100.0, key="min_price_between")
                with col_p2:
                    max_price = st.number_input("إلى (ر.س):", min_value=0.0, value=500.0, key="max_price_between")
        
        with col_f2:
            st.markdown("##### 🏙️ المدينة")
            cities = sorted(set([o.get('المدينة', '') for o in orders if o.get('المدينة')]))
            city_filter = st.multiselect(
                "اختر المدن:",
                ["كامل السعودية"] + cities,
                default=["كامل السعودية"],
                key="city_filter"
            )
        
        col_f3, col_f4 = st.columns(2)
        
        with col_f3:
            st.markdown("##### 📦 حالة الطلب")
            statuses = sorted(set([o.get('حالة الطلب', '') for o in orders if o.get('حالة الطلب')]))
            status_filter = st.multiselect(
                "اختر الحالات:",
                ["الكل"] + statuses,
                default=["تم توصيل الطلب"],
                key="status_filter"
            )
        
        with col_f4:
            st.markdown("##### 💳 طريقة الدفع")
            payments = sorted(set([o.get(' طريقة الدفع', '') for o in orders if o.get(' طريقة الدفع')]))
            payment_filter = st.multiselect(
                "اختر طرق الدفع:",
                ["الكل"] + payments,
                default=["الكل"],
                key="payment_filter"
            )
        
        # تطبيق الفلاتر
        if st.button("🔍 تطبيق الفلاتر وعرض النتائج", type="primary", use_container_width=True):
            filtered_orders = orders.copy()
            
            # فلتر السعر
            if price_filter_type == "أكثر من":
                filtered_orders = [o for o in filtered_orders if float(o.get('المبلغ الاجمالي', 0) or 0) > min_price]
            elif price_filter_type == "أقل من":
                filtered_orders = [o for o in filtered_orders if float(o.get('المبلغ الاجمالي', 0) or 0) < max_price]
            elif price_filter_type == "بين":
                filtered_orders = [o for o in filtered_orders if min_price <= float(o.get('المبلغ الاجمالي', 0) or 0) <= max_price]
            
            # فلتر المدينة
            if "كامل السعودية" not in city_filter:
                filtered_orders = [o for o in filtered_orders if o.get('المدينة', '') in city_filter]
            
            # فلتر الحالة
            if "الكل" not in status_filter:
                filtered_orders = [o for o in filtered_orders if o.get('حالة الطلب', '') in status_filter]
            
            # فلتر طريقة الدفع
            if "الكل" not in payment_filter:
                filtered_orders = [o for o in filtered_orders if o.get(' طريقة الدفع', '') in payment_filter]
            
            # حفظ في session_state
            st.session_state.filtered_customers = filtered_orders
            
            st.success(f"✅ تم العثور على {len(filtered_orders)} عميل مطابق للفلاتر!")
        
        # عرض النتائج
        if hasattr(st.session_state, 'filtered_customers') and st.session_state.filtered_customers:
            filtered = st.session_state.filtered_customers
            
            st.markdown("---")
            st.markdown(f"### 📊 النتائج: {len(filtered)} عميل")
            
            # إحصائيات
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                total_value = sum([float(o.get('المبلغ الاجمالي', 0) or 0) for o in filtered])
                st.metric("💰 إجمالي القيمة", f"{total_value:,.0f} ر.س")
            with col_s2:
                unique_phones = len(set([o.get('رقم الهاتف', '') for o in filtered if o.get('رقم الهاتف')]))
                st.metric("📱 أرقام فريدة", f"{unique_phones:,}")
            with col_s3:
                avg_order = total_value / len(filtered) if filtered else 0
                st.metric("📊 متوسط الطلب", f"{avg_order:,.0f} ر.س")
            with col_s4:
                cities_in_result = len(set([o.get('المدينة', '') for o in filtered if o.get('المدينة')]))
                st.metric("🏙️ المدن", f"{cities_in_result}")
            
            # عرض الجدول
            with st.expander("👁️ عرض تفاصيل العملاء"):
                df_filtered = pd.DataFrame(filtered)
                st.dataframe(df_filtered[['اسم العميل', 'رقم الهاتف', 'المدينة', 'المبلغ الاجمالي', 'حالة الطلب', ' طريقة الدفع']])
            
            # حفظ الحملة
            st.markdown("---")
            campaign_message = st.text_area(
                "✍️ نص الرسالة:",
                placeholder="مثال: مرحباً {الاسم}، نقدم لك عرض خاص...",
                height=150
            )
            
            if st.button("💾 حفظ الحملة", type="primary", use_container_width=True):
                if not campaign_name:
                    st.error("❌ يرجى إدخال اسم الحملة!")
                elif not campaign_message:
                    st.error("❌ يرجى كتابة نص الرسالة!")
                else:
                    # تحميل الحملات الموجودة
                    try:
                        with open("moraselaty_campaigns.json", "r", encoding="utf-8") as f:
                            campaigns_data = json.load(f)
                    except:
                        campaigns_data = {"campaigns": []}
                    
                    # إنشاء الحملة
                    new_campaign = {
                        "id": len(campaigns_data["campaigns"]) + 1,
                        "name": campaign_name,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "created_by": st.session_state.username,
                        "message": campaign_message,
                        "filters": {
                            "price_type": price_filter_type,
                            "cities": city_filter,
                            "statuses": status_filter,
                            "payments": payment_filter
                        },
                        "total_customers": len(filtered),
                        "unique_phones": unique_phones,
                        "total_value": total_value,
                        "customers": filtered
                    }
                    
                    campaigns_data["campaigns"].append(new_campaign)
                    
                    with open("moraselaty_campaigns.json", "w", encoding="utf-8") as f:
                        json.dump(campaigns_data, f, ensure_ascii=False, indent=2)
                    
                    st.success(f"✅ تم حفظ الحملة: {campaign_name}")
                    st.balloons()
                    del st.session_state.filtered_customers
                    st.rerun()
    
    with tab3:
        st.markdown("### 📋 الحملات السابقة")
        
        try:
            with open("moraselaty_campaigns.json", "r", encoding="utf-8") as f:
                campaigns_data = json.load(f)
            campaigns = campaigns_data.get("campaigns", [])
        except:
            campaigns = []
        
        if not campaigns:
            st.info("📭 لا توجد حملات محفوظة بعد.")
        else:
            for campaign in reversed(campaigns):
                with st.expander(f"📱 {campaign['name']} - {campaign['created_at'].split()[0]}"):
                    col_c1, col_c2 = st.columns([2, 1])
                    
                    with col_c1:
                        st.markdown(f"**👤 المنشئ:** {campaign['created_by']}")
                        st.markdown(f"**📅 التاريخ:** {campaign['created_at']}")
                        st.markdown(f"**👥 العملاء:** {campaign['total_customers']:,}")
                        st.markdown(f"**📱 أرقام فريدة:** {campaign['unique_phones']:,}")
                        st.markdown(f"**💰 إجمالي القيمة:** {campaign['total_value']:,.0f} ر.س")
                    
                    with col_c2:
                        if st.button("📥 تصدير Excel", key=f"export_{campaign['id']}"):
                            df_export = pd.DataFrame(campaign['customers'])
                            st.download_button(
                                "⬇️ تحميل",
                                df_export.to_csv(index=False, encoding='utf-8-sig'),
                                f"campaign_{campaign['id']}.csv",
                                "text/csv"
                            )
                    
                    st.markdown("**✍️ نص الرسالة:**")
                    st.text_area("", campaign['message'], height=100, key=f"msg_{campaign['id']}", disabled=True)

