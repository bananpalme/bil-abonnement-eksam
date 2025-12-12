import streamlit as st
import requests
import os

API = os.environ.get("API_GATEWAY_URL", "http://localhost:5000/api")

if st.session_state.role not in ["dataregistry", "admin"]:
    st.error("You are not authorized to view this page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}
resp_clients = requests.get(f"{API}/client", headers=headers)

if resp_clients.status_code == 200:
    clients = resp_clients.json()
    client_map = {f"{c['first_name']} {c['last_name']}": c['id'] for c in clients}
else:
    st.error("Failed to load clients")


resp_cars = requests.get(f"{API}/cars", headers=headers)
if resp_cars.status_code == 200:
    cars = resp_cars.json()
    car_map = {f"{c['make']} {c['model']} ({c['year']})": c['id'] for c in cars}
else:
    st.error("Failed to load cars")


if client_map and car_map:
    st.subheader("Create Rental Contract")

    with st.form("rental_form"):
        selected_client_name = st.selectbox("Select client", list(client_map.keys()))
        selected_client_id = client_map[selected_client_name]

        selected_car_name = st.selectbox("Select car", list(car_map.keys()))
        selected_car_id = car_map[selected_car_name]

        months = st.number_input("Months")
        monthly_rate = st.number_input("Monthly rate")

        total_cost = months * monthly_rate
    
        submitted = st.form_submit_button("Create Rental Contract")

        if submitted:
            contract = {
            "client_id": selected_client_id,
            "car_id": selected_car_id,
            "months": months,
            "monthly_rate": monthly_rate,
            "total_cost": total_cost
            }

            resp = requests.post(f"{API}/contract", headers=headers, json=contract)
            if resp.status_code == 201:
                st.success("Rental contract created!")
            else:
                st.error(resp.json().get("message", "Error creating contract"))

resp_contracts = requests.get(f"{API}/contract", headers=headers)

if resp_contracts.status_code == 200:
    contracts = resp_contracts.json()
    st.table(contracts)
else:
    st.error("Failed to load clients")