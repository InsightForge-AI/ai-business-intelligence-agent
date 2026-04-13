import streamlit as st
import requests

# page title
st.title("AI Business Intelligence System")

st.write("Enter query to analyze")


# input box
query = st.text_area("Enter your query", placeholder="Example: sales trend prediction")


# button
if st.button("🔍 Analyze", use_container_width=True, type="primary"):

    if not query:

        st.warning("Please enter query")

    else:

        with st.spinner("🔄 Processing your query..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze", json={"query": query}, timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("✅ Analysis Complete")

                    # Display results in tabs
                    tab1, tab2 = st.tabs(["🎯 Agent Decision", "📊 Module Output"])

                    with tab1:
                        st.write(result.get("agent", "No decision available"))

                    with tab2:
                        st.json(result.get("module_results", {}))
                else:
                    st.error(f"❌ Error: {response.status_code}")

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout - backend is taking too long")
            except requests.exceptions.ConnectionError:
                st.error("🔴 Cannot connect to backend at http://127.0.0.1:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
