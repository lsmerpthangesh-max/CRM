import streamlit as st
import pandas as pd
import urllib.parse
import time
import os

st.set_page_config(page_title="Lingam Super Market WhatsApp Sender", layout="wide")

st.title("🛒 Lingam Super Market - WhatsApp Bulk Sender")
st.markdown("**Efficient Automation System**")

# Download Template
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
    st.success(f"✅ Loaded **{len(df)}** customers")
    st.dataframe(df.head(20), use_container_width=True)

    delay = st.slider("Delay between messages (seconds)", 15, 60, 25)

    if st.button("🚀 START AUTOMATIC LINK OPENING", type="primary", use_container_width=True):
        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Missing columns: Customer Name and Phone Number")
        else:
            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market! நன்றி உங்கள் ஆதரவுக்கு! Visit again soon.",
                "Promo": "Dear {name}, Month-end special offer at Lingam Super Market! Up to 20% OFF! இந்த மாத இறுதி சலுகை! Hurry!",
                "ReEngage": "Dear {name}, We miss you at Lingam Super Market! Special 10% discount waiting. மீண்டும் வருகை தரவும்!"
            }

            progress_bar = st.progress(0)
            status = st.empty()

            for idx, row in df.iterrows():
                name = str(row.get('Customer Name', '')).strip()
                phone = str(row.get('Phone Number', '')).strip().replace(" ", "").replace("+", "")
                campaign = str(row.get('Campaign Type', 'ThankYou')).strip()

                message = templates.get(campaign, templates["ThankYou"]).format(name=name)
                encoded = urllib.parse.quote(message)

                link = f"https://wa.me/{phone}?text={encoded}"

                status.text(f"[{idx+1}/{len(df)}] Opening WhatsApp for **{name}**...")
                
                # Show clickable link
                st.markdown(f"**{idx+1}. {name}** → [📱 OPEN & SEND]({link})")

                progress_bar.progress((idx + 1) / len(df))
                time.sleep(delay)   # Wait before next link

            st.success("✅ All links processed! Now click 'Send' in WhatsApp for each chat.")
            st.info("💡 Keep WhatsApp Web open in Chrome. Click the links one by one.")

else:
    st.info("👆 Upload your Excel file first")

st.caption("This is the most stable method. Full auto-click is not possible reliably in Streamlit on server.")
