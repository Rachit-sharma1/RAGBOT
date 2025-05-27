import streamlit as st
import warnings
import logging
import requests
import streamlit_authenticator as stauth
import yaml
from streamlit_lottie import st_lottie
from descope.descope_client import DescopeClient
from descope.exceptions import AuthException
import time

# --- Page config ---
st.set_page_config(page_title="RagBot - AI Assistant", page_icon="🤖", layout="centered")

# --- Global Style ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #f0f4fd, #e0f7fa, #f3e5f5);
    background-attachment: fixed;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.main-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(31, 38, 135, 0.15);
    padding: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid #f1f5f9;
    max-width: 480px;
    margin: 0 auto;
}

.login-footer {
    text-align: center;
    font-size: 0.9rem;
    color: #7b8794;
    margin-top: 2rem;
}
.login-footer a {
    color: #0ea5e9;
    text-decoration: none;
}
.login-footer a:hover {
    text-decoration: underline;
}

footer {visibility: hidden;}

@media (max-width: 600px) {
    .main-card {padding: 1rem;}
}

/* Floating Action Button */
.fab-download {
    position: fixed;
    bottom: 32px;
    right: 32px;
    background: #0ea5e9;
    color: #fff;
    border-radius: 50%;
    width: 60px; height: 60px;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    box-shadow: 0 4px 12px rgba(31,38,135,0.14);
    cursor: pointer;
    z-index: 9999;
    border: none;
    transition: background 0.2s;
}
.fab-download:hover { background: #0284c7; }
</style>
""", unsafe_allow_html=True)

# --- Lottie loader ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except:
        return None

lotties = {
    "welcome": load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"),
    "background": load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ksgk2r3.json"),
}

# --- Config ---
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

try:
    with open("authentication/credentials.yaml", "r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    st.error(f"Error loading credentials: {e}")
    st.stop()

credentials = config.get("credentials", {})

authenticator = stauth.Authenticate(
    credentials,
    cookie_name="my_cookie_name",
    cookie_secret="dengo",
    cookie_expiry_days=1
)

DESCOPE_PROJECT_ID = str(st.secrets.get("DESCOPE_PROJECT_ID"))
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

# --- LOGIN SECTION ---
if ("authentication_status" not in st.session_state or not st.session_state["authentication_status"]) and "token" not in st.session_state:
    with st.container():
        st.markdown("<div style='margin-top: -80px'></div>", unsafe_allow_html=True)

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("## 👋 Welcome to RagBot")
        st.markdown("Your secure AI assistant for documents. Login to get started.")
        st.markdown("""
        - 📄 **Upload & Search** PDFs instantly  
        - 🔐 **Secure & Private** document access  
        - 💡 **AI-powered** summarization & Q/A  
        - ⚡ **Fast login** via username or Google  
        """)

        if lotties["welcome"]:
            st_lottie(lotties["welcome"], height=120, key="welcome_anim")

        tab1, tab2 = st.tabs(["Username/Password", "Sign in with Google"])

        with tab1:
            authenticator.login(location="main", key="LoginForm")

            if "authentication_status" in st.session_state:
                if st.session_state["authentication_status"] is False:
                    st.error("Incorrect username or password.")
                elif st.session_state["authentication_status"] is None:
                    st.warning("Enter your credentials to continue.")

        with tab2:
            st.markdown("### Sign in with Google")
            if st.button("Continue with Google", key="google_login"):
                response = descope_client.oauth.start(provider="google", return_url="http://localhost:8501")
                st.markdown(f'<meta http-equiv="refresh" content="0; url={response["url"]}">', unsafe_allow_html=True)

            if "code" in st.query_params:
                code = st.query_params["code"]
                st.query_params.clear()
                try:
                    with st.spinner("Signing in..."):
                        jwt_response = descope_client.sso.exchange_token(code)
                    st.session_state["token"] = jwt_response["sessionToken"].get("jwt")
                    st.session_state["refresh_token"] = jwt_response["refreshSessionToken"].get("jwt")
                    st.session_state["user"] = jwt_response["user"]
                    st.session_state["authentication_status"] = True
                    st.session_state["name"] = st.session_state["user"].get("name", "Google User")
                    st.rerun()
                except AuthException:
                    st.error("Google login failed.")

        st.markdown("""
        <div class='login-footer'>
            Need help? <a href='mailto:support@ragbot.com'>Contact us</a> |
            <a href='#'>Privacy</a> |
            <a href='#'>Terms</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop() 

# --- MAIN APP ---
from modules.chat import display_chat_history, handle_user_input, download_chat_history
from modules.pdf_handler import upload_pdfs
from modules.vectorstore import load_vectorstore
from modules.llm import get_llm_chain
from modules.chroma_inspector import inspect_chroma

# --- SIDEBAR: User Card and Controls ---
with st.sidebar:
    if "token" in st.session_state:
        # User Card
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(90deg,#e0f7fa,#f3e5f5 80%);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
                display: flex; align-items: center; gap: 0.8rem;
            ">
                <span style="font-size:2rem;">🧑‍💼</span>
                <div>
                    <div style="font-weight:600;">{st.session_state.get('name', 'Google User')}</div>
                    <div style="font-size:0.9rem; color:#7b8794;">Logged in</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.header("📥 Upload & Inspect PDFs")
        if st.button("Logout"):
            for key in ["token", "refresh_token", "user", "name"]:
                st.session_state.pop(key, None)
            st.session_state["authentication_status"] = False
            st.rerun()
    else:
        st.header("📥 Upload & Inspect PDFs")
        authenticator.logout("Logout", "sidebar")

# --- Animated Welcome Banner and Background ---
if st.session_state.get("authentication_status", False) or "token" in st.session_state:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #a7ffeb, #f3e5f5 80%);
            border-radius: 16px;
            padding: 1.2rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(31, 38, 135, 0.07);
            display: flex; align-items: center; gap: 1rem;
        ">
            <span style="font-size:2.2rem;">👋</span>
            <span style="font-size:1.2rem; font-weight:600;">
                Welcome, {st.session_state.get('name', 'User')}! Ready to explore your documents?
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if lotties["background"]:
        st_lottie(
            lotties["background"],
            height=80,
            speed=1,
            key="background_anim"
        )

# --- Main App UI ---
st.title("Ask RagBot! 🤖")

# Section Headings & Dividers
st.markdown("### 📄 Document Tools")
st.divider()

st.write(f"Hello, **{st.session_state.get('name', 'User')}**! Let's work with your documents.")

uploaded_files, submitted = upload_pdfs()

# --- Progress Bar for PDF Processing ---
if submitted and uploaded_files:
    progress_text = "Crunching your documents…"
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    with st.spinner("Finalizing..."):
        vectorstore = load_vectorstore(uploaded_files)
        st.session_state.vectorstore = vectorstore
    my_bar.empty()
    st.success("Vector database updated! 🎉")

# --- Chat Section ---
if "vectorstore" in st.session_state:
    st.markdown("### 💬 Chat with your Documents")
    st.divider()
    # Stylish Chat Container
    st.markdown(
        """
        <div style="
            background: rgba(255,255,255,0.97);
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(31,38,135,0.08);
            padding: 1.5rem 1.2rem 1.2rem 1.2rem;
            margin-bottom: 1.5rem;
        ">
        """,
        unsafe_allow_html=True
    )
    inspect_chroma(st.session_state.vectorstore)
    display_chat_history()
    handle_user_input(get_llm_chain(st.session_state.vectorstore))
    st.markdown("</div>", unsafe_allow_html=True)

    # Floating Action Button for Download
    st.markdown("""
    <button class="fab-download" onclick="document.getElementById('download-chat-btn').click()">⬇️</button>
    """, unsafe_allow_html=True)
    if st.button("📥 Download Chat History", key="download-chat-btn"):
        download_chat_history()
