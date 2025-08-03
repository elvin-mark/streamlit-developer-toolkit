import streamlit as st
from scapy.all import rdpcap, TCP, UDP, IP
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Advanced Packet Sniffer & Analyzer", layout="wide")
st.title(
    "📡 Advanced Packet Sniffer & Analyzer (Offline) with Filters & Packet Inspector"
)

uploaded_file = st.file_uploader("Upload a PCAP file", type=["pcap", "pcapng"])

if uploaded_file:
    try:
        packets = rdpcap(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read PCAP file: {e}")
        st.stop()

    st.success(f"Loaded {len(packets)} packets")

    # Extract packet info
    protocols = []
    src_ips = []
    dst_ips = []
    src_ports = []
    dst_ports = []
    lengths = []
    timestamps = []
    packet_numbers = []

    for i, pkt in enumerate(packets):
        packet_numbers.append(i + 1)  # 1-based index

        # Protocol
        if pkt.haslayer(TCP):
            protocols.append("TCP")
        elif pkt.haslayer(UDP):
            protocols.append("UDP")
        elif pkt.haslayer("ICMP"):
            protocols.append("ICMP")
        else:
            protocols.append("Other")

        # IP addresses
        if pkt.haslayer(IP):
            src_ips.append(pkt[IP].src)
            dst_ips.append(pkt[IP].dst)
        else:
            src_ips.append("N/A")
            dst_ips.append("N/A")

        # Ports (TCP/UDP)
        if pkt.haslayer(TCP) or pkt.haslayer(UDP):
            sport = pkt.sport if hasattr(pkt, "sport") else None
            dport = pkt.dport if hasattr(pkt, "dport") else None
            src_ports.append(sport if sport is not None else "N/A")
            dst_ports.append(dport if dport is not None else "N/A")
        else:
            src_ports.append("N/A")
            dst_ports.append("N/A")

        # Length
        lengths.append(len(pkt))

        # Timestamp (if present)
        try:
            ts = datetime.fromtimestamp(pkt.time)
        except Exception:
            ts = None
        timestamps.append(ts)

    df = pd.DataFrame(
        {
            "Packet #": packet_numbers,
            "Protocol": protocols,
            "Source IP": src_ips,
            "Destination IP": dst_ips,
            "Source Port": src_ports,
            "Destination Port": dst_ports,
            "Length": lengths,
            "Timestamp": timestamps,
        }
    )

    st.sidebar.header("Filters")

    # Protocol filter
    protocol_options = df["Protocol"].unique().tolist()
    selected_protocols = st.sidebar.multiselect(
        "Select Protocol(s):", options=protocol_options, default=protocol_options
    )

    # Source IP filter
    selected_src_ip = st.sidebar.text_input("Filter by Source IP (partial)")

    # Destination IP filter
    selected_dst_ip = st.sidebar.text_input("Filter by Destination IP (partial)")

    # Source Port filter
    selected_src_port = st.sidebar.text_input(
        "Filter by Source Port (exact or partial)"
    )

    # Destination Port filter
    selected_dst_port = st.sidebar.text_input(
        "Filter by Destination Port (exact or partial)"
    )

    # Packet Length range filter
    min_len, max_len = int(df["Length"].min()), int(df["Length"].max())
    selected_length_range = st.sidebar.slider(
        "Packet Length Range (bytes):",
        min_value=min_len,
        max_value=max_len,
        value=(min_len, max_len),
    )

    # Packet Number range filter
    min_pkt, max_pkt = int(df["Packet #"].min()), int(df["Packet #"].max())
    selected_pkt_range = st.sidebar.slider(
        "Packet Number Range:",
        min_value=min_pkt,
        max_value=max_pkt,
        value=(min_pkt, max_pkt),
    )

    # Timestamp filter
    min_ts = df["Timestamp"].min()
    max_ts = df["Timestamp"].max()

    if min_ts and max_ts and not pd.isna(min_ts) and not pd.isna(max_ts):
        selected_ts_range = st.sidebar.date_input(
            "Filter by Timestamp Range:",
            value=(min_ts.date(), max_ts.date()),
            min_value=min_ts.date(),
            max_value=max_ts.date(),
        )
    else:
        selected_ts_range = None

    # Reset filters button
    if st.sidebar.button("Reset Filters"):
        selected_protocols = protocol_options
        selected_src_ip = ""
        selected_dst_ip = ""
        selected_src_port = ""
        selected_dst_port = ""
        selected_length_range = (min_len, max_len)
        selected_pkt_range = (min_pkt, max_pkt)
        selected_ts_range = (
            (min_ts.date(), max_ts.date()) if min_ts and max_ts else None
        )

    # Apply filters
    filtered_df = df[
        (df["Protocol"].isin(selected_protocols))
        & (df["Length"] >= selected_length_range[0])
        & (df["Length"] <= selected_length_range[1])
        & (df["Packet #"] >= selected_pkt_range[0])
        & (df["Packet #"] <= selected_pkt_range[1])
    ]

    if selected_src_ip:
        filtered_df = filtered_df[
            filtered_df["Source IP"].str.contains(selected_src_ip, case=False, na=False)
        ]

    if selected_dst_ip:
        filtered_df = filtered_df[
            filtered_df["Destination IP"].str.contains(
                selected_dst_ip, case=False, na=False
            )
        ]

    if selected_src_port:
        filtered_df = filtered_df[
            filtered_df["Source Port"]
            .astype(str)
            .str.contains(selected_src_port, case=False, na=False)
        ]

    if selected_dst_port:
        filtered_df = filtered_df[
            filtered_df["Destination Port"]
            .astype(str)
            .str.contains(selected_dst_port, case=False, na=False)
        ]

    if selected_ts_range and not pd.isna(min_ts) and not pd.isna(max_ts):
        start_date = pd.to_datetime(selected_ts_range[0])
        end_date = (
            pd.to_datetime(selected_ts_range[1])
            + pd.Timedelta(days=1)
            - pd.Timedelta(seconds=1)
        )
        filtered_df = filtered_df[
            (filtered_df["Timestamp"] >= start_date)
            & (filtered_df["Timestamp"] <= end_date)
        ]

    st.subheader(f"Filtered Packets: {len(filtered_df)}")

    # Protocol distribution chart
    protocol_counts = filtered_df["Protocol"].value_counts()
    st.bar_chart(protocol_counts)

    # Top Source IPs
    top_src = filtered_df["Source IP"].value_counts().head(10)
    st.subheader("Top 10 Source IPs (Filtered)")
    st.table(top_src)

    # Packet length distribution
    st.subheader("Packet Length Distribution (Filtered)")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["Length"], bins=30, color="skyblue", edgecolor="black")
    ax.set_xlabel("Packet Length (bytes)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Show packet timestamps summary
    if filtered_df["Timestamp"].notnull().any():
        st.subheader("Timestamp Range of Filtered Packets")
        st.write(
            f"From {filtered_df['Timestamp'].min()} to {filtered_df['Timestamp'].max()}"
        )

    # Filtered packet raw data preview
    st.subheader("Filtered Raw Packet Data (first 20 rows)")
    st.dataframe(filtered_df.head(20))

    # --- New packet inspector ---

    st.subheader("🔎 Inspect a Specific Packet")

    packet_selection = st.selectbox(
        "Select Packet # to Inspect", options=filtered_df["Packet #"].tolist()
    )

    if packet_selection:
        pkt_idx = packet_selection - 1  # zero-based index in packets list
        packet = packets[pkt_idx]

        st.markdown("**Packet Summary:**")
        st.text(packet.summary())

        st.markdown("**Packet Detailed Info:**")
        # Using scapy show() which returns a string when passing _=None
        pkt_details = packet.show(dump=True)
        st.text(pkt_details)

        st.markdown("**Raw Bytes (Hex):**")
        raw_bytes = bytes(packet)
        hex_string = raw_bytes.hex()
        # Format hex string as spaced pairs (e.g., "af 3d 12 ...")
        spaced_hex = " ".join(
            hex_string[i : i + 2] for i in range(0, len(hex_string), 2)
        )
        st.code(spaced_hex, language="plaintext")

else:
    st.info("Upload a PCAP file to analyze network traffic offline.")
