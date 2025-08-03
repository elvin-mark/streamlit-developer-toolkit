import streamlit as st

st.title("Welcome!")
st.markdown("A collection of useful developer tools built with Streamlit.")

st.header("🛠️ Tools")

tool_list = [
    ("API Client", "Test your APIs with support for different authentication methods."),
    ("Base64 Tool", "Encode and decode Base64 strings."),
    ("Bcrypt Hasher", "Hash and verify passwords using Bcrypt."),
    ("Color Picker", "Pick colors and get their HEX, RGB, and HSL values."),
    ("DB Explorer", "Explore PostgreSQL databases."),
    ("CRON Generator", "Generate and evaluate CRON expressions."),
    ("Highlight Diff", "Compare two texts and highlight their differences."),
    ("Image Converter & Optimizer", "Convert and optimize images."),
    ("JSON Visualizer", "Visualize JSON data in a tree format."),
    ("JWT Decoder", "Decode JSON Web Tokens."),
    ("Packet Sniffer", "Analyze PCAP files."),
    ("QR Code Generator", "Generate QR codes from text."),
    ("Regex Tester", "Test regular expressions."),
    ("UUID Generator", "Generate UUIDs in different versions."),
    (
        "Timestamp Converter",
        "Convert between Unix timestamps and human-readable dates.",
    ),
    ("YAML-JSON Converter", "Convert between YAML and JSON formats."),
]

cols = st.columns(3)
for i, (name, description) in enumerate(tool_list):
    with cols[i % 3]:
        st.subheader(name)
        st.write(description)
        st.link_button("Go to tool", f"/{name.replace(' ', '_')}")


st.markdown("---")
st.markdown(
    """
## 🚀 Getting Started

1.  **Install dependencies:** `pip install -r requirements.txt`
2.  **Run the app:** `streamlit run Home.py`
"""
)
