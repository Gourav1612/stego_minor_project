import streamlit as st
from stego import encode_image, decode_image
from io import BytesIO
from PIL import Image
from cryptography.fernet import Fernet
import base64
import hashlib

# --- KMS CORE ---
def get_kms_key(password: str):
    hash_gen = hashlib.sha256(password.encode()).digest() 
    return base64.urlsafe_b64encode(hash_gen)

def secure_encrypt(data, password):
    key = get_kms_key(password)
    return Fernet(key).encrypt(data.encode()).decode()

def secure_decrypt(cipher, password):
    try:
        key = get_kms_key(password)
        return Fernet(key).decrypt(cipher.encode()).decode()
    except Exception:
        return None

# --- UI CONFIGURATION ---
st.set_page_config(page_title="STAGNOGRAPHY", layout="wide")

# CSS - Changed to Gold (#D4AF37) and Charcoal (#121212)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

    .stApp {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Roboto Mono', monospace;
    }

    .header-box {
        border-bottom: 2px solid #1E1E1E;
        padding-bottom: 20px;
        margin-bottom: 40px;
    }

    .title-text {
        color: #D4AF37; /* Gold Accent */
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: #121212;
    }

    .stTabs [data-baseweb="tab"] {
        border: 1px solid #1E1E1E;
        background-color: #1A1A1A;
        color: #888888;
        height: 50px;
        padding: 0 40px;
        font-size: 13px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #222222 !important;
        color: #D4AF37 !important;
        border-bottom: 2px solid #D4AF37 !important;
    }

    .stTextArea textarea, .stTextInput input {
        background-color: #1A1A1A !important;
        border: 1px solid #333333 !important;
        color: #FFFFFF !important;
        border-radius: 0px !important;
    }

    .stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border-radius: 0px !important;
        font-weight: 700;
        border: none;
        width: 100%;
        height: 45px;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #FFFFFF !important;
        box-shadow: 0 0 15px #D4AF37;
    }

    [data-testid="column"] {
        border: 1px solid #1E1E1E;
        padding: 20px !important;
        background-color: #161616;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-box">
        <div class="title-text">IMAGE STEGANOGRAPHY</div>
        <div style="color: #666666; font-size: 11px; letter-spacing: 1px;">
            SECURE LAYERED STEGANOGRAPHY PROTOCOL
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TABS & LOGIC (SAME AS YOUR ORIGINAL) ---
tab_enc, tab_dec = st.tabs(["INJECT_PAYLOAD", "EXTRACT_PAYLOAD"])

with tab_enc:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("<p style='color:#666'>IMAGE_INPUT</p>", unsafe_allow_html=True)
        img_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if img_file: st.image(img_file, use_container_width=True)
    with c2:
        st.markdown("<p style='color:#666'>PAYLOAD_DATA</p>", unsafe_allow_html=True)
        msg = st.text_area("PLAINTEXT", placeholder="Enter sensitive information...", height=150, label_visibility="collapsed")
        st.markdown("<p style='color:#666'>AUTHORIZATION_KEY</p>", unsafe_allow_html=True)
        key = st.text_input("KEY", type="password", label_visibility="collapsed")
        if st.button("ENCODE"):
            if not key or not msg: st.error("CORE_FAILURE: PARAMETERS_NULL")
            else:
                try:
                    with st.spinner("ENCRYPTING..."):
                        cipher_text = secure_encrypt(msg, key)
                        raw_img = Image.open(img_file).convert('RGB')
                        stego_img = encode_image(raw_img, cipher_text)
                        buf = BytesIO()
                        stego_img.save(buf, format="PNG")
                        st.success("ENCODING_COMPLETE")
                        st.download_button(label="EXPORT", data=buf.getvalue(), file_name="secured_image.png", mime="image/png")
                except Exception as e: st.error(f"ERROR: {e}")

with tab_dec:
    c3, c4 = st.columns([1, 1])
    with c3:
        st.markdown("<p style='color:#666'>ARTIFACT_SOURCE</p>", unsafe_allow_html=True)
        stego_file = st.file_uploader("UPLOAD", type=["png"], key="dec_upload", label_visibility="collapsed")
        if stego_file: st.image(stego_file, use_container_width=True)
    with c4:
        st.markdown("<p style='color:#666'>DECRYPTION_AUTHORIZATION</p>", unsafe_allow_html=True)
        dec_key = st.text_input("AUTH_KEY", type="password", key="dec_key", label_visibility="collapsed")
        if st.button("DECODE"):
            if not dec_key: st.error("CORE_FAILURE: AUTH_KEY_NULL")
            else:
                with st.spinner("DECRYPTING..."):
                    stego_img = Image.open(stego_file).convert('RGB')
                    hidden_data = decode_image(stego_img)
                    final_text = secure_decrypt(hidden_data, dec_key)
                    if final_text:
                        st.success("ACCESS_GRANTED")
                        st.markdown("<p style='color:#D4AF37; font-size:12px;'>EXTRACTED_DATA:</p>", unsafe_allow_html=True)
                        st.code(final_text, language=None)
                    else: st.error("ACCESS_DENIED: AUTHENTICATION_FAILED")

st.markdown("<div style='margin-top:100px; text-align:center; color:#333; font-size:10px;'>STAGNOGRAPHY_MINOR_PROJECT</div>", unsafe_allow_html=True)