import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Regex Tester", layout="wide")

st.title("🔍 Regex Tester")

with st.sidebar:
    st.header("Regex Settings")

    pattern = st.text_input("Regex Pattern", r"\b\w+\b")
    replacement = st.text_input("Substitution (optional)", "")
    flags = 0
    if st.checkbox("Ignore Case (re.IGNORECASE)"):
        flags |= re.IGNORECASE
    if st.checkbox("Multiline (re.MULTILINE)"):
        flags |= re.MULTILINE
    if st.checkbox("Dot Matches Newline (re.DOTALL)"):
        flags |= re.DOTALL

    mode = st.radio("Match Mode", ["findall", "search", "sub"])

text_input = st.text_area("Input Text", "Paste your text here...\n", height=300)

# Process regex
matches = []
output = ""
error = None

try:
    regex = re.compile(pattern, flags)
    if mode == "findall":
        matches = list(regex.findall(text_input))
    elif mode == "search":
        match = regex.search(text_input)
        if match:
            matches = [match.group()] + list(match.groups())
    elif mode == "sub":
        output = regex.sub(replacement, text_input)
        matches = list(regex.findall(text_input))
except re.error as e:
    error = str(e)

# Show matches
st.subheader("🧪 Results")

if error:
    st.error(f"Regex Error: {error}")
elif mode == "sub":
    st.markdown("**🔁 Substitution Output:**")
    st.code(output)
    st.markdown("**🎯 Matches Before Substitution:**")
    st.write(matches)
else:
    st.markdown(f"**🔎 {len(matches)} Match(es) Found:**")
    st.write(matches)


# Highlight matches
def highlight_matches(text, regex, flags):
    try:
        compiled = re.compile(regex, flags)
        spans = list(compiled.finditer(text))
        highlighted = ""
        last_end = 0
        for match in spans:
            start, end = match.span()
            highlighted += text[last_end:start]
            highlighted += f"<mark>{text[start:end]}</mark>"
            last_end = end
        highlighted += text[last_end:]
        return highlighted
    except re.error:
        return text


st.markdown("**🖍️ Highlighted Text:**", unsafe_allow_html=True)
highlighted_html = highlight_matches(text_input, pattern, flags)
st.markdown(
    f"<div style='white-space: pre-wrap;'>{highlighted_html}</div>",
    unsafe_allow_html=True,
)

# Download matches
if matches:
    st.subheader("⬇️ Export")
    df = pd.DataFrame(
        matches,
        columns=(
            ["Match"]
            if isinstance(matches[0], str)
            else [f"Group {i}" for i in range(len(matches[0]))]
        ),
    )
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Matches as CSV", csv, "matches.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("Created with ❤️ using Streamlit and Python's re module")
