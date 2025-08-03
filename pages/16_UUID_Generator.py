import streamlit as st
import uuid

st.set_page_config(page_title="UUID Generator", layout="centered")

st.title("🔑 UUID Generator")
st.write(
    "Generate Universally Unique Identifiers (UUIDs) in different versions (v1, v3, v4, v5)."
)

uuid_version = st.selectbox("Select UUID version", ["v1", "v3", "v4", "v5"])

num_uuids = st.slider(
    "How many UUIDs to generate?", min_value=1, max_value=100, value=1
)

namespace_input = None
name_input = None
namespace_options = {
    "DNS": uuid.NAMESPACE_DNS,
    "URL": uuid.NAMESPACE_URL,
    "OID": uuid.NAMESPACE_OID,
    "X500": uuid.NAMESPACE_X500,
}

if uuid_version in ["v3", "v5"]:
    selected_namespace = st.selectbox(
        "Select namespace", list(namespace_options.keys())
    )
    namespace_input = namespace_options[selected_namespace]
    name_input = st.text_input("Enter name (e.g. domain, path)", value="example.com")

if st.button("Generate UUIDs"):
    generated_uuids = []
    for _ in range(num_uuids):
        if uuid_version == "v1":
            generated_uuids.append(str(uuid.uuid1()))
        elif uuid_version == "v3":
            generated_uuids.append(str(uuid.uuid3(namespace_input, name_input)))
        elif uuid_version == "v4":
            generated_uuids.append(str(uuid.uuid4()))
        elif uuid_version == "v5":
            generated_uuids.append(str(uuid.uuid5(namespace_input, name_input)))

    st.success(
        f"✅ Generated {len(generated_uuids)} UUID{'s' if len(generated_uuids) > 1 else ''}:"
    )
    for i, u in enumerate(generated_uuids, 1):
        st.code(u, language="text")

    st.download_button(
        "📄 Download as .txt",
        data="\n".join(generated_uuids),
        file_name="uuids.txt",
        mime="text/plain",
    )
