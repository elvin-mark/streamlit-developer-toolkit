import streamlit as st
import base64

st.set_page_config(page_title="Base64 Encoder/Decoder", layout="centered")
st.title("🧮 Base64 Encoder & Decoder")

mode = st.radio("Select Mode", ["Encode", "Decode"], horizontal=True)

user_input = st.text_area(
    "Enter text" if mode == "Encode" else "Enter Base64 string",
    height=150,
    placeholder="Type or paste here...",
)


def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def decode_base64(b64_text: str) -> str:
    b64_text += "=" * (-len(b64_text) % 4)  # Fix missing padding
    return base64.b64decode(b64_text).decode("utf-8")


if user_input:
    try:
        if mode == "Encode":
            result = encode_base64(user_input)
            st.success("✅ Encoded Base64:")
        else:
            result = decode_base64(user_input)
            st.success("✅ Decoded Text:")

        st.code(result, language="text")
    except Exception as e:
        st.error("⚠️ Error during conversion:")
        st.exception(e)
