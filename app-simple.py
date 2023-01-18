import streamlit as st
import pandas as pd
import requests
import time
import io


def is_page_indexed(url):
    url = "https://www.google.com/search?q=site:"+url
    response = requests.get(url)
    if "did not match any documents" in response.text:
        return "URL is Not Indexed"
    else:
        return "URL is Indexed"

def main():
    st.title("URL Index Checker")

    uploaded_file = st.file_uploader("Upload a CSV file containing a list of URLs", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(io.StringIO(uploaded_file.read().decode('utf-8')))
            total_urls = len(df)
            start_time = time.time()
            for i, row in df.iterrows():
                st.write(f"{row['url']}: {is_page_indexed(row['url'])}")
                progress = (i+1) / total_urls
                remaining_time = ((time.time() - start_time) / (i+1)) * (total_urls - (i+1))
                st.progress(progress)
                st.write(f"Time remaining: {round(remaining_time, 2)} seconds")
        except:
            st.write("Invalid file format")

if __name__ == "__main__":
    main()

