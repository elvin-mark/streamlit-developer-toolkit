import streamlit as st
from PIL import Image, ImageOps
import io

st.set_page_config(page_title="Image Converter & Optimizer", layout="centered")

st.title("🖼️ Image Converter & Optimizer")
st.write(
    "Upload an image and convert it between formats (PNG, JPG, WebP). Optionally reduce file size."
)

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    # Load and show original image
    image = ImageOps.exif_transpose(Image.open(uploaded_file))
    st.image(image, caption="Original Image", use_column_width=True)

    # Select output format
    st.subheader("🛠️ Conversion Settings")
    output_format = st.selectbox("Convert to format", ["JPEG", "PNG", "WEBP"])

    # Optimization level
    quality = st.slider("Quality (higher = better, larger file)", 10, 100, 80)

    # Convert and optimize
    if st.button("Convert and Optimize"):
        buffer = io.BytesIO()

        save_kwargs = {"quality": quality}
        if output_format == "JPEG":
            save_kwargs["optimize"] = True
            save_kwargs["format"] = "JPEG"
            image = image.convert("RGB")  # JPEG doesn't support alpha
        elif output_format == "PNG":
            save_kwargs["optimize"] = True
            save_kwargs["format"] = "PNG"
        elif output_format == "WEBP":
            save_kwargs["format"] = "WEBP"

        image.save(buffer, **save_kwargs)
        buffer.seek(0)

        # Show download
        st.success(f"Image converted to {output_format}!")
        st.download_button(
            label="⬇️ Download Optimized Image",
            data=buffer,
            file_name=f"converted_image.{output_format.lower()}",
            mime=f"image/{output_format.lower()}",
        )

        # Show optimized image size
        size_kb = len(buffer.getvalue()) / 1024
        st.info(f"📦 Final file size: {size_kb:.2f} KB")
