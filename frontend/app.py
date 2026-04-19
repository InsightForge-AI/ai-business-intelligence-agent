import streamlit as st
import requests

# page title
st.title("AI Business Intelligence System")

st.write("Enter query to analyze")


# input box
query = st.text_area(

    "Enter your query",

    placeholder="Example: sales trend prediction"

)


# button
if st.button("Analyze"):


    if not query:

        st.warning("Please enter query")


    else:

        st.info("Processing...")


        try:

            response = requests.post(

                "http://127.0.0.1:8000/analyze",

                json={"query": query}

            )


            result = response.json()


            st.success("Analysis Complete")


            st.subheader("Agent Decision")

            st.write(result.get("agent"))


            st.subheader("Module Output")

            st.json(result.get("module_results"))


        except:

            st.error("Backend not running")