import streamlit as st
import bcrypt

st.set_page_config(page_title="🔐 Bcrypt Hasher & Verifier")

st.title("🔐 Bcrypt Hasher & Verifier")

# Section: Hash a text
st.header("1. Generate a Bcrypt Hash")

input_text = st.text_input("Enter the text to hash (e.g., password):", type="password")

if input_text:
    hashed = bcrypt.hashpw(input_text.encode("utf-8"), bcrypt.gensalt())
    st.success("✅ Hashed Successfully!")
    st.code(hashed.decode(), language="text")

# Section: Verify a text against hash
st.header("2. Verify Text Against Hash")

verify_text = st.text_input("Enter the plain text to verify:", type="password")
hash_to_check = st.text_input("Enter the bcrypt hash to check against:")

if verify_text and hash_to_check:
    try:
        is_valid = bcrypt.checkpw(
            verify_text.encode("utf-8"), hash_to_check.encode("utf-8")
        )
        if is_valid:
            st.success("✅ Match! The text is valid for this hash.")
        else:
            st.error("❌ No match. The text does not correspond to this hash.")
    except Exception as e:
        st.error(f"⚠️ Error verifying hash: {e}")
