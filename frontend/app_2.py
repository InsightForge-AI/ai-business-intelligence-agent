import streamlit as st
import httpx

st.set_page_config(page_title="Easy NLP Analyzer", page_icon="🧠", layout="centered")

st.title("Easy NLP Analyzer")
st.write(
    "Paste your text below and click **Analyze**. The app shows sentiment, a short summary, and top keywords."
)

with st.form("nlp_form"):
    text = st.text_area(
        "Your text",
        height=240,
        placeholder="Type or paste text here...",
    )
    submitted = st.form_submit_button("Analyze text")

if submitted:
    if not text.strip():
        st.warning("Please enter some text before analyzing.")
    else:
        with st.spinner("Analyzing your text..."):
            try:
                response = httpx.post(
                    "http://localhost:8000/nlp/analyze",
                    json={"text": text},
                    timeout=10.0,
                )
                response.raise_for_status()
                result = response.json()

                st.success("Analysis complete!")
                st.markdown("---")

                st.subheader("📌 Summary")
                st.info(result.get("summary", "No summary returned."))

                st.subheader("😊 Sentiment")
                st.metric(label="Sentiment", value=result.get("sentiment", "Unknown"))

                st.subheader("🔑 Keywords")
                keywords = result.get("keywords", [])
                if keywords:
                    st.write(" ".join(f"`{keyword}`" for keyword in keywords))
                else:
                    st.write("No keywords returned.")

                st.subheader("📄 Full response")
                st.json(result)
            except httpx.RequestError as exc:
                st.error(f"Request error: {exc}")
            except httpx.HTTPStatusError as exc:
                st.error(f"API error: {exc.response.status_code} - {exc.response.text}")