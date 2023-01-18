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
    st.markdown("Upload a CSV file containing a list of URLs to check the indexation status. Note, the column containing the URLs should be titled 'url'")
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
            <form action="data
            :text/csv;charset=utf-8,%EF%BB%BF" method="post" enctype="text/csv" id="csv_download_form">
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
            indexed_count = indexation_count["URL is Indexed"]
            not_indexed_count = indexation_count["URL is Not Indexed"]
            total = indexed_count + not_indexed_count
            indexed_percent = (indexed_count/total) * 100
            not_indexed_percent = (not_indexed_count/total) * 100
            chart_data = pd.DataFrame({'Indexed':[indexed_percent, not_indexed_percent]},index = ['Indexed','Not Indexed'])
            st.pie_chart(chart_data)
        except:
            st.write("Invalid file format")
    else:
        url_input = st.text_input("Enter a single URL")
        st.write(f"{url_input}: {is_page_indexed(url_input)}")
        indexed_count = 0
        not_indexed_count = 0
        if is_page_indexed(url_input) == 'URL is Indexed':
            indexed_count += 1
        else:
            not_indexed_count += 1
        total = indexed_count + not_indexed_count
        indexed_percent = (indexed_count/total) * 100
        not_indexed_percent = (not_indexed_count/total) * 100
        chart_data = pd.DataFrame({'Indexed':[indexed_percent, not_indexed_percent]},index = ['Indexed','Not Indexed'])
        st.pie_chart(chart_data)

if __name__ == "__main__":
    main()
