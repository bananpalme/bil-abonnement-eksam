import streamlit as st
import requests
import os


API = os.environ.get("API_GATEWAY_URL", "http://localhost:5000/api")

# session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

st.title("Company Dashboard")


# authentication functions
def do_login(username, password):
    resp = requests.post(f"{API}/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        data = resp.json()
        token = data.get("access_token")
        role = data.get("role")
        st.session_state.token = token
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = role
        st.success("Logged in")

def do_logout():
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.role = None

def register(username, password, role):
    response = requests.post(f"{API}/profile", json={"username": username, "password": password, "role": role})
    if response.status_code == 201:
        st.success("Sucessfully registered")
    else:
        try:
            msg = response.json().get("message", "Registration failed")
        except ValueError:
            msg = response.text or "Registration failed"
        st.error(msg)

# ui
if not st.session_state.logged_in:
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        do_login(u, p)

    st.subheader("Register")
    make_username = st.text_input("Create username")
    make_password = st.text_input("Create Password", type="password")
    role = st.selectbox("Choose role", ("dataregistry", "damages", "admin"),)
    if st.button("Register"):
        register(make_username, make_password, role)

else:
    st.sidebar.write(f"User: {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        do_logout()

    st.title("Home")
    st.write("Use the sidebar to navigate through your allowed pages.")
