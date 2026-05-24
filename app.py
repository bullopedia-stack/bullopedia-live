import streamlit as st
import google.generativeai as genai
import os

# तिजोरी से चाबी उठाना
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# instruction.txt फाइल से आपका प्रॉम्प्ट ऑटोमैटिक लोड करना
if os.path.exists("instruction.txt"):
    with open("instruction.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
else:
    SYSTEM_PROMPT = "You are a professional financial analyst bot."

# 🚨 100% वर्किंग लाइव सर्च टूल और सही मॉडल नेम (gemini-2.5-flash)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=SYSTEM_PROMPT,
    tools=[{"google_search": {}}]
)

# पोर्टल का पासवर्ड
VALID_PASSWORDS = ["STUDENT2026", "BULLGURU", "VIPACCESS"]

# ==============================================================================
# ✨ PREMIUM BLACK & ORANGE THEME (ब्यूटीफुल लुक) ✨
# ==============================================================================
st.set_page_config(page_title="BULLOPEDIA", page_icon="📈", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0d0d0d;
    color: #ffffff;
}
.orange-text {
    color: #ff7700;
    font-weight: bold;
}
#MainMenu, header, footer {visibility: hidden;}
div.stButton > button:first-child {
    background-color: #ff7700;
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    padding: 12px 24px;
    width: 100%;
}
div.stButton > button:first-child:hover {
    background-color: #e06600;
}
div.markdown-container-markdownContainer {
    background-color: #161616;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #262626;
}
p, h1, h2, h3, li, blockquote, span {
    color: #ffffff !important;
}
div.markdown-container-markdownContainer h1, div.markdown-container-markdownContainer strong {
    color: #ff7700 !important;
}
</style>
""", unsafe_allow_html=True)

def show_header():
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=90)
    with col2:
        st.markdown("<h1 style='color: #ff7700; margin-top: 5px; font-size: 2.8rem;'>BULLOPEDIA</h1>", unsafe_allow_html=True)

# ==============================================================================
# 🔐 एक्सेस गेटवे
# ==============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.write("")
    show_header()
    st.markdown("<h3 style='text-align: center; color: #ffffff;'>Welcome to <span class='orange-text'>BULLOPEDIA</span></h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff7700;'>🔐 Secure Student Portal Access</p>", unsafe_allow_html=True)
    st.write("")
    
    password_input = st.text_input("Enter your Access Code (Password) to login:", type="password")
    login_button = st.button("Access Portal")
    
    if login_button:
        if password_input.strip().upper() in VALID_PASSWORDS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Access Denied! Invalid password code typed.")
else:
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        show_header()
    with col_h2:
        st.write("")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.markdown("<hr style='border: 1px solid #262626;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #ff7700;'>📊 Live Fundamental Analysis Bot</h3>", unsafe_allow_html=True)

    stock_name = st.text_input("Enter Stock Name (e.g., TATA MOTORS):", placeholder="Type stock code ticker here...")
    analyze_button = st.button("Run Analysis")

    if analyze_button:
        if stock_name.strip() == "":
            st.warning("Please specify a valid Indian stock name first.")
        else:
            with st.spinner(f"🔍 Fetching live 2026 data and analyzing {stock_name}, please hold..."):
                try:
                    # लाइव सर्च का इस्तेमाल करके डेटा निकालने का सॉलिड कमांड
                    response = model.generate_content(
                        f"Search Google for the absolute latest live financial data of '{stock_name}' for the year 2026. Completely fill out every placeholder in your system instruction template layout based on your search results. Do not output raw instructions or N/A text."
                    )
                    st.success("Analysis Completed Successfully!")
                    st.markdown(f"### 📋 Analysis Report: <span class='orange-text'>{stock_name.upper()}</span>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(response.text, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}\nMake sure your Google Gemini API Key is working fine in Streamlit Secrets.")
