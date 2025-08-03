import streamlit as st
import requests
import json
from base64 import b64encode


# Convert to cURL
def build_curl(method, url, headers, body=None):
    curl = [f"curl -X {method} '{url}'"]
    for k, v in headers.items():
        curl.append(f"-H '{k}: {v}'")
    if body:
        if isinstance(body, dict):
            body_str = json.dumps(body)
        else:
            body_str = str(body)
        curl.append(f"--data '{body_str}'")
    return " \\\n  ".join(curl)


st.set_page_config(page_title="Advanced API Client", layout="wide")
st.title("🚀 Advanced API Client")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Left: Request setup
with st.sidebar:
    st.header("🔧 Request Settings")
    method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])
    url = st.text_input("Request URL", "https://jsonplaceholder.typicode.com/posts/1")

    # Auth section
    auth_type = st.selectbox(
        "Authentication", ["None", "Basic Auth", "Bearer Token", "API Key"]
    )

    headers = {}
    if auth_type == "Basic Auth":
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if user and pwd:
            token = b64encode(f"{user}:{pwd}".encode()).decode()
            headers["Authorization"] = f"Basic {token}"

    elif auth_type == "Bearer Token":
        token = st.text_input("Bearer Token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    elif auth_type == "API Key":
        key_name = st.text_input("Key Name")
        key_value = st.text_input("Key Value")
        key_location = st.radio("Key Location", ["Header", "Query"])
        if key_name and key_value:
            if key_location == "Header":
                headers[key_name] = key_value
            else:
                url += f"{'&' if '?' in url else '?'}{key_name}={key_value}"

    # Custom headers input
    headers_input = st.text_area(
        "Extra Headers (JSON)", value='{\n  "Content-Type": "application/json"\n}'
    )
    try:
        extra_headers = json.loads(headers_input)
        headers.update(extra_headers)
    except:
        st.error("Invalid headers JSON")

    # Body options
    body_mode = st.selectbox(
        "Request Body Type", ["None", "JSON", "Raw", "Form-data", "File Upload"]
    )
    body = None
    files = None

    if method in ["POST", "PUT", "PATCH"]:
        if body_mode == "JSON":
            json_input = st.text_area("JSON Body", height=200)
            try:
                body = json.loads(json_input) if json_input else None
            except:
                st.error("Invalid JSON")

        elif body_mode == "Raw":
            raw_input = st.text_area("Raw Body", height=200)
            body = raw_input

        elif body_mode == "Form-data":
            st.markdown("Enter key-value form fields:")
            form_data = {}
            for i in range(3):  # Add more if you want
                k = st.text_input(f"Key {i+1}", key=f"form_k_{i}")
                v = st.text_input(f"Value {i+1}", key=f"form_v_{i}")
                if k:
                    form_data[k] = v
            body = form_data

        elif body_mode == "File Upload":
            upload_file = st.file_uploader("Upload File")
            if upload_file:
                files = {"file": (upload_file.name, upload_file.getvalue())}

    send = st.button("📨 Send Request")

# Send request
if send:
    try:
        with st.spinner("Sending..."):
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=body if body_mode == "JSON" else None,
                data=body if body_mode in ["Raw", "Form-data"] else None,
                files=files,
            )
            response.raise_for_status()

        # Save to history
        st.session_state.history.insert(
            0, {"method": method, "url": url, "status": response.status_code}
        )

        st.success("✅ Request successful")
        st.subheader("📬 Response")
        st.code(f"{response.status_code} {response.reason}", language="http")

        with st.expander("Response Headers"):
            st.json(dict(response.headers))

        with st.expander("Response Body"):
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                try:
                    st.json(response.json())
                except:
                    st.text(response.text)
            else:
                st.text(response.text)
        with st.expander("💻 cURL Command"):
            st.code(build_curl(method, url, headers, body), language="bash")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error: {e}")

# History
st.markdown("## 🕘 Request History")
for item in st.session_state.history[:10]:
    st.markdown(f"- `{item['method']}` [**{item['url']}**] → `{item['status']}`")

st.caption("🛠️ Built with Streamlit + Requests — by you 🚀")
