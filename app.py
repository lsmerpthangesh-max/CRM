import streamlit as st
import pandas as pd
import urllib.parse
import os

st.set_page_config(page_title="Lingam Super Market WhatsApp", layout="wide")

st.title("🛒 Lingam Super Market - WhatsApp Bulk Sender")
st.markdown("**Upload & Send Automation**")

# Template Download - Fixed Path
template_path = "/home/workdir/artifacts/lingam_customers_template.xlsx"

if os.path.exists(template_path):
    with open(template_path, "rb") as f:
        st.download_button(
            label="📥 Download Excel Template",
            data=f,
            file_name="lingam_customers_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("Template file not found. Please create one manually.")

uploaded_file = st.file_uploader("Upload your customers.xlsx file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ Successfully loaded **{len(df)}** customers!")
    
    st.subheader("Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    if st.button("🚀 Generate WhatsApp Links for All Customers", type="primary", use_container_width=True):
        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("❌ Missing required columns: 'Customer Name' and 'Phone Number'")
        else:
            st.subheader("✅ Generated WhatsApp Links (Click to Send)")

            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market! நன்றி உங்கள் ஆதரவுக்கு! Visit again soon.",
                "Promo": "Dear {name}, Month-end special offer at Lingam Super Market! Up to 20% OFF! இந்த மாத இறுதி சலுகை! Hurry!",
                "ReEngage": "Dear {name}, We miss you at Lingam Super Market! Special 10% discount waiting for you. மீண்டும் வருகை தரவும்!"
            }

            for idx, row in df.iterrows():
                name = str(row.get('Customer Name', 'Customer')).strip()
                phone_raw = str(row.get('Phone Number', '')).strip()
                phone = phone_raw.replace("+", "").replace(" ", "")
                campaign = str(row.get('Campaign Type', 'ThankYou')).strip()

                message = templates.get(campaign, templates["ThankYou"]).format(name=name)
                encoded_msg = urllib.parse.quote(message)
                
                wa_link = f"https://wa.me/{phone}?text={encoded_msg}"
                
                st.markdown(f"**{idx+1}. {name}** — [📱 Send Message]({wa_link})")

            st.success("✅ All links generated! Click each one to send.")
            st.info("💡 Open WhatsApp Web first. Click links one by one.")

else:
    st.info("👆 Please upload your customer Excel file to begin.")

st.caption("Stable & Free Method | No Headless Issues")
