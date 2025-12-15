import streamlit as st
import requests
from datetime import date
import os

API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL", "http://localhost:5000/api")

st.title("Inspection Service")

st.header("Create Inspection")

# --- Bilinformation ---
car_number = st.text_input("Car number")
car_model = st.text_input("Car model")

km_before = st.number_input("Kilometers before", min_value=0)
km_after = st.number_input("Kilometers after", min_value=0)

# --- Interiør check ---
st.subheader("Interior inspection")

seats_ok = st.checkbox("Seats OK")
steering_ok = st.checkbox("Steering OK")
carpet_ok = st.checkbox("Carpets OK")
belts_ok = st.checkbox("Seat belts OK")
gearbox_ok = st.checkbox("Gearbox OK")
smell_ok = st.checkbox("No bad smell")
warning_lights_ok = st.checkbox("No warning lights")

inspection_date = st.date_input("Inspection date", value=date.today())

# --- Send inspection ---
if st.button("Save inspection"):
    payload = {
        "car_number": car_number,
        "car_model": car_model,
        "km_before": km_before,
        "km_after": km_after,
        "seats_ok": seats_ok,
        "steering_ok": steering_ok,
        "carpet_ok": carpet_ok,
        "belts_ok": belts_ok,
        "gearbox_ok": gearbox_ok,
        "smell_ok": smell_ok,
        "warning_lights_ok": warning_lights_ok,
        "date": str(inspection_date)
    }

    response = requests.post(
        f"{API_GATEWAY_URL}/inspection", # <-- SLUTPUNKTET ER /inspection
        json=payload
    )

    if response.status_code == 201:
        st.success("Inspection saved successfully! if damage found, go to DamageService")
    else:
        st.error("Failed to save inspection")
