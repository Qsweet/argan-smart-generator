# ============================================
# 🌿 Argan Package Smart Script Generator v1 (محدّث لمكتبة openai>=1.0.0)
# الكاتب: د. محمد القضاه
# الوصف: تطبيق توليد سكربتات تسويقية باللهجة السعودية
# ملاحظة: تأكد من وضع OPENAI_API_KEY في Streamlit Secrets
# ============================================

import streamlit as st
from openai import OpenAI
import datetime

# إعداد الواجهة
st.set_page_config(
    page_title="Argan Package Script Generator",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 Argan Package Smart Script Generator")
st.markdown("##### ✨ نظام توليد سكربتات تسويقية باللهجة السعودية 🇸🇦")
st.markdown("---")

# جلب مفتاح OpenAI من Secrets (Streamlit Cloud)
try:
    OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_KEY = None

if not OPENAI_KEY:
    st.error("⚠️ لم يتم إعداد مفتاح OpenAI في إعدادات التطبيق (Settings → Secrets). أضف OPENAI_API_KEY ثم أعد تحميل الصفحة.")
    st.stop()

# تهيئة عميل OpenAI (الإصدار 1.0+)
client = OpenAI(api_key=OPENAI_KEY)

# واجهة الإدخال
col1, col2 = st.columns(2)
with col1:
    offer = st.text_input("🎁 العرض الخاص:")
    product = st.text_input("🧴 المنتج:")
    platform = st.selectbox("📱 المنصة:", ["Snapchat", "TikTok", "Meta"])
    scenario = st.selectbox("🎬 نوع السيناريو:", ["إعلان انطلاق", "تجربة المنتج", "توعية", "موشن"])

with col2:
    shipping = st.text_input("🚚 التوصيل:")
    gift = st.text_input("🎁 الهدية:")
    cashback = st.text_input("💸 الكاش باك (اختياري):")
    tone = st.selectbox("🎤 نبرة النص:", ["طبيعية", "فخمة", "عفوية", "أنثوية", "تحفيزية"])

custom_inst = st.text_area("📝 تعليمات إضافية:", placeholder="مثلاً: اجعل النص قصيرًا، باللهجة السعودية، وابدأ بجملة مشوقة...")

st.markdown("---")

# زر التنفيذ
if st.button("🧠 توليد السكربت الآن"):
    # التحقق من الحقول الإلزامية
    if not all([offer, product, platform, scenario, shipping, gift, custom_inst]):
        st.error("⚠️ الرجاء تعبئة جميع الحقول المطلوبة قبل التوليد.")
    else:
        with st.spinner("⚙️ جاري إنشاء السكربت..."):
            # بناء الـ prompt
            prompt = f"""
اكتب سكربت تسويقي باللهجة السعودية لمنتج "{product}" مناسب لمنصة {platform}.
نوع السيناريو: {scenario}.
نبرة النص: {tone}.

🎁 العرض: {offer}
🚚 التوصيل: {shipping}
🎁 الهدية: {gift}
💸 الكاش باك: {cashback if cashback else "لا يوجد"}
📝 تعليمات إضافية: {custom_inst}

✳️ المتطلبات:
- سكربت قصير لا يتجاوز 30 ثانية.
- يبدأ بجملة قوية تشد الانتباه.
- منطقي ومترابط.
- لهجة سعودية طبيعية وواثقة.
- ختام بدعوة للفعل مناسبة للمنصة ({platform}).
- اجعل السكربت مختلف عن أي سكربت عام أو نمطي.
"""
            try:
                # استدعاء واجهة Chat Completions بالطريقة الجديدة (openai>=1.0.0)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت كاتب محتوى تسويقي سعودي محترف متخصص في سناب شات وتيك توك ومتابع لسياسات المنصات."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.95,
                    max_tokens=700
                )

                # الحصول على النص من الاستجابة
                # في بعض إصدارات المكتبة صيغة الوصول قد تكون slightly different،
                # لكن عادة يمكن الوصول كما يلي:
                script = ""
                try:
                    # محاولة الوصول بالطريقة الكائنية
                    script = response.choices[0].message.content.strip()
                except Exception:
                    # fallback: محاولة شكل dict-like
                    script = response["choices"][0]["message"]["content"].strip()

                # عرض النتيجة
                st.success("✅ تم توليد السكربت بنجاح!")
                st.markdown(f"### 🧾 السكربت الناتج:")
                st.text_area("📜 النص النهائي:", script, height=300)

                # أزرار النسخ والتنزيل
                st.download_button("📥 تحميل النص كملف TXT", data=script, file_name=f"{product}_script.txt")

                # توقيع
                st.markdown("---")
                st.caption(f"تم إعداد هذا النظام بواسطة محمد القضاه • Argan Package • {datetime.datetime.now().strftime('%Y/%m/%d %H:%M')}")

            except Exception as e:
                # عرض الخطأ بطريقة ودّية مع نص الخطأ الفني للdebug
                st.error("❌ حدث خطأ أثناء الاتصال بـ OpenAI. تحقق من مفتاح OPENAI_API_KEY وإعداداتك.")
                st.exception(e)
