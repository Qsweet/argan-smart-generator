# ============================================
# 🌿 Argan Package Smart CMS v7
# تصميم احترافي | Responsive | Dashboard مرئي
# إعداد: د. محمد القضاه
# ============================================

import streamlit as st
import pandas as pd
import openai
import datetime
import json, csv
from pathlib import Path
from io import StringIO
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Argan Smart CMS", page_icon="🌿", layout="wide")

# ======================== CSS ========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700&family=Poppins:wght@400;600&display=swap');
html, body, [class*="css"]  {
  font-family: 'Tajawal', 'Poppins', sans-serif;
  background-color: #F8F5F0;
}
h1,h2,h3,h4 { color: #1A1F1C; font-weight:700; }
.stButton>button {
  background-color:#1A1F1C;color:#fff;border-radius:8px;
  font-weight:600;padding:0.6rem 1.5rem;border:none;
}
.stButton>button:hover{background-color:#E6B05C;color:#1A1F1C;}
.card {
  background:rgba(255,255,255,0.85);
  border-radius:16px;
  padding:25px;
  box-shadow:0 4px 15px rgba(0,0,0,0.08);
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
</style>
""", unsafe_allow_html=True)

# ======================== Load data ========================
with open("users.json","r",encoding="utf-8") as f: USERS=json.load(f)
with open("options.json","r",encoding="utf-8") as f: options=json.load(f)
openai.api_key=st.secrets["OPENAI_API_KEY"]
Path("scenarios_log.csv").touch(exist_ok=True)

def get_role(u): return USERS.get(u,{}).get("role","user")

def log_scenario(u,p,s,plat):
  with open("scenarios_log.csv","a",encoding="utf-8",newline="") as f:
    csv.writer(f).writerow([u,p,s,plat,"جديد","جديد","","","",datetime.datetime.now()])

def get_df():
  try:
    df=pd.read_csv("scenarios_log.csv",names=["user","product","scenario","platform","status","required_action","delivery_date","video_link","extra","created_at"])
    return df
  except: return pd.DataFrame(columns=["user","product","scenario","platform","status","required_action","delivery_date","video_link","created_at"])

# ======================== LOGIN ========================
def login():
  st.markdown("<h1 style='text-align:center'>🌿 Argan Smart CMS</h1>",unsafe_allow_html=True)
  u=st.text_input("👤 اسم المستخدم"); p=st.text_input("🔑 كلمة المرور",type="password")
  if st.button("دخول"):
    if u in USERS and USERS[u]["password"]==p:
      st.session_state.user=u; st.session_state.page="home"; st.rerun()
    else: st.error("❌ بيانات خاطئة")

# ======================== HOME ========================
def home():
  st.markdown("<div class='card' style='text-align:center;'>",unsafe_allow_html=True)
  st.markdown("<h2>أهلاً بكم في نظام إدارة المحتوى الذكي لشركة أرجان باكيج</h2>",unsafe_allow_html=True)
  st.markdown("<p>إعداد: د. محمد القضاه</p>",unsafe_allow_html=True)
  st.markdown("</div>",unsafe_allow_html=True)
  if st.button("🚀 بدء إنتاج السيناريوهات",use_container_width=True):
    st.session_state.page="generator"; st.rerun()

# ======================== GENERATOR ========================
def generator():
  st.markdown("<div class='card'><h2>🧠 إنتاج السيناريوهات التسويقية</h2>",unsafe_allow_html=True)
  c1,c2=st.columns(2)
  with c1:
    offer=st.selectbox("🎁 العرض:",options["offer"])
    product=st.selectbox("🧴 المنتج:",options["product"])
    platform=st.selectbox("📱 المنصة:",options["platform"])
    scenario=st.selectbox("🎬 السيناريو:",options["scenario"])
  with c2:
    shipping=st.selectbox("🚚 التوصيل:",options["shipping"])
    gift=st.selectbox("🎁 الهدية:",options["gift"])
    cashback=st.selectbox("💸 الكاش باك:",options["cashback"])
    tone=st.selectbox("🎤 نبرة النص:",options["tone"])
  inst=st.text_area("📝 تعليمات إضافية:")
  if st.button("✨ توليد النص"):
    with st.spinner("جارٍ توليد النص..."):
      prompt=f"اكتب سكربت باللهجة السعودية لمنتج {product} على منصة {platform} بأسلوب {tone}. السيناريو: {scenario}. العرض: {offer}, التوصيل: {shipping}, الهدية: {gift}, الكاش باك: {cashback}. تعليمات: {inst}"
      try:
        r=openai.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":"كاتب محتوى تسويقي سعودي محترف."},{"role":"user","content":prompt}])
        s=r.choices[0].message.content.strip()
        st.text_area("📜 النص الناتج:",s,height=220)
        log_scenario(st.session_state.user,product,scenario,platform)
        st.success("تم الحفظ في حسابك ✅")
      except Exception as e: st.error(e)
  st.markdown("</div>",unsafe_allow_html=True)

# ======================== ACCOUNT ========================
def account():
  df=get_df(); df=df[df["user"]==st.session_state.user]
  st.markdown("<h2>👤 حسابي</h2>",unsafe_allow_html=True)
  if df.empty: st.info("لا يوجد سيناريوهات بعد."); return
  st.dataframe(df,use_container_width=True)

# ======================== ADMIN ========================
def admin():
  st.markdown("<h2>👑 لوحة التحكم</h2>",unsafe_allow_html=True)
  df=get_df()
  if df.empty: st.warning("لا بيانات بعد"); return
  st.metric("عدد المستخدمين",len(df["user"].unique()))
  st.metric("إجمالي السيناريوهات",len(df))
  col1,col2=st.columns(2)
  with col1:
    f=df.groupby("user").size().reset_index(name="count")
    st.plotly_chart(px.bar(f,x="user",y="count",color="user",title="عدد السيناريوهات لكل مستخدم"))
  with col2:
    p=df.groupby("platform").size().reset_index(name="count")
    st.plotly_chart(px.pie(p,names="platform",values="count",title="توزيع المنصات"))

# ======================== NAVBAR ========================
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

# ======================== ROUTER ========================
page=st.session_state.get("page","home")
if page=="home": home()
elif page=="generator": generator()
elif page=="account": account()
elif page=="admin": admin()
