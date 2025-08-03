import streamlit as st
import pandas as pd
import psycopg2

# --- Sidebar: Database Connection ---
st.sidebar.header("PostgreSQL Connection")

host = st.sidebar.text_input("Host", value="localhost")
port = st.sidebar.text_input("Port", value="5432")
dbname = st.sidebar.text_input("Database Name", value="your_database")
user = st.sidebar.text_input("User", value="your_user")
password = st.sidebar.text_input("Password", type="password")

# --- Connect Button ---
if st.sidebar.button("Connect"):
    try:
        conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        st.success("Connected to PostgreSQL database!")
        st.session_state.conn = conn
        st.session_state.query_history = []  # initialize history
    except Exception as e:
        st.error(f"Connection failed: {e}")

# --- Check for connection ---
conn = st.session_state.get("conn", None)
if not conn:
    st.warning("Please connect to the database from the sidebar.")
    st.stop()

# --- Display Tables ---
st.sidebar.subheader("📋 Tables in Database")


def get_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name;
        """
        )
        return cur.fetchall()


def describe_table(conn, schema, table):
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position;
        """,
            (schema, table),
        )
        return cur.fetchall()


tables = get_tables(conn)
table_names = [f"{schema}.{table}" for schema, table in tables]
selected_table = st.sidebar.selectbox("Select a table to describe:", table_names)

if selected_table:
    schema, table = selected_table.split(".")
    columns_info = describe_table(conn, schema, table)
    st.subheader(f"🧾 Table Schema: `{selected_table}`")
    st.table(pd.DataFrame(columns_info, columns=["Column", "Type", "Nullable"]))


# --- Query Input ---
st.header("💬 SQL Query Executor")
query = st.text_area("Enter your SQL query:", height=150)

if st.button("Execute Query"):
    try:
        df = pd.read_sql_query(query, conn)
        st.success("Query executed successfully!")
        st.dataframe(df, use_container_width=True)

        # Save to history
        if "query_history" not in st.session_state:
            st.session_state.query_history = []
        st.session_state.query_history.insert(0, query)  # most recent first
        st.session_state.query_history = st.session_state.query_history[
            :10
        ]  # limit to last 10

        # --- Download as CSV ---
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV", csv, file_name="query_result.csv", mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error executing query: {e}")

# --- Query History ---
if "query_history" in st.session_state and st.session_state.query_history:
    st.subheader("🕘 Query History")
    for i, past_query in enumerate(st.session_state.query_history):
        with st.expander(f"Query #{i+1}", expanded=False):
            st.code(past_query, language="sql")
            if st.button(f"Rerun Query #{i+1}", key=f"rerun_{i}"):
                try:
                    df = pd.read_sql_query(past_query, conn)
                    st.success(f"Query #{i+1} executed successfully!")
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        f"Download CSV #{i+1}",
                        csv,
                        file_name=f"query_result_{i+1}.csv",
                        mime="text/csv",
                    )
                except Exception as e:
                    st.error(f"Error executing Query #{i+1}: {e}")
