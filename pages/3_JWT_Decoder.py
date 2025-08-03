import streamlit as st
import base64
import json

st.set_page_config(page_title="JWT Decoder", layout="centered")
st.title("🔐 JWT Decoder")

st.markdown(
    """
This tool decodes a [JWT (JSON Web Token)](https://jwt.io) into its components.
"""
)

jwt_token = st.text_area(
    "Paste your JWT here",
    height=150,
    placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
)

show_signature = st.checkbox("Show Signature", value=False)


def decode_segment(segment: str):
    # Add padding if needed
    segment += "=" * (4 - len(segment) % 4)
    decoded_bytes = base64.urlsafe_b64decode(segment)
    return decoded_bytes.decode("utf-8")


if jwt_token:
    parts = jwt_token.strip().split(".")

    if len(parts) != 3:
        st.error("❌ Invalid JWT. A JWT must have 3 parts separated by '.'")
    else:
        header, payload, signature = parts

        try:
            decoded_header = decode_segment(header)
            decoded_payload = decode_segment(payload)

            st.subheader("📦 Header")
            st.json(json.loads(decoded_header))

            st.subheader("🧾 Payload")
            st.json(json.loads(decoded_payload))

            if show_signature:
                st.subheader("🔏 Signature")
                st.code(signature, language="text")
            else:
                st.caption("✅ Signature is hidden (enable checkbox to see it)")

        except Exception as e:
            st.error("⚠️ Failed to decode JWT parts")
            st.exception(e)
