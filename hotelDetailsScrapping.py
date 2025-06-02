import streamlit as st 
import requests
from bs4 import BeautifulSoup
import csv
import os

def webscrapper(web_url, f_name):
    st.info("⏳ Reading the content from the URL...")

    header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = requests.get(web_url, headers=header)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        hotel_divs = soup.find_all("div", role="listitem")

        file_path = f'{f_name}.csv'
        with open(file_path, 'w', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(['hotel_name', 'hotel_location', 'hotel_price', 'hotel_rating', 'hotel_score', 'hotel_review', 'hotel_link'])

            for details in hotel_divs:
                try:
                    hotel_name = details.find(name="div", class_="b87c397a13 a3e0b4ffd1").text.strip()
                except:
                    hotel_name = "NA"

                try:
                    hotel_location = details.find(name="span", class_="d823fbbeed f9b3563dd4").text.strip()
                except:
                    hotel_location = "NA"

                try:
                    hotel_price = details.find(name="span", class_="b87c397a13 f2f358d1de ab607752a2").text.replace('₹ ', '')
                except:
                    hotel_price = "NA"

                hotel_rating = details.find("div", class_="f63b14ab7a f546354b44 becbee2f63")
                hotel_rating = hotel_rating.get_text(strip=True) if hotel_rating else "No rating"

                hotel_score = details.find("div", class_="f63b14ab7a dff2e52086")
                hotel_score = hotel_score.get_text(strip=True) if hotel_score else "No Score"

                hotel_review = details.find(name="div", class_="fff1944c52 fb14de7f14 eaa8455879")
                hotel_review = hotel_review.get_text(strip=True) if hotel_review else "No review"

                hotel_link = details.find(name="a", href=True)
                hotel_link = hotel_link.get('href') if hotel_link else "NA"

                writer.writerow([hotel_name, hotel_location, hotel_price, hotel_rating, hotel_score, hotel_review, hotel_link])

        return file_path, "✅ Scraping completed!"
    else:
        return None, f"❌ Connection failed! Status code: {response.status_code}"


# ---------------------------------------------
# 🌐 Streamlit UI
# ---------------------------------------------

st.set_page_config(page_title="Hotel Details Scraper", layout="centered")

st.title("🏨 Hotel Booking Web Scraper")
st.markdown("Easily scrape hotel listings from [Booking.com](https://www.booking.com) and export as CSV.")

with st.expander("📌 How to use this scraper (click to expand)"):
    st.markdown("""
    **Step-by-Step:**

    1. Go to [Booking.com homepage](https://www.booking.com/index.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaGyIAQGYAQm4AQfIAQzYAQHoAQGIAgGoAgO4AvqT3MEGwAIB0gIkYTQzOGQ0OGEtOTg3OC00YjA2LThhYjctNDc2NWI3ZTM4ZjVm2AIF4AIB&sid=05f91942013529a737c376153cb04edb&keep_landing=1&sb_price_type=total&)
    2. Enter the destination, select dates, and click **Search**
    3. After results load, **copy the full URL** from the address bar
    4. Paste that URL in the field below
    5. Enter a file name and click **Scrape Hotels**
    6. Download the CSV!

    ✅ **Example**: `https://www.booking.com/searchresults.en-gb.html?dest_id=-2092174&...`
    """)

url = st.text_input("🔗 Paste the full Booking.com search URL:")
file_name = st.text_input("📁 Enter desired file name (no extension):")

if st.button("🚀 Scrape Hotels"):
    if url and file_name:
        with st.spinner("Scraping hotels... Please wait!"):
            path, status = webscrapper(url, file_name)
            st.success(status)
            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button("📥 Download CSV", data=f, file_name=path, mime="text/csv")
    else:
        st.warning("⚠️ Please enter both the URL and a file name.")


