import streamlit as st
import webbrowser
import os
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("User already exists!")
    conn.close()

# Pages
def login_page():
    st.markdown("<h1 style='font-size:36px; color:purple;'><center>LOGIN</center></h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_user(username, password):
            st.markdown("<p style='color:purple;'>Logged in successfully!</p>", unsafe_allow_html=True)
            st.session_state.authenticated = True
            st.session_state.username = username
        else:
            st.markdown("<p style='color:red;'>Incorrect username or password</p>", unsafe_allow_html=True)

def logout_page():
    st.markdown("<h1 style='font-size:36px; color:purple;'><center>LOGOUT</center></h1>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.success("Logged out successfully!")

def register_page():
    st.markdown("<h1 style='font-size:36px; color:purple;'><center>REGISTER</center></h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            add_user(username, password)
            st.success("User registered successfully!")
        else:
            st.error("Please fill in all fields")

def dashboard_page():
    st.markdown("<h1 style='font-size:36px; color:purple;'><center>India City GDP Power BI Dashboard</center></h1>", unsafe_allow_html=True)
    # Show the button only after the user is logged in
    if st.button("Open Dashboard"):
        # Construct the absolute path to the PBIX file
        pbix_path = os.path.abspath("C:\\Users\\sbhav\\OneDrive\\Documents\\Infosys Intern.pbix")
        # Generate the Power BI service URL (replace with your actual service URL)
        power_bi_service_url = "https://app.powerbi.com/groups/me/reports/58207bd6-9877-4b96-85f8-c796c9927357/ReportSection83e2ca78d5c79d93bfa1?experience=power-bi"
        webbrowser.open(power_bi_service_url)

# Main logic
init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

menu = ["Register", "Login", "Dashboard", "Logout"]
choice = st.sidebar.radio("MENU", menu)

if choice == "Login":
    if not st.session_state.authenticated:
          login_page()
    else:
        st.success(f"You are already logged in as {st.session_state.username}")
elif choice == "Register":
    register_page()
elif choice == "Dashboard":
    if st.session_state.authenticated:
        dashboard_page()  # Show the dashboard only if authenticated
    else:
        st.warning("Please log in to access the dashboard")
elif choice == "Logout":
    if st.session_state.authenticated:
        logout_page()
    else:
        st.warning("You are not logged in")
