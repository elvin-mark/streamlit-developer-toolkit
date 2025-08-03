import streamlit as st
import time
from datetime import datetime, timezone
import pytz

st.set_page_config(page_title="🕒 Timestamp Converter", layout="centered")

st.title("🕒 Unix Timestamp ↔ Date Converter")

st.markdown(
    "This tool converts between Unix timestamps and human-readable dates (both UTC and Local)."
)

# Show current timestamp
st.header("📍 Current Time")
col1, col2 = st.columns(2)
with col1:
    now = datetime.now(timezone.utc)
    st.metric("Current Timestamp (UTC)", int(now.timestamp()))
with col2:
    st.metric("Current Time (UTC)", now.strftime("%Y-%m-%d %H:%M:%S"))

st.divider()

# Convert timestamp to date
st.header("⬅️ Convert Timestamp → Human-readable Date")

timestamp_input = st.text_input(
    "Enter Unix Timestamp (seconds):", placeholder="e.g., 1672531200"
)
if timestamp_input:
    try:
        ts_int = int(timestamp_input)
        dt_utc = datetime.fromtimestamp(ts_int, timezone.utc)
        dt_local = dt_utc.astimezone()

        st.success("✅ Conversion successful:")
        st.write(
            f"**UTC:** {dt_utc.strftime('%Y-%m-%d %H:%M:%S')}  \n"
            f"**Local Timezone ({dt_local.tzinfo}):** {dt_local.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    except Exception as e:
        st.error(f"Invalid timestamp: {e}")

st.divider()

# Convert date to timestamp
st.header("➡️ Convert Date → Unix Timestamp")

col1, col2 = st.columns(2)
with col1:
    date_input = st.date_input("Pick a date")
with col2:
    time_input = st.time_input("Pick a time")

dt_combined = datetime.combine(date_input, time_input)
dt_utc = dt_combined.astimezone(timezone.utc)
timestamp = int(dt_utc.timestamp())

st.success("✅ Unix Timestamp:")
st.code(f"{timestamp} (UTC)", language="text")

# Optional: Timezone conversion
st.divider()
st.subheader("🌍 Optional Timezone Info")

selected_tz = st.selectbox(
    "Select a timezone:", pytz.all_timezones, index=pytz.all_timezones.index("UTC")
)
localized = dt_combined.astimezone(pytz.timezone(selected_tz))
st.write(f"**{selected_tz} Time:** {localized.strftime('%Y-%m-%d %H:%M:%S')}")
st.write(f"**Unix Timestamp in {selected_tz}:** `{int(localized.timestamp())}`")

st.info("🔁 All conversions are based on seconds (not milliseconds).")
