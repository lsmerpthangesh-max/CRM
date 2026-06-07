import streamlit as st
import pandas as pd
import urllib.parse
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Lingam WhatsApp Auto Sender", layout="wide")

st.title("🛒 Lingam Super Market - Auto WhatsApp Sender")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"Loaded {len(df)} customers")

    delay = st.slider("Delay (seconds)", 10, 60, 20)

    if st.button("🚀 Start Auto Send"):

        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Required columns missing!")
        else:

            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market!",
                "Promo": "Dear {name}, Month-end offer! Up to 20% OFF!",
                "ReEngage": "Dear {name}, We miss you! Come back & get discount!"
            }

            # Chrome setup with profile (NO QR every time)
            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=chrome_profile")

            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            driver.get("https://web.whatsapp.com")

            st.warning("Scan QR if first time...")

            time.sleep(15)

            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():
                name = str(row['Customer Name'])
                phone = str(row['Phone Number']).replace("+", "").replace(" ", "")
                campaign = str(row.get('Campaign Type', 'ThankYou'))

                msg = templates.get(campaign, templates["ThankYou"]).format(name=name)
                encoded = urllib.parse.quote(msg)

                url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded}"
                driver.get(url)

                status.text(f"Sending to {name} ({i+1}/{len(df)})")

                time.sleep(8)

                try:
                    input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
                    input_box.send_keys(Keys.ENTER)
                except:
                    st.error(f"Failed for {name}")

                time.sleep(delay)
                progress.progress((i+1)/len(df))

            st.success("✅ Messages Sent Successfully!")
