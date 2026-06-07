import streamlit as st
import pandas as pd
import urllib.parse
import time
import os

st.set_page_config(page_title="Lingam Super Market WhatsApp", layout="wide")

st.title("🛒 Lingam Super Market - WhatsApp Bulk Sender")
st.markdown("**Upload → Generate → Send Automation**")

# Template Download
template_path = "/home/workdir/artifacts/lingam_customers_template.xlsx"
if os.path.exists(template_path):
    with open(template_path, "rb") as f:
        st.download_button(
            label="📥 Download Excel Template",
            data=f,
            file_name="lingam_customers_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

uploaded_file = st.file_uploader("Upload your customers.xlsx file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ Loaded **{len(df)}** customers successfully!")
    st.dataframe(df.head(20), use_container_width=True)

    delay = st.slider("Delay between messages (seconds)", 10, 45, 18)

    if st.button("🚀 Generate & Start Sending Process", type="primary", use_container_width=True):
        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Missing required columns: Customer Name and Phone Number")
        else:
            st.subheader("🔄 Processing Messages...")

            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market! நன்றி உங்கள் ஆதரவுக்கு! Visit again soon.",
                "Promo": "Dear {name}, Month-end special offer at Lingam Super Market! Up to 20% OFF! இந்த மாத இறுதி சலுகை! Hurry!",
                "ReEngage": "Dear {name}, We miss you at Lingam Super Market! Special 10% discount waiting. மீண்டும் வருகை தரவும்!"
            }

            progress_bar = st.progress(0)
            status_text = st.empty()
            success_count = 0

            for idx, row in df.iterrows():
                name = str(row.get('Customer Name', 'Customer')).strip()
                phone_raw = str(row.get('Phone Number', '')).strip()
                phone = phone_raw.replace("+", "").replace(" ", "")
                campaign = str(row.get('Campaign Type', 'ThankYou')).strip()

                message = templates.get(campaign, templates["ThankYou"]).format(name=name)
                encoded_message = urllib.parse.quote(message)
                
                wa_link = f"https://wa.me/{phone}?text={encoded_message}"

                status_text.text(f"[{idx+1}/{len(df)}] Opening link for {name}...")
                
                # Display clickable link
                st.markdown(f"**{idx+1}. {name}** → [📱 Click to Send]({wa_link})")
                
                success_count += 1
                progress_bar.progress((idx + 1) / len(df))
                
                # Auto wait before next
                time.sleep(delay)

            st.success(f"🎉 Process Completed! Generated {success_count} messages.")
            st.info("✅ Open WhatsApp Web → Click the links one by one. Messages are pre-filled.")

else:
    st.info("👆 Please upload your customer Excel file.")

st.caption("This is the most stable free method. WhatsApp Web must be open.")
