import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="QR Code Generator", layout="centered")
st.title("🔲 QR Code Generator")

# User Input
data = st.text_input(
    "Enter text or URL to generate QR code", placeholder="https://example.com"
)
size = st.slider(
    "QR Code Size (pixels)", min_value=100, max_value=800, value=300, step=50
)


# Generate QR Code
def generate_qr(data: str, size: int) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((size, size))


if data:
    try:
        qr_img = generate_qr(data, size)
        st.image(qr_img, caption="QR Code Preview")

        # Download Button
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button(
            label="📥 Download QR Code",
            data=buf.getvalue(),
            file_name="qr_code.png",
            mime="image/png",
        )
    except Exception as e:
        st.error("⚠️ Failed to generate QR code.")
        st.exception(e)
else:
    st.info("Enter some data to generate a QR code.")
