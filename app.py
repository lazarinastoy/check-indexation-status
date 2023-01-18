import streamlit as st
import pandas as pd
import requests
import time
import io
from collections import Counter

def is_page_indexed(url):
    url = "https://www.google.com/search?q=site:"+url
    response = requests.get(url)
    if "did not match any documents" in response.text:
        return "URL is Not Indexed"
    else:
        return "URL is Indexed"

def main():
    st.set_page_config(page_title="URL Index Checker", page_icon=":guardsman:", layout="wide")
    st.title("URL Index Checker")
    st.markdown("Upload a CSV file containing a list of URLs to check the indexation status.")
    uploaded_file = st.file_uploader("Upload a CSV file containing a list of URLs", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(io.StringIO(uploaded_file.read().decode('utf-8')))
            total_urls = len(df)
            start_time = time.time()
            df['Indexation Status'] = df['url'].apply(is_page_indexed)
            indexation_count = Counter(df['Indexation Status'])
            st.write(indexation_count)
            st.write("Indexation status saved in the uploaded csv.")
            st.markdown("Download the csv with Indexation Status")
            buffer = io.StringIO()
            df.to_csv(buffer,index=False)
            buffer.seek(0)
            st.markdown('Download the csv')
            st.markdown("""
            <form action="data:text/csv;charset=utf-8,%EF%BB%BF" method="post" enctype="text/csv" id="csv_download_form">
                <input type="hidden" name="file" value='{file}'/>
                <input type="submit" value="Download" style="display: none" id="csv_download_button"/>
            </form>""".format(file=buffer.getvalue()), unsafe_allow_html=True)
            st.markdown("""<button onclick="document.getElementById('csv_download_button').click();" class="btn btn-primary">Download CSV</button>""", unsafe_allow_html=True)
            st.markdown("""
                <script>
                document.getElementById('csv_download_form').addEventListener('submit', function(event) {
                    event.preventDefault();
                    var form = event.target;
                    var a = document.createElement('a');
                    a.href = form.action + form.elements.file.value;
                    a.download = 'data.csv';
                    a.click();
                });
                </script>
            """, unsafe_allow_html=True)
           
