import streamlit as st
import requests

API_GATEWAY_URL = "http://localhost:5000/api"

def get_clients():
    response = requests.get(f"{API_GATEWAY_URL}/client")
    response.raise_for_status()
    return response.json()

def get_cars():
    response = requests.get(f"{API_GATEWAY_URL}/cars")
    response.raise_for_status()
    return response.json()

def get_contracts():
    response = requests.get(f"{API_GATEWAY_URL}/contract")
    response.raise_for_status()
    return response.json()

st.title("Rental Service Dashboard")

st.header("Clients")
clients = get_clients()

if clients:
    st.table(clients)
else:
    st.write("No clients found or API unreachable.")

st.header("Cars")
cars = get_cars()

if cars:
    st.table(cars)
else:
    st.write("No cars found or API unreachable.")

st.header("Contracts")
contracts = get_contracts()

if contracts:
    st.table(contracts)
else:
    st.write("No contracts found or API unreachable")