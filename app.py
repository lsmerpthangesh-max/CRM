import streamlit as st
import pandas as pd
import urllib.parse
import time
import os
from datetime import datetime

st.set_page_config(page_title="Lingam Super Market WhatsApp", layout="wide")

st.title("🛒 Lingam Super Market - WhatsApp Bulk Sender")
st.markdown("**File Upload + Automation System**")

# Template Download
template_path = "/home/workdir/artifacts/lingam_customers_template.xlsx"
if os.path.exists(template_path):
    with open(template_path, "rb") as f:
        st.download_button("📥 Download Excel Template", data=f, file_name="lingam_customers_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

uploaded_file = st.file_uploader("Upload customers.xlsx", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ Loaded {len(df)} customers")
    st.dataframe(df.head(15), use_container_width=True)

    mode = st.radio("Choose Sending Mode", ["Generate Links (Manual Click)", "Auto Send using Selenium"])

    delay = st.slider("Delay between messages (seconds)", 20, 60, 35)

    if st.button("🚀 START SENDING", type="primary", use_container_width=True):
        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Missing columns")
        else:
            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market! நன்றி உங்கள் ஆதரவுக்கு! Visit again soon.",
                "Promo": "Dear {name}, Month-end special offer at Lingam Super Market! Up to 20% OFF! இந்த மாத இறுதி சலுகை!",
                "ReEngage": "Dear {name}, We miss you at Lingam Super Market! Special 10% discount waiting. மீண்டும் வருகை தரவும்!"
            }

            if mode == "Generate Links (Manual Click)":
                st.subheader("Generated Links")
                for idx, row in df.iterrows():
                    name = str(row.get('Customer Name', '')).strip()
                    phone = str(row.get('Phone Number', '')).strip().replace("+", "").replace(" ", "")
                    campaign = str(row.get('Campaign Type', 'ThankYou')).strip()
                    message = templates.get(campaign, templates["ThankYou"]).format(name=name)
                    link = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"
                    st.markdown(f"**{idx+1}. {name}** → [Send]({link})")
                st.info("Click each link manually.")

            else:  # Auto Mode with Selenium
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.common.by import By
                    from webdriver_manager.chrome import ChromeDriverManager
                    from selenium.webdriver.chrome.service import Service
                    
                    st.info("Launching WhatsApp Web... Please scan QR code in the opened browser.")
                    
                    options = Options()
                    options.add_argument("--user-data-dir=whatsapp_session")
                    options.add_argument("--start-maximized")
                    
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                    driver.get("https://web.whatsapp.com")
                    
                    st.success("Browser opened. Scan QR code if needed.")
                    time.sleep(15)  # Time to scan QR
                    
                    success = 0
                    progress_bar = st.progress(0)
                    
                    for idx, row in df.iterrows():
                        name = str(row.get('Customer Name', '')).strip()
                        phone = str(row.get('Phone Number', '')).strip().replace("+", "").replace(" ", "")
                        campaign = str(row.get('Campaign Type', 'ThankYou')).strip()
                        
                        message = templates.get(campaign, templates["ThankYou"]).format(name=name)
                        
                        try:
                            url = f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}"
                            driver.get(url)
                            time.sleep(8)  # Wait for chat to load
                            
                            send_button = driver.find_element(By.XPATH, '//div[@data-testid="compose-box-send-button"]')
                            send_button.click()
                            success += 1
                            st.write(f"✅ Sent to {name}")
                        except Exception as e:
                            st.warning(f"Failed {name}: {e}")
                        
                        progress_bar.progress((idx + 1) / len(df))
                        time.sleep(delay)
                    
                    st.success(f"Completed! Sent: {success}")
                    driver.quit()
                    
                except Exception as e:
                    st.error(f"Selenium Error: {e}. Install webdriver-manager and try again.")

else:
    st.info("Upload your Excel file to start.")

st.caption("Auto mode opens browser and tries to send. Keep it running.")
