# ============================================
# 🌿 Argan Package Smart CMS v8
# لوحة تحكم احترافية + إحصائيات تفاعلية + جدول رئيسي
# إعداد: د. محمد القضاه
# ============================================

import streamlit as st
import pandas as pd
import openai
import datetime
import json, csv
from pathlib import Path
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Argan Smart CMS", page_icon="🌿", layout="wide")

# ======================== CSS ========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700&display=swap');
html, body, [class*="css"]  {
  font-family: 'Tajawal', sans-serif;
  background-color: #F8F5F0;
}
h1,h2,h3,h4 { color: #1A1F1C; font-weight:700; }
.stButton>button {
  background-color:#1A1F1C;color:#fff;border-radius:8px;
  font-weight:600;padding:0.6rem 1.5rem;border:none;
}
.stButton>button:hover{background-color:#E6B05C;color:#1A1F1C;}
.card {
  background:rgba(255,255,255,0.95);
  border-radius:16px;
  padding:25px;
  box-shadow:0 4px 15px rgba(0,0,0,0.08);
  margin-bottom:20px;
}
.navbar {
  display:flex;justify-content:space-between;align-items:center;
  padding:0.8rem 1rem;background:#1A1F1C;color:white;border-radius:8px;
}
.navbar button{
  background:#E6B05C;color:#1A1F1C;border:none;
  border-radius:6px;padding:0.4rem 0.8rem;font-weight:600;margin-left:0.4rem;
}
.navbar button:hover{background:white;color:#1A1F1C;}
.metric-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.metric-value {font-size: 1.8rem; font-weight: 700; color: #1A1F1C;}
.metric-label {color: #E6B05C; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# ======================== Load Data ========================
with open("users.json","r",encoding="utf-8") as f: USERS=json.load(f)
with open("options.json","r",encoding="utf-8") as f: options=json.load(f)
openai.api_key=st.secrets["OPENAI_API_KEY"]
Path("scenarios_log.csv").touch(exist_ok=True)

# -------------------- دوال مساعدة --------------------
def get_role(u): return USERS.get(u,{}).get("role","user")

def log_scenario(u,p,s,plat):
    with open("scenarios_log.csv","a",encoding="utf-8",newline="") as f:
        csv.writer(f).writerow([u,p,s,plat,"جديد","جديد","","","",datetime.datetime.now()])

def get_df():
    try:
        df=pd.read_csv("scenarios_log.csv",names=["user","product","scenario","platform","status","required_action","delivery_date","video_link","extra","created_at"])
        return df
    except:
        return pd.DataFrame(columns=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])

# -------------------- تسجيل الدخول --------------------
def login():
    st.markdown("<h1 style='text-align:center'>🌿 Argan Smart CMS</h1>",unsafe_allow_html=True)
    u=st.text_input("👤 اسم المستخدم"); p=st.text_input("🔑 كلمة المرور",type="password")
    if st.button("دخول"):
        if u in USERS and USERS[u]["password"]==p:
            st.session_state.user=u; st.session_state.page="home"; st.rerun()
        else: st.error("❌ بيانات خاطئة")

# -------------------- الصفحة الرئيسية --------------------
def home():
    st.markdown("<div class='card' style='text-align:center;'>",unsafe_allow_html=True)
    st.markdown("<h2>أهلاً بكم في نظام إدارة المحتوى الذكي لشركة أرجان باكيج</h2>",unsafe_allow_html=True)
    st.markdown("<p>إعداد: د. محمد القضاه</p>",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    if st.button("🚀 بدء إنتاج السيناريوهات",use_container_width=True):
        st.session_state.page="generator"; st.rerun()

# -------------------- صفحة توليد السيناريوهات --------------------
generator
# -------------------- حساب المستخدم --------------------
def account():
    df=get_df(); df=df[df["user"]==st.session_state.user]
    st.markdown("<h2>👤 حسابي</h2>",unsafe_allow_html=True)
    if df.empty: st.info("لا يوجد سيناريوهات بعد."); return
    st.dataframe(df,use_container_width=True)

# -------------------- لوحة تحكم الأدمن --------------------
def admin():
    st.markdown("<h2>👑 لوحة التحكم الإدارية</h2>",unsafe_allow_html=True)
    df=get_df()
    if df.empty:
        st.warning("لا توجد بيانات بعد.")
        return

    # ======= إحصائيات عامة =======
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("<div class='metric-box'><div class='metric-value'>{}</div><div class='metric-label'>إجمالي المستخدمين</div></div>".format(len(df["user"].unique())), unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-box'><div class='metric-value'>{}</div><div class='metric-label'>عدد السيناريوهات</div></div>".format(len(df)), unsafe_allow_html=True)
    with c3:
        latest = df["created_at"].max() if not df.empty else "-"
        st.markdown("<div class='metric-box'><div class='metric-value'>{}</div><div class='metric-label'>آخر تحديث</div></div>".format(latest), unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # ======= الرسوم البيانية =======
    col1,col2 = st.columns(2)
    with col1:
        f=df.groupby("user").size().reset_index(name="count")
        st.plotly_chart(px.bar(f,x="user",y="count",color="user",title="👤 أكثر المستخدمين نشاطًا"),use_container_width=True)
    with col2:
        f2=df.groupby("platform").size().reset_index(name="count")
        st.plotly_chart(px.pie(f2,names="platform",values="count",title="📱 توزيع المنصات"),use_container_width=True)

    st.plotly_chart(px.bar(df.groupby("product").size().reset_index(name="count"),
                           x="product",y="count",color="product",
                           title="🧴 أكثر المنتجات توليدًا للسكربتات"),
                    use_container_width=True)

    st.markdown("---")
    st.markdown("<h3>📋 الجدول الرئيسي</h3>",unsafe_allow_html=True)
    st.dataframe(df,use_container_width=True)

# -------------------- Navbar --------------------
if "user" not in st.session_state: login(); st.stop()

st.markdown("<div class='navbar'>"
            f"<div>🌿 {st.session_state.user}</div>"
            "<div>", unsafe_allow_html=True)
cols=st.columns(3)
with cols[0]:
    if st.button("🏠 الرئيسية"): st.session_state.page="home"; st.rerun()
with cols[1]:
    if st.button("👤 حسابي"): st.session_state.page="account"; st.rerun()
with cols[2]:
    if get_role(st.session_state.user)=="admin":
        if st.button("📊 لوحة التحكم"): st.session_state.page="admin"; st.rerun()
    if st.button("🚪 خروج"):
        st.session_state.clear(); st.rerun()
st.markdown("</div>",unsafe_allow_html=True)

# -------------------- التوجيه --------------------
page=st.session_state.get("page","home")
if page=="home": home()
elif page=="generator": generator()
elif page=="account": account()
elif page=="admin": admin()

