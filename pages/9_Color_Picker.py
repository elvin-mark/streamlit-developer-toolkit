import streamlit as st
import colorsys
import webcolors

st.set_page_config(page_title="🎨 Color Picker Tool")

st.title("🎨 Interactive Color Picker")

# Color picker widget
selected_color = st.color_picker("Pick a color:", "#00ffcc")


# Convert HEX to RGB
def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# Convert RGB to HSL
def rgb_to_hsl(r, g, b):
    # Normalize RGB to [0, 1]
    r /= 255
    g /= 255
    b /= 255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return int(h * 360), int(s * 100), int(l * 100)


# Get CSS name from RGB
def get_css_name(r, g, b):
    try:
        return webcolors.rgb_to_name((r, g, b))
    except ValueError:
        return "N/A"


# Parse color
rgb = hex_to_rgb(selected_color)
hsl = rgb_to_hsl(*rgb)
css_name = get_css_name(*rgb)

# Display
st.subheader("🧾 Color Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**HEX:** `{selected_color.upper()}`")
    st.markdown(f"**RGB:** `rgb{rgb}`")
    st.markdown(f"**HSL:** `hsl{hsl}`")
    st.markdown(f"**CSS Name:** `{css_name}`")

with col2:
    st.markdown("**Preview:**")
    st.markdown(
        f"<div style='width:100px;height:100px;border-radius:8px;background-color:{selected_color};border:1px solid #aaa;'></div>",
        unsafe_allow_html=True,
    )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
