import streamlit as st
import pandas as pd
import pywhatkit
import time
import os
from datetime import datetime

st.set_page_config(page_title="Lingam Super Market WhatsApp Sender", layout="wide")
st.title("🛒 Lingam Super Market - WhatsApp Bulk Sender")
st.markdown("### Professional Automated Messaging System")

# File Upload
uploaded_file = st.file_uploader("Upload your customer Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ File loaded successfully! Total Customers: **{len(df)}**")
    
    st.subheader("📋 Customer Data Preview")
    st.dataframe(df.head(20), use_container_width=True)
    
    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        delay = st.slider("Delay between messages (seconds)", 25, 60, 35)
    with col2:
        start_row = st.number_input("Start from row (0 = first customer)", min_value=0, value=0)
    
    if st.button("🚀 Start Sending Messages", type="primary", use_container_width=True):
        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Missing required columns: 'Customer Name' and 'Phone Number'")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            success = 0
            failed = 0
            
            TEMPLATES = {
                "ThankYou": "Dear {name},\nThank you for shopping at Lingam Super Market!\nநன்றி உங்கள் ஆதரவுக்கு! Visit us again soon.",
                "Promo": "Dear {name},\nMonth-end special offer at Lingam Super Market!\nUp to 20% OFF!\nஇந்த மாத இறுதி சலுகை!",
                "ReEngage": "Dear {name},\nWe miss you at Lingam Super Market!\nSpecial 10% discount waiting.\nமீண்டும் வருகை தரவும்!"
            }
            
            for idx, row in df.iterrows():
                if idx < start_row:
                    continue
                    
                name = str(row['Customer Name']).strip()
                phone = str(row['Phone Number']).strip().replace(" ", "")
                campaign = str(row.get('Campaign Type', 'ThankYou')).strip()
                
                message = TEMPLATES.get(campaign, TEMPLATES["ThankYou"]).format(name=name)
                
                try:
                    status_text.text(f"Sending to {name} ({phone})...")
                    pywhatkit.sendwhatmsg_instantly(
                        phone_no=phone,
                        message=message,
                        wait_time=delay,
                        tab_close=True,
                        close_time=5
                    )
                    success += 1
                except Exception as e:
                    st.warning(f"Failed for {name}: {e}")
                    failed += 1
                
                progress = min((idx + 1) / len(df), 1.0)
                progress_bar.progress(progress)
                time.sleep(delay)
            
            st.success(f"✅ Automation Completed! Sent: {success} | Failed: {failed}")

else:
    st.info("👆 Please upload your Excel file using the template provided below.")

# Download Template Button
with open("/home/workdir/artifacts/lingam_customers_template.xlsx", "rb") as file:
    st.download_button(
        label="📥 Download Excel Template",
        data=file,
        file_name="lingam_customers_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.caption("Note: Keep WhatsApp Web open and logged in on Chrome during sending.")
