import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Lingam Super Market WhatsApp", layout="wide")

st.title("🛒 Lingam Super Market - WhatsApp Bulk Sender")
st.markdown("**File Upload Based Automation**")

# Template Download
with open("/home/workdir/artifacts/lingam_customers_template.xlsx", "rb") as f:
    st.download_button(
        label="📥 Download Excel Template",
        data=f,
        file_name="lingam_customers_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

uploaded_file = st.file_uploader("Upload customers.xlsx", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ Loaded {len(df)} customers")
    
    st.subheader("Preview")
    st.dataframe(df.head(15), use_container_width=True)

    delay = st.slider("Recommended delay between opening links (seconds)", 5, 30, 12)

    if st.button("🚀 Generate All WhatsApp Links", type="primary", use_container_width=True):
        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Missing columns: Customer Name and Phone Number")
        else:
            st.subheader("✅ Generated Links (Click to Send)")

            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market! நன்றி உங்கள் ஆதரவுக்கு!",
                "Promo": "Dear {name}, Month-end offer at Lingam Super Market! Up to 20% OFF! இந்த மாத இறுதி சலுகை!",
                "ReEngage": "Dear {name}, We miss you at Lingam Super Market! Special discount waiting. மீண்டும் வருகை தரவும்!"
            }

            for idx, row in df.iterrows():
                name = str(row.get('Customer Name', '')).strip()
                phone = str(row.get('Phone Number', '')).strip().replace(" ", "").replace("+", "")
                campaign = str(row.get('Campaign Type', 'ThankYou')).strip()

                message = templates.get(campaign, templates["ThankYou"]).format(name=name)
                encoded_msg = urllib.parse.quote(message)
                
                wa_link = f"https://wa.me/{phone}?text={encoded_msg}"
                
                st.markdown(f"**{idx+1}. {name}** → [Send Message]({wa_link})")
            
            st.info("👆 Click each link one by one. WhatsApp Web will open with pre-filled message.")

else:
    st.info("Please upload your Excel file")

st.caption("Note: This is the most stable free method. For true full auto, use WhatsApp Business API later.")
