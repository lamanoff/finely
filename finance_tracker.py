import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File to store data
DATA_FILE = 'finance_data.csv'

# Load data
def load_data():
    try:
        return pd.read_csv(DATA_FILE, parse_dates=['date'])
    except FileNotFoundError:
        return pd.DataFrame(columns=['date', 'category', 'amount', 'type'])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load existing data
df = load_data()

st.title("💸 Financial Tracker")

# --- New entry form ---
st.header("Add Transaction")

with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        entry_type = st.selectbox("Type", ["Income", "Expense"])
        category = st.text_input("Category", placeholder="e.g. food, salary, rent")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        date = st.date_input("Date", value=datetime.today())
    
    submitted = st.form_submit_button("Add")
    if submitted:
        new_row = {
            "date": pd.to_datetime(date),
            "category": category.strip().capitalize(),
            "amount": amount,
            "type": entry_type
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Transaction added!")

# --- Display transactions ---
st.header("📊 Transaction History")

if not df.empty:
    df_sorted = df.sort_values("date", ascending=False)
    st.dataframe(df_sorted, use_container_width=True)

    # Summary stats
    income = df[df["type"] == "Income"]["amount"].sum()
    expense = df[df["type"] == "Expense"]["amount"].sum()
    balance = income - expense

    st.subheader("💡 Summary")
    st.metric("Total Income", f"{income:.2f} ₽")
    st.metric("Total Expenses", f"{expense:.2f} ₽")
    st.metric("Balance", f"{balance:.2f} ₽", delta_color="inverse")

    # --- Expense chart by category ---
    st.subheader("📉 Expenses by Category")

    expense_by_cat = df[df["type"] == "Expense"].groupby("category")["amount"].sum()
    if not expense_by_cat.empty:
        fig, ax = plt.subplots()
        expense_by_cat.plot(kind="bar", ax=ax)
        ax.set_ylabel("Amount (₽)")
        ax.set_xlabel("Category")
        ax.set_title("Expenses by Category")
        st.pyplot(fig)
else:
    st.info("No data yet. Add your first transaction above.")
