
import streamlit as st
import requests
import time

# ------------------ Page Config ------------------ #
st.set_page_config(
    page_title="AI Business Intelligence System",
    layout="centered"
)

# ------------------ Title ------------------ #
st.title("🤖 AI Business Intelligence System")

# ------------------ Typing Effect (Run Once) ------------------ #
if "loaded" not in st.session_state:
    typing_placeholder = st.empty()

    text = "⚙️ Initializing AI Modules..."
    display_text = ""

    for char in text:
        display_text += char
        typing_placeholder.markdown(f"**{display_text}**")
        time.sleep(0.03)

    typing_placeholder.markdown("**⚙️ Initializing AI Modules... ✅ Ready**")
    st.session_state.loaded = True
else:
    st.markdown("**⚙️ Initializing AI Modules... ✅ Ready**")

# ------------------ Description ------------------ #
st.write("Enter query to analyze")

# ------------------ Input ------------------ #
query = st.text_area(
    "Enter your query",
    placeholder="Example: sales trend prediction"
)

# ------------------ Button ------------------ #
if st.button("🔍 Analyze", use_container_width=True, type="primary"):

    # ✅ Input Validation
    if not query or not query.strip():
        st.warning("⚠️ Please enter a valid query before proceeding.")
        st.stop()

    # ✅ Loading Spinner
    with st.spinner("🔄 Processing your query... Please wait..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"query": query},
                timeout=10
            )

            # ❌ Server Error
            if response.status_code != 200:
                st.error(f"⚠️ Server error ({response.status_code}). Please try again later.")
                st.stop()

            # ❌ Invalid JSON
            try:
                result = response.json()
            except ValueError:
                st.error("❌ Invalid response from backend (not JSON).")
                st.stop()

            # ❌ Empty Response
            if not result:
                st.warning("⚠️ No response received from backend.")
                st.stop()

            # ------------------ UI Layout ------------------ #
            st.success("✅ Analysis Complete")
            st.markdown("---")

            col1, col2 = st.columns(2)

            # -------- Agent Decision -------- #
            with col1:
                st.subheader("🎯 Agent Decision")
                st.json(result.get("agent", "No decision available"))

            # -------- Module Output -------- #
            with col2:
                st.subheader("📊 Module Output")
                module_output = result.get("module_results", {})

                if module_output:
                    st.json(module_output)
                else:
                    st.warning("No module output returned.")

            # -------- Full Response -------- #
            st.markdown("---")
            st.subheader("📄 Full Response")
            st.json(result)

        # ------------------ Error Handling ------------------ #
        except requests.exceptions.ConnectionError:
            st.error("🔴 Cannot connect to backend. Ensure server is running on port 8000.")

        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Backend is taking too long to respond.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {str(e)}")

        except Exception:
            st.error("❌ Unexpected error occurred. Please try again.")

