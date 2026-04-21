import streamlit as st
import requests
import json

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Business Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION ----------------
if "conversations" not in st.session_state:
    st.session_state.conversations = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "active_chat_index" not in st.session_state:
    st.session_state.active_chat_index = None


# ---------------- SIDEBAR STYLE ----------------
st.markdown("""
<style>

/* sidebar */
section[data-testid="stSidebar"]{
    background:#0b0f19;
    padding-top:15px;
}

/* new chat button */
.new-chat button{
    background:#1f2937 !important;
    color:white !important;
    border-radius:12px !important;
    padding:10px !important;
    font-size:14px !important;
}

/* section title */
.side-title{
    font-size:12px;
    color:#9ca3af;
    margin-top:15px;
    margin-bottom:6px;
}

/* chat buttons */
section[data-testid="stSidebar"] button{
    background:transparent !important;
    color:#e5e7eb !important;
    border:none !important;
    text-align:left !important;
    padding:8px !important;
    font-size:14px !important;
}

section[data-testid="stSidebar"] button:hover{
    background:#111827 !important;
    border-radius:8px;
}

/* divider */
.divider{
    height:1px;
    background:#1f2937;
    margin:12px 0;
}

/* MAIN UI */

.stApp{
    background: linear-gradient(135deg,#6a8fd8,#8ec5d6);
}

.block-container{
    padding-top:20px;
    padding-bottom:120px;
}

/* header */
.top-bar{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:55px;
    background:white;
    display:flex;
    align-items:center;
    justify-content:center;
    border-bottom:1px solid #e5e7eb;
    z-index:9999;
}

.title{
    font-size:24px;
    font-family:Georgia,serif;
    font-weight:600;
    color:black;
}

/* input fixed bottom */
[data-testid="stChatInput"]{
    position:fixed;
    bottom:35px;
    left:50%;
    transform:translateX(-50%);
    width:700px;
}

/* rounded input */
[data-testid="stChatInput"] textarea{
    border-radius:35px !important;
    padding:14px !important;
    background:#111827 !important;
    color:white !important;
    border:none !important;
    font-size:13px !important;
}

/* results */
.result-container{
    max-width:780px;
    margin:auto;
    margin-top:25px;
}

.result-container div{
    padding:12px !important;
    font-size:14px !important;
}

h3{
    font-size:14px !important;
}

[data-testid="stJson"]{
    font-size:10px !important;
}

[data-testid="stJson"] pre{
    font-size:10px !important;
}

/* PRINT SETTINGS */
@media print {

[data-testid="stChatInput"]{
display:none !important;
}

section[data-testid="stSidebar"]{
display:none !important;
}

.top-bar{
position:relative !important;
}

.stApp{
background:white !important;
}

}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown('<div class="new-chat">', unsafe_allow_html=True)

if st.sidebar.button("✏️ New Chat"):

    if st.session_state.current_chat:

        if st.session_state.active_chat_index is None:

            st.session_state.conversations.append(
                st.session_state.current_chat
            )

        else:

            st.session_state.conversations[
                st.session_state.active_chat_index
            ] = st.session_state.current_chat

    st.session_state.current_chat = []

    st.session_state.active_chat_index = None

    st.rerun()

st.sidebar.markdown('</div>', unsafe_allow_html=True)


st.sidebar.markdown(
    '<div class="side-title">Recents</div>',
    unsafe_allow_html=True
)


# chat list
for i, chat in enumerate(reversed(st.session_state.conversations)):

    real_index = len(st.session_state.conversations)-1-i

    first_query = chat[0]["query"] if chat else "New Chat"

    title = first_query.title()

    if len(title) > 45:
        title = title[:45] + "..."

    if st.sidebar.button(title, key=f"chat_{real_index}"):

        st.session_state.current_chat = list(
            st.session_state.conversations[real_index]
        )

        st.session_state.active_chat_index = real_index

        st.rerun()


st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# clear all
if st.sidebar.button("🗑 Clear All Chats"):

    st.session_state.conversations = []

    st.session_state.current_chat = []

    st.session_state.active_chat_index = None

    st.rerun()


# download only current chat
st.sidebar.download_button(

    "⬇ Download Session",

    data=json.dumps(st.session_state.current_chat, indent=2),

    file_name="current_chat.json",

    mime="application/json"

)


# ---------------- HEADER ----------------
st.markdown("""
<div class="top-bar">
<div class="title">
AI Business Intelligence
</div>
</div>
""", unsafe_allow_html=True)


# ---------------- INPUT ----------------
query = st.chat_input("Ask business question...")


if query:

    with st.spinner("Analyzing data..."):

        try:

            r = requests.post(

                "http://127.0.0.1:8000/analyze",

                json={"query": query, "model": "AUTO"}

            )

            result = r.json()

        except:

            result = {

                "agent": "error",

                "module_results": {

                    "error": "backend not running"

                }

            }

    result["query"] = query

    st.session_state.current_chat.append(result)

    if st.session_state.active_chat_index is not None:

        st.session_state.conversations[
            st.session_state.active_chat_index
        ] = st.session_state.current_chat

    st.rerun()


# ---------------- RESULTS ----------------
if st.session_state.current_chat:

    st.markdown("<div class='result-container'>", unsafe_allow_html=True)

    for item in st.session_state.current_chat:

        st.markdown(f"""
        <div style="
            background:#22c55e20;
            padding:12px;
            border-radius:10px;
            font-size:14px;
            margin-bottom:18px;
        ">
        <b>Query :</b> {item.get("query")}
        </div>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns(2)

        with col1:

            st.subheader("Agent")

            st.json([item.get("agent")], expanded=True)

        with col2:

            st.subheader("Output")

            st.json(item.get("module_results"), expanded=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- AUTO SCROLL ----------------
st.markdown("""
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)
