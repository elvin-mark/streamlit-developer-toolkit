import streamlit as st
import difflib
import html

st.set_page_config(page_title="📝 Text/Code Diff Tool", layout="wide")
st.title("📝 Text / Code Diff Tool")

st.markdown(
    """
Compare two text or code blocks side-by-side and highlight differences.
Useful for comparing configs, code versions, JSON files, etc.
"""
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Text")
    text1 = st.text_area("Paste or write the original text/code here:", height=300)

with col2:
    st.subheader("Modified Text")
    text2 = st.text_area("Paste or write the modified text/code here:", height=300)


def highlight_diff(text1, text2):
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    result_lines = []
    for line in diff:
        if line.startswith("- "):
            # Removed lines with stronger red background and darker text
            escaped = html.escape(line[2:])
            result_lines.append(
                f'<div style="background:#ff4d4d; color:#330000; padding: 2px 4px;">- {escaped}</div>'
            )
        elif line.startswith("+ "):
            # Added lines with stronger green background and darker text
            escaped = html.escape(line[2:])
            result_lines.append(
                f'<div style="background:#4dff4d; color:#003300; padding: 2px 4px;">+ {escaped}</div>'
            )
        elif line.startswith("? "):
            # Skip diff hint lines
            continue
        else:
            # Unchanged lines with normal background
            escaped = html.escape(line[2:] if line.startswith("  ") else line)
            result_lines.append(f'<div style="padding: 2px 4px;">{escaped}</div>')
    return "\n".join(result_lines)


if st.button("Show Diff"):
    if not text1.strip() or not text2.strip():
        st.warning("Please provide text in both input boxes.")
    else:
        st.subheader("Diff Result")
        diff_html = highlight_diff(text1, text2)
        st.markdown(diff_html, unsafe_allow_html=True)
