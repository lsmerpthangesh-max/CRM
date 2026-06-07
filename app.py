import streamlit as st
import pandas as pd
import urllib.parse
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

st.set_page_config(page_title="Lingam Auto WhatsApp Sender", layout="wide")

st.title("🛒 Lingam Super Market - FULL AUTO WhatsApp Sender")

uploaded_file = st.file_uploader("Upload customers.xlsx", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.success(f"Loaded {len(df)} customers")
    st.dataframe(df.head())

    delay = st.slider("Delay (seconds)", 10, 60, 20)

    if st.button("🚀 START FULL AUTO SEND"):

        if 'Customer Name' not in df.columns or 'Phone Number' not in df.columns:
            st.error("Excel must contain 'Customer Name' and 'Phone Number'")
        else:

            # Message Templates
            templates = {
                "ThankYou": "Dear {name}, Thank you for shopping at Lingam Super Market! நன்றி!",
                "Promo": "Dear {name}, Month-end offer! Up to 20% OFF! Hurry!",
                "ReEngage": "Dear {name}, We miss you! Come back & get 10% discount!"
            }

            # Chrome setup
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")

            driver = webdriver.Chrome(options=chrome_options)

            # Open WhatsApp Web
            driver.get("https://web.whatsapp.com")

            st.warning("📱 Scan QR Code in browser (only first time)")
            time.sleep(20)  # time to scan QR

            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():

                name = str(row['Customer Name'])
                phone = str(row['Phone Number']).replace("+", "").replace(" ", "")
                campaign = str(row.get('Campaign Type', 'ThankYou'))

                message = templates.get(campaign, templates["ThankYou"]).format(name=name)

                encoded_msg = urllib.parse.quote(message)

                url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

                driver.get(url)

                status.text(f"Sending to {name} ({i+1}/{len(df)})")

                # Wait for message box
                time.sleep(10)

                try:
                    # Press Enter to send
                    box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                    box.send_keys(Keys.ENTER)
                except:
                    st.error(f"Failed for {name}")

                time.sleep(delay)

                progress.progress((i+1)/len(df))

            st.success("✅ ALL MESSAGES SENT AUTOMATICALLY!")
