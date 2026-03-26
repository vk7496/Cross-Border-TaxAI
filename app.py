import streamlit as st
import re

# --- تنظیمات صفحه ---
st.set_page_config(page_title="Multi-Lingual Tax AI", layout="wide")

# استایل‌دهی برای پشتیبانی از متون راست‌به‌چپ (RTL) در بخش عربی
st.markdown("""
    <style>
    .rtl-text { text-align: right; direction: rtl; font-family: 'Tahoma'; }
    .ltr-text { text-align: left; direction: ltr; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 AI Global Accountant (TR - OM - International)")
st.subheader("Support: English | Türkçe | العربية")

# --- توابع منطق محاسباتی (بدون خطا) ---
def validate_invoice(data, country_code):
    errors = []
    subtotal = data.get("subtotal", 0)
    tax_rate = data.get("tax_rate", 0)
    claimed_tax = data.get("tax_amount", 0)
    claimed_total = data.get("total", 0)

    # ۱. چک کردن قوانین خاص کشورها
    if country_code == "TR": # قوانین ترکیه
        valid_rates = [0, 1, 10, 20]
        if tax_rate not in valid_rates:
            errors.append(f"❌ Invalid KDV Rate: {tax_rate}% (Turkey uses 1, 10, 20)")
    
    elif country_code == "OM": # قوانین عمان
        if tax_rate not in [0, 5]:
            errors.append(f"❌ Invalid VAT Rate: {tax_rate}% (Oman standard is 5%)")

    # ۲. محاسبات ریاضی (قطعی)
    expected_tax = round(subtotal * (tax_rate / 100), 2)
    if abs(expected_tax - claimed_tax) > 0.05:
        errors.append(f"⚠️ Math Error: Tax should be {expected_tax}, but AI found {claimed_tax}")

    expected_total = round(subtotal + claimed_tax, 2)
    if abs(expected_total - claimed_total) > 0.05:
        errors.append(f"⚠️ Math Error: Total should be {expected_total}, but AI found {claimed_total}")

    return errors

# --- شبیه‌سازی استخراج داده توسط AI ---
# در پروژه واقعی، خروجی مدل هوش مصنوعی جایگزین این بخش می‌شود
mock_results = {
    "Turkey (Türkçe)": {
        "lang": "tr", "country": "TR",
        "data": {"vendor": "İstanbul Market", "tax_id": "1234567890", "subtotal": 1500.0, "tax_rate": 20, "tax_amount": 300.0, "total": 1800.0}
    },
    "Oman (العربية)": {
        "lang": "ar", "country": "OM",
        "data": {"vendor": "أسواق مسقط", "tax_id": "OM998877", "subtotal": 100.0, "tax_rate": 5, "tax_amount": 5.0, "total": 105.0}
    },
    "Global (English)": {
        "lang": "en", "country": "INT",
        "data": {"vendor": "Tech Solutions Ltd", "tax_id": "GB-5544", "subtotal": 2000.0, "tax_rate": 15, "tax_amount": 300.0, "total": 2300.0}
    }
}

# --- بخش تعاملی دمو ---
col_input, col_result = st.columns([1, 1])

with col_input:
    st.info("Step 1: AI Data Extraction")
    selected_demo = st.selectbox("Select a demo invoice language:", list(mock_results.keys()))
    
    current_lang = mock_results[selected_demo]["lang"]
    current_data = mock_results[selected_demo]["data"]
    
    # نمایش داده‌ها متناسب با زبان
    if current_lang == "ar":
        st.markdown(f'<div class="rtl-text"><b>المورد:</b> {current_data["vendor"]}</div>', unsafe_allow_html=True)
    elif current_lang == "tr":
        st.write(f"**Satıcı:** {current_data['vendor']}")
    else:
        st.write(f"**Vendor:** {current_data['vendor']}")
        
    st.json(current_data)

with col_result:
    st.success("Step 2: Logic Validation")
    country_code = mock_results[selected_demo]["country"]
    
    if st.button("Run Audit / تدقيق"):
        issues = validate_invoice(current_data, country_code)
        
        if not issues:
            st.write("✅ **Status:** Verified (All rules passed)")
            st.balloons()
        else:
            for error in issues:
                st.error(error)

# --- راهنمای ارائه ---
st.divider()
st.markdown("""
### 💡 چطور این سیستم خطای هوش مصنوعی را مدیریت می‌کند؟
1. **AI (مدل زبانی):** فاکتور را می‌بیند و با استفاده از قابلیت Multilingual، متن عربی یا ترکی را به داده عددی تبدیل می‌کند.
2. **Logic Engine (پایتون):** بدون توجه به زبان، اعداد را دوباره جمع و ضرب می‌کند و با نرخ‌های مالیاتی مصوب (مثل KDV ترکیه) تطبیق می‌دهد.
""")
