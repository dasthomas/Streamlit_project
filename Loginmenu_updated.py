import streamlit as st
import json
import hashlib
import os
from datetime import datetime
import pandas as pd
import plotly.express as px

USER_FILE = "users.json"

# Get current theme preference from Streamlit config
try:
    theme = st.config.get_option("theme.base")
except:
    theme = "light"

# Add theme-aware styling for light and dark modes
if theme == "dark":
    # Dark theme styles
    st.markdown("""
        <style>
        /* Dark Theme Configuration */
        .stApp {
            background-color: #0e1117 !important;
            color: #e6edf3 !important;
        }
        
        body {
            background-color: #0e1117 !important;
            color: #e6edf3 !important;
        }
        
        /* Login title - light text for dark background */
        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: #e6edf3 !important;
        }
        
        /* Negative balance - red text visible on dark background */
        .negative-balance {
            color: #ff6b6b !important;
            font-weight: bold;
            font-size: 1.2em;
            background-color: rgba(255, 107, 107, 0.1) !important;
            padding: 10px;
            border-radius: 5px;
        }
        
        /* Input fields and text areas */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            background-color: #21262d !important;
            color: #e6edf3 !important;
            border: 1px solid #30363d !important;
        }
        
        /* Subheader styling */
        h2, h3 {
            color: #e6edf3 !important;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #238636 !important;
            color: #ffffff !important;
        }
        
        .stButton button:hover {
            background-color: #2ea043 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    # Light theme styles
    st.markdown("""
        <style>
        /* Light Theme Configuration */
        .stApp {
            background-color: #ffffff !important;
            color: #1f2937 !important;
        }
        
        body {
            background-color: #ffffff !important;
            color: #1f2937 !important;
        }
        
        /* Login title - dark text for light background */
        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: #1f2937 !important;
        }
        
        /* Negative balance - red text visible on light background */
        .negative-balance {
            color: #dc3545 !important;
            font-weight: bold;
            font-size: 1.2em;
            background-color: rgba(220, 53, 69, 0.1) !important;
            padding: 10px;
            border-radius: 5px;
        }
        
        /* Input fields and text areas */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            background-color: #f3f4f6 !important;
            color: #1f2937 !important;
            border: 1px solid #d1d5db !important;
        }
        
        /* Subheader styling */
        h2, h3 {
            color: #1f2937 !important;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #0066cc !important;
            color: #ffffff !important;
        }
        
        .stButton button:hover {
            background-color: #0052a3 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Page navigation state
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

users = {}
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        try:
            users = json.load(f)
        except Exception:
            users = {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# Use a large money emoji for universal compatibility
st.markdown("<div style='font-size:60px;text-align:center;'>💰</div>", unsafe_allow_html=True)
st.markdown('<div class="login-title">Expense Tracker</div>', unsafe_allow_html=True)

if st.session_state["page"] == "login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")
    register_btn = st.button("Register New User")
    forgot_btn = st.button("Forgot Password")

    if login_btn:
        if username in users and users[username]["password"] == hash_password(password):
            st.session_state["logged_in_user"] = username
            st.session_state["page"] = "dashboard"
            st.rerun()
        else:
            st.error("Invalid username or password.")
    if register_btn:
        st.session_state["page"] = "register"
        st.rerun()
    if forgot_btn:
        st.session_state["page"] = "forgot"
        st.rerun()

elif st.session_state["page"] == "register":
    st.subheader("Register New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    do_register = st.button("Register")
    back_btn = st.button("Back to Login")
    if do_register:
        if not new_username or not new_password or not confirm_password:
            st.error("Please fill all fields.")
        elif new_username in users:
            st.error("Username already exists.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            users[new_username] = {
                "password": hash_password(new_password),
                "balance": 0.0,
                "money_added": [],
                "expenses": []
            }
            save_users(users)
            st.success("User registered successfully!")
    if back_btn:
        st.session_state["page"] = "login"
        st.rerun()

elif st.session_state["page"] == "forgot":
    st.subheader("Forgot Password")
    fp_username = st.text_input("Username for Password Reset")
    fp_new_password = st.text_input("New Password", type="password")
    fp_confirm_password = st.text_input("Confirm New Password", type="password")
    do_reset = st.button("Reset Password")
    back_btn = st.button("Back to Login")
    if do_reset:
        if fp_username not in users:
            st.error("Username not found.")
        elif not fp_new_password or not fp_confirm_password:
            st.error("Please fill all fields.")
        elif fp_new_password != fp_confirm_password:
            st.error("Passwords do not match.")
        else:
            users[fp_username]["password"] = hash_password(fp_new_password)
            save_users(users)
            st.success("Password reset successfully!")
    if back_btn:
        st.session_state["page"] = "login"
        st.rerun()

elif st.session_state["page"] == "dashboard":
    current_user = st.session_state.get("logged_in_user")
    if not current_user or current_user not in users:
        st.error("User not found. Please log in again.")
        st.session_state["page"] = "login"
        st.rerun()
    
    # Logout button at top
    if st.button("Logout"):
        st.session_state["logged_in_user"] = None
        st.session_state["page"] = "login"
        st.rerun()
    
    st.subheader(f"Welcome, {current_user}!")
    
    # Show total balance
    balance = users[current_user].get("balance", 0.0)
    
    # Show balance with proper styling for both themes
    if balance < 0:
        st.markdown(f"<div class='negative-balance'>Total Account Balance: ₹{balance:.2f}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='balance-display' style='color: var(--text-color, inherit);'>Total Account Balance: <span style='color: #28a745;'>₹{balance:.2f}</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Add money to account - ONLY FOR YESUDAS
    if current_user == "yesudas":
        st.subheader("Add Money to Account")
        
        # Dropdown to select who is adding money
        payer_name = st.selectbox(
            "Select Name (Who is adding money)",
            ["Dass", "Elizabeth", "Ellen","Sonny Sonnet","Helen","Edil","Nancy Margaret","Arul","Minisha","Saison","Joy","Shoban","Trinity","Sharmila","Harini","Nancy","Abi","Cristilla","Jenifer","Stephen","Ebineser","John Charles","Princy","Wilson"]
        )
        
        money_description = st.text_input("Description (e.g., Salary, Gift, Bonus)")
        
        col1, col2 = st.columns(2)
        with col1:
            add_amount = st.number_input("Amount to Add (₹)", min_value=0.0, format="%.2f")
        with col2:
            add_btn = st.button("Add Money")
        
        if add_btn and add_amount > 0:
            users[current_user]["balance"] = users[current_user].get("balance", 0.0) + add_amount
            if "money_added" not in users[current_user]:
                users[current_user]["money_added"] = []
            users[current_user]["money_added"].append({
                "from_user": payer_name,
                "amount": add_amount,
                "description": money_description,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_users(users)
            st.success(f"Added ₹{add_amount:.2f} from {payer_name} to your account!")
            st.rerun()
        
        st.markdown("---")
        
        # Show money added history with filter
        st.subheader("Money Added History")
        money_added = users[current_user].get("money_added", [])
        if money_added:
            df_money = pd.DataFrame(money_added)
            
            # Filter by name
            filter_name = st.selectbox(
                "Filter by Name",
                ["All"] + list(df_money["from_user"].unique())
            )
            
            if filter_name != "All":
                df_money_filtered = df_money[df_money["from_user"] == filter_name]
            else:
                df_money_filtered = df_money
            
            st.dataframe(df_money_filtered, use_container_width=True)
        else:
            st.info("No money added yet.")
        
        st.markdown("---")
        
        # Add expenses - ONLY FOR YESUDAS
        st.subheader("Add Expense")
        expense_category = st.selectbox(
            "Category",
            ["Food", "Transportation", "Housing", "Utilities", "Entertainment", "Shopping", "Medical", "Investment", "Others"]
        )
        expense_amount = st.number_input("Expense Amount (₹)", min_value=0.0, format="%.2f")
        expense_description = st.text_input("Description")
        add_expense_btn = st.button("Add Expense")
        
        if add_expense_btn and expense_amount > 0:
            if users[current_user].get("balance", 0) < expense_amount:
                st.error("Insufficient balance! Your balance will go negative.")
                # Still add the expense with negative balance
                users[current_user]["balance"] -= expense_amount
                if "expenses" not in users[current_user]:
                    users[current_user]["expenses"] = []
                users[current_user]["expenses"].append({
                    "category": expense_category,
                    "amount": expense_amount,
                    "description": expense_description,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                save_users(users)
                st.markdown(f"<div class='negative-balance'>Expense of ₹{expense_amount:.2f} added! Your balance is now ₹{users[current_user]['balance']:.2f}</div>", unsafe_allow_html=True)
                st.rerun()
            else:
                users[current_user]["balance"] -= expense_amount
                if "expenses" not in users[current_user]:
                    users[current_user]["expenses"] = []
                users[current_user]["expenses"].append({
                    "category": expense_category,
                    "amount": expense_amount,
                    "description": expense_description,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                save_users(users)
                st.success(f"Expense of ₹{expense_amount:.2f} added!")
                st.rerun()
        
        st.markdown("---")
        
        # Show expenses with filters
        st.subheader("Your Expenses")
        expenses = users[current_user].get("expenses", [])
        if expenses:
            df_expenses = pd.DataFrame(expenses)
            df_expenses["date"] = pd.to_datetime(df_expenses["date"])
            
            # Extract month and year
            df_expenses["month_year"] = df_expenses["date"].dt.strftime("%Y-%m")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_category = st.selectbox(
                    "Filter by Category",
                    ["All"] + list(df_expenses["category"].unique())
                )
            with col2:
                filter_month = st.selectbox(
                    "Filter by Month",
                    ["All"] + sorted(df_expenses["month_year"].unique(), reverse=True)
                )
            
            # Apply filters
            df_filtered = df_expenses
            if filter_category != "All":
                df_filtered = df_filtered[df_filtered["category"] == filter_category]
            if filter_month != "All":
                df_filtered = df_filtered[df_filtered["month_year"] == filter_month]
            
            st.dataframe(df_filtered, use_container_width=True)
            
            # Show pie chart by category
            if len(df_filtered) > 0:
                st.subheader("Expense Distribution by Category")
                category_totals = df_filtered.groupby("category")["amount"].sum()
                fig_pie = px.pie(
                    values=category_totals.values,
                    names=category_totals.index,
                    title="Expense Distribution by Category"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Show bar chart by month
            if len(df_expenses) > 0:
                st.subheader("Monthly Expense Trend")
                monthly_totals = df_expenses.groupby("month_year")["amount"].sum().reset_index()
                fig_bar = px.bar(
                    monthly_totals,
                    x="month_year",
                    y="amount",
                    title="Monthly Expenses",
                    labels={"month_year": "Month", "amount": "Amount (₹)"}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No expenses added yet.")
    else:
        st.info(f"📖 Read-Only Mode - Viewing Yesudas's Account | Logged in as: {current_user}")
        
        st.markdown("---")
        
        # Display Yesudas's balance (read-only for other users)
        yesudas_balance = users.get("yesudas", {}).get("balance", 0.0)
        if yesudas_balance < 0:
            st.markdown(f"<div class='negative-balance'>Yesudas's Account Balance: ₹{yesudas_balance:.2f}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='balance-display' style='color: var(--text-color, inherit);'>Yesudas's Account Balance: <span style='color: #28a745;'>₹{yesudas_balance:.2f}</span></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display Yesudas's money added (read-only)
        st.subheader("Money Added History (Yesudas)")
        yesudas_money = users.get("yesudas", {}).get("money_added", [])
        if yesudas_money:
            df_money = pd.DataFrame(yesudas_money)
            
            # Filter by name
            filter_name = st.selectbox(
                "Filter by Name",
                ["All"] + list(df_money["from_user"].unique())
            )
            
            if filter_name != "All":
                df_money_filtered = df_money[df_money["from_user"] == filter_name]
            else:
                df_money_filtered = df_money
            
            st.dataframe(df_money_filtered, use_container_width=True)
        else:
            st.info("No money records available.")
        
        st.markdown("---")
        
        # Display Yesudas's expenses (read-only)
        st.subheader("Expense Records (Yesudas)")
        yesudas_expenses = users.get("yesudas", {}).get("expenses", [])
        if yesudas_expenses:
            df_expenses = pd.DataFrame(yesudas_expenses)
            df_expenses["date"] = pd.to_datetime(df_expenses["date"])
            
            # Extract month and year
            df_expenses["month_year"] = df_expenses["date"].dt.strftime("%Y-%m")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_category = st.selectbox(
                    "Filter by Category",
                    ["All"] + list(df_expenses["category"].unique())
                )
            with col2:
                filter_month = st.selectbox(
                    "Filter by Month",
                    ["All"] + sorted(df_expenses["month_year"].unique(), reverse=True)
                )
            
            # Apply filters
            df_filtered = df_expenses
            if filter_category != "All":
                df_filtered = df_filtered[df_filtered["category"] == filter_category]
            if filter_month != "All":
                df_filtered = df_filtered[df_filtered["month_year"] == filter_month]
            
            st.dataframe(df_filtered, use_container_width=True)
            
            # Show pie chart by category
            if len(df_filtered) > 0:
                st.subheader("Expense Distribution by Category (Yesudas)")
                category_totals = df_filtered.groupby("category")["amount"].sum()
                fig_pie = px.pie(
                    values=category_totals.values,
                    names=category_totals.index,
                    title="Expense Distribution by Category"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Show bar chart by month
            if len(df_expenses) > 0:
                st.subheader("Monthly Expense Trend (Yesudas)")
                monthly_totals = df_expenses.groupby("month_year")["amount"].sum().reset_index()
                fig_bar = px.bar(
                    monthly_totals,
                    x="month_year",
                    y="amount",
                    title="Monthly Expenses",
                    labels={"month_year": "Month", "amount": "Amount (₹)"}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No expense records available.")
