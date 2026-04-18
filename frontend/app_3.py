import streamlit as st
import requests

st.title("AI Business Intelligence System")

query = st.text_area("Enter your query")

if st.button("Analyze"):

    if query == "":
        st.warning("Please enter query")

    else:
        st.write("Processing...")

        try:
            res = requests.post("http://127.0.0.1:8000/analyze", json={"query": query})
            data = res.json()

            st.write("Analysis Complete")

            st.write("Agent Decision:")
            st.write(data["agent"])

            st.write("Module Output:")
            st.write(data["module_results"])

        except:
            st.write("Backend not running")