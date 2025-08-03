import streamlit as st
import datetime

st.set_page_config(page_title="CRON Generator & Evaluator", layout="wide")

st.title("🕒 CRON Expression Generator & Evaluator (No Dependencies)")

st.markdown("Create a CRON expression and evaluate its next run time.")


# --- Local CRON evaluator ---
def parse_cron_field(field, min_value, max_value):
    if field == "*":
        return set(range(min_value, max_value + 1))
    values = set()
    for part in field.split(","):
        if "/" in part:
            base, step = part.split("/")
            step = int(step)
            if base == "*":
                values.update(range(min_value, max_value + 1, step))
            elif "-" in base:
                start, end = map(int, base.split("-"))
                values.update(range(start, end + 1, step))
        elif "-" in part:
            start, end = map(int, part.split("-"))
            values.update(range(start, end + 1))
        else:
            values.add(int(part))
    return values


def next_cron_time(expr: str, from_time=None):
    if from_time is None:
        from_time = datetime.datetime.now().replace(
            second=0, microsecond=0
        ) + datetime.timedelta(minutes=1)

    try:
        minute, hour, day, month, weekday = expr.strip().split()
        mins = parse_cron_field(minute, 0, 59)
        hrs = parse_cron_field(hour, 0, 23)
        days = parse_cron_field(day, 1, 31)
        months = parse_cron_field(month, 1, 12)
        weekdays = parse_cron_field(weekday, 0, 6)  # Monday=0

        max_search = 365 * 2 * 24 * 60  # 2 years of minutes
        for _ in range(max_search):
            if (
                from_time.minute in mins
                and from_time.hour in hrs
                and from_time.day in days
                and from_time.month in months
                and from_time.weekday() in weekdays
            ):
                return from_time
            from_time += datetime.timedelta(minutes=1)
        return None
    except Exception as e:
        return f"Error parsing: {e}"


# --- UI: CRON Builder ---
st.subheader("Build CRON Expression")

col1, col2, col3 = st.columns(3)

with col1:
    minute = st.text_input("Minute (0-59)", "*")
    hour = st.text_input("Hour (0-23)", "*")

with col2:
    day = st.text_input("Day of Month (1-31)", "*")
    month = st.text_input("Month (1-12)", "*")

with col3:
    weekday = st.text_input("Day of Week (0-6, 0=Monday)", "*")

cron_expr = f"{minute} {hour} {day} {month} {weekday}"

st.code(cron_expr, language="bash")

# --- Evaluation ---
st.subheader("Next Execution Time")

# from_time = st.datetime_input("Start from (optional)", value=datetime.datetime.now())
selected_date = st.date_input("Choose a date")
selected_time = st.time_input("Choose a time")
from_time = datetime.datetime.combine(selected_date, selected_time)

if st.button("Evaluate Next Time"):
    next_time = next_cron_time(cron_expr, from_time)
    if isinstance(next_time, datetime.datetime):
        st.success(f"✅ Next run time: {next_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.error(f"❌ {next_time}")

# --- Extra Features ---
st.markdown("---")
st.subheader("📘 CRON Field Reference")

with st.expander("Click to view field meanings"):
    st.markdown(
        """
- **Minute**: `0-59`
- **Hour**: `0-23`
- **Day of Month**: `1-31`
- **Month**: `1-12`
- **Day of Week**: `0-6` (0 = Monday, 6 = Sunday)

You can use:
- `*` — Every value
- `*/5` — Every 5 units
- `1,15,30` — Specific values
- `5-10` — Range of values
"""
    )

# --- Footer ---
st.markdown("Built with ❤️ using Streamlit — no external libraries.")
