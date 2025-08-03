import streamlit as st
import json
import yaml

st.set_page_config(page_title="YAML ↔ JSON Converter", layout="wide")
st.title("🔄 YAML ↔ JSON Converter")

st.markdown(
    """
Convert between **YAML** and **JSON** formats easily.
- Paste your YAML or JSON text below.
- Select conversion direction.
- See the output instantly.
"""
)

# Sidebar: choose conversion direction
conversion_direction = st.sidebar.selectbox(
    "Select Conversion Direction",
    options=["JSON → YAML", "YAML → JSON"],
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    input_text = st.text_area(
        label="Paste your input text here",
        height=400,
        placeholder="Paste valid JSON or YAML here depending on the direction...",
    )

with col2:
    st.subheader("Output")
    output_text = ""

    if input_text.strip():
        try:
            if conversion_direction == "JSON → YAML":
                # Parse JSON first
                parsed = json.loads(input_text)
                # Convert to YAML (safe_dump)
                output_text = yaml.safe_dump(parsed, sort_keys=False, indent=2)
            else:  # YAML → JSON
                # Parse YAML first
                parsed = yaml.safe_load(input_text)
                # Convert to JSON (pretty printed)
                output_text = json.dumps(parsed, indent=2)
        except Exception as e:
            output_text = f"❌ Error:\n{e}"

    st.text_area(
        label="Converted output",
        value=output_text,
        height=400,
        disabled=False,
    )
