import streamlit as st
import warnings
import logging
import requests
import streamlit_authenticator as stauth
import yaml
from streamlit_lottie import st_lottie
from descope.descope_client import DescopeClient
from descope.exceptions import AuthException

# --- Page config ---
st.set_page_config(page_title="RagBot - AI Assistant", page_icon="🤖", layout="centered")

# --- CSS to remove Streamlit header & white space above content ---
st.markdown("""
<style>
/* Hide Streamlit's default header */
header[data-testid="stHeader"] {
    display: none;
}

/* Remove padding and margin above app content */
section[data-testid="stAppViewContainer"] > div:first-child {
    padding-top: 0 !important;
    margin-top: -4rem !important;
}

/* Reset body/app background and fonts */
html, body, .stApp {
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #f0f4fd, #e0f7fa, #f3e5f5);
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

/* Style main login card */
.main-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 18px;
    padding: 2rem;
    max-width: 480px;
    margin: 0 auto;
    box-shadow: 0 4px 24px rgba(31, 38, 135, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid #f1f5f9;
}

/* Footer styling */
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

/* Hide footer */
footer {
    visibility: hidden;
}

@media (max-width: 600px) {
    .main-card {
        padding: 1rem;
        margin-top: 0;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Lottie loader function ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except:
        return None

lotties = {
    "welcome": load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"),
}

# --- Suppress warnings/logging ---
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

# --- Load credentials ---
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

# --- Login screen ---
if ("authentication_status" not in st.session_state or not st.session_state["authentication_status"]) and "token" not in st.session_state:
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
                st.experimental_rerun()
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

# --- Main App ---
from modules.chat import display_chat_history, handle_user_input, download_chat_history
from modules.pdf_handler import upload_pdfs
from modules.vectorstore import load_vectorstore
from modules.llm import get_llm_chain
from modules.chroma_inspector import inspect_chroma

with st.sidebar:
    st.header("📥 Upload & Inspect PDFs")
    if "token" in st.session_state:
        if st.button("Logout"):
            for key in ["token", "refresh_token", "user", "name"]:
                st.session_state.pop(key, None)
            st.session_state["authentication_status"] = False
            st.experimental_rerun()
        st.success(f"Logged in as: {st.session_state.get('name', 'Google User')}")
    else:
        authenticator.logout("Logout", "sidebar")

st.title("Ask RagBot! 🤖")
st.write(f"Hello, **{st.session_state.get('name', 'User')}**! Let's work with your documents.")

uploaded_files, submitted = upload_pdfs()
if submitted and uploaded_files:
    with st.spinner("Crunching your documents..."):
        vectorstore = load_vectorstore(uploaded_files)
        st.session_state.vectorstore = vectorstore
    st.success("Vector database updated! 🎉")

if "vectorstore" in st.session_state:
    inspect_chroma(st.session_state.vectorstore)
    display_chat_history()
    handle_user_input(get_llm_chain(st.session_state.vectorstore))

if "vectorstore" in st.session_state and st.button("📥 Download Chat History"):
    download_chat_history()
