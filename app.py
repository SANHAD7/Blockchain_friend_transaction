import streamlit as st
from blockchain import Blockchain
import plotly.express as px
import pandas as pd

# --------------------------
# Custom CSS for Styling
# --------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #f1c40f;
    }
    .card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #ecf0f1;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .block-hash {
        font-size: 0.8em;
        color: #bdc3c7;
        word-wrap: break-word;
    }
    /* Fix input labels visibility */
    label, .stTextInput label, .stNumberInput label {
        color: #f1c40f !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    /* Input fields */
    .stTextInput input, .stNumberInput input {
        color: #2c3e50 !important;
        background-color: #ecf0f1 !important;
        border-radius: 10px;
        padding: 8px;
    }
    /* Stylish button */
    div.stForm button {
        background: linear-gradient(135deg, #f39c12, #d35400);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: 0.3s;
    }
    div.stForm button:hover {
        background: linear-gradient(135deg, #f1c40f, #e67e22);
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Initialize Blockchain
# --------------------------
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# --------------------------
# Hero Section
# --------------------------
st.markdown("<h1 style='text-align:center;'>🔐 Friend Transaction Blockchain</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#bdc3c7;'>A futuristic way to keep your transactions immutable & secure</p>", unsafe_allow_html=True)

# --------------------------
# Sidebar Navigation
# --------------------------
page = st.sidebar.radio("📍 Navigate", ["➕ Add Transaction", "📜 Blockchain Ledger", "📊 Analytics"])

# --------------------------
# Add Transaction Page
# --------------------------
if page == "➕ Add Transaction":
    st.subheader("📤 Add a New Transaction")
    with st.form("transaction_form", clear_on_submit=True):
        sender = st.text_input("👤 Sender Name")
        receiver = st.text_input("👤 Receiver Name")
        amount = st.number_input("💰 Amount (₹)", min_value=0.01, step=0.01)
        submit = st.form_submit_button("🚀 Add Transaction")

        if submit:
            if sender and receiver and amount > 0:
                blockchain.add_block(sender, receiver, amount)
                st.success(f"✅ {sender} sent ₹{amount:.2f} to {receiver}")
            else:
                st.error("⚠️ Please fill all fields properly.")

    # Show Blockchain Stats in cards
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-card'>🧱 Blocks<br>{len(blockchain.chain)}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'>✅ Chain Valid<br>{'Yes' if blockchain.is_chain_valid() else 'No'}</div>", unsafe_allow_html=True)
    total_tx = sum([b.amount for b in blockchain.chain[1:]])
    col3.markdown(f"<div class='metric-card'>💰 Total Tx Value<br>₹{total_tx:.2f}</div>", unsafe_allow_html=True)

# --------------------------
# Blockchain Ledger Page
# --------------------------
elif page == "📜 Blockchain Ledger":
    st.subheader("🧾 Blockchain Ledger")
    for block in reversed(blockchain.chain):
        st.markdown(
            f"""
            <div class='card'>
                <h4>🧱 Block {block.index}</h4>
                <p><b>⏱ Timestamp:</b> {block.timestamp}</p>
                <p><b>👤 Sender:</b> {block.sender}</p>
                <p><b>👤 Receiver:</b> {block.receiver}</p>
                <p><b>💰 Amount:</b> ₹ {block.amount}</p>
                <p class='block-hash'><b>🔗 Hash:</b> {block.hash}</p>
                <p class='block-hash'><b>⛓ Prev Hash:</b> {block.previous_hash}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------
# Analytics Page
# --------------------------
elif page == "📊 Analytics":
    st.subheader("📈 Transaction Analytics")

    if len(blockchain.chain) > 1:
        data = {
            "Sender": [b.sender for b in blockchain.chain[1:]],
            "Receiver": [b.receiver for b in blockchain.chain[1:]],
            "Amount": [b.amount for b in blockchain.chain[1:]],
            "Timestamp": [b.timestamp for b in blockchain.chain[1:]],
        }
        df = pd.DataFrame(data)

        # Show table
        st.dataframe(df)

        # Plotly bar chart
        fig = px.bar(df, x="Sender", y="Amount", color="Receiver",
                     title="💸 Transactions Between Friends",
                     text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No transactions yet. Add some first! 🚀")
