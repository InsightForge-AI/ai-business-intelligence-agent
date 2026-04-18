import streamlit as st
import requests
import time

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="AI BI System",
    page_icon="🤖",
    layout="wide"
)

# ------------------ SESSION STATE ------------------ #
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ SIDEBAR ------------------ #
with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.success("History cleared")

    st.markdown("---")
    st.info("💡 Tip: Ask detailed business queries for better insights")

# ------------------ HEADER ------------------ #
st.title("🤖 AI Business Intelligence System")
st.caption("AI-powered insights for smarter decisions")

# ------------------ LOADING EFFECT ------------------ #
def typing_effect():
    if "loaded" not in st.session_state:
        placeholder = st.empty()
        text = "⚙️ Initializing AI Engine..."
        out = ""

        for char in text:
            out += char
            placeholder.markdown(f"### {out}")
            time.sleep(0.015)

        placeholder.success("✅ Ready")
        st.session_state.loaded = True

typing_effect()

# ------------------ INPUT ------------------ #
query = st.text_area(
    "🔍 Enter your query",
    placeholder="e.g., Predict next quarter sales",
    height=100
)

# ------------------ API FUNCTION (CACHED) ------------------ #
@st.cache_data(show_spinner=False)
def call_backend_cached(query):
    return call_backend(query)

def call_backend(query):
    try:
        res = requests.post(
            "http://127.0.0.1:8000/analyze",
            json={"query": query},
            timeout=15
        )

        if res.status_code != 200:
            return {"error": f"Server error: {res.status_code}"}

        return res.json()

    except requests.exceptions.Timeout:
        return {"error": "⏱️ Timeout"}
    except requests.exceptions.ConnectionError:
        return {"error": "🔴 Backend not reachable"}
    except Exception as e:
        return {"error": str(e)}

# ------------------ BUTTON ------------------ #
col1, col2 = st.columns([3, 1])

with col1:
    analyze_btn = st.button("🚀 Analyze", use_container_width=True)

with col2:
    refresh_btn = st.button("🔄 Refresh")

# ------------------ ACTION ------------------ #
if analyze_btn:

    if not query.strip():
        st.warning("⚠️ Please enter a valid query")
        st.stop()

    with st.spinner("🧠 Thinking..."):
        result = call_backend_cached(query)

    if "error" in result:
        st.error(result["error"])
        st.stop()

    # Save history
    st.session_state.history.append({
        "query": query,
        "result": result
    })

# ------------------ DISPLAY HISTORY ------------------ #
if st.session_state.history:

    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"📝 Query {i}: {item['query']}", expanded=False):

            result = item["result"]

            tab1, tab2, tab3 = st.tabs([
                "🎯 Decision",
                "📊 Insights",
                "📄 Raw"
            ])

            with tab1:
                st.json(result.get("agent", {}))

            with tab2:
                modules = result.get("module_results", {})
                if modules:
                    for k, v in modules.items():
                        st.markdown(f"**{k}**")
                        st.json(v)
                else:
                    st.warning("No module results")

            with tab3:
                st.json(result)

# ------------------ EMPTY STATE ------------------ #
else:
    st.info("👆 Enter a query and click Analyze to see results")

# ------------------ FOOTER ------------------ #
st.markdown("---")
st.caption("🚀 AI BI System | Advanced UI v2")