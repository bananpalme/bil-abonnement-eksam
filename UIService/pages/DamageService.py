import streamlit as st
import requests
import os

API = os.environ.get("API_GATEWAY_URL", "http://localhost:5000/api")

if st.session_state.role not in ["damages", "admin"]:
    st.error("You are not authorized to view this page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}
response = requests.get(f"{API}/damage-types")
if response.status_code in (200, 201):
    damages = response.json()
    damage_map = {f"{d['name']} (${d['base_cost']})": d['id'] for d in damages}
else:
    st.error(f"Failed to load damage types: {response.status_code}")

resp_cars = requests.get(f"{API}/cars", headers=headers)
if resp_cars.status_code in (200, 201):
    cars = resp_cars.json()
    car_map = {f"{c['make']} {c['model']} ({c['year']})": c['id'] for c in cars}
    # Reverse map for looking up car name by id (derived from car_map)
    id_to_car = {v: k for k, v in car_map.items()}
else:
    st.error("Failed to load cars")
    car_map = {}
    id_to_car = {}


st.header("Report Damages for a Car")
with st.form("damage_form"):
    selected_car_name = st.selectbox("Select Car", list(car_map.keys()))
    car_id = car_map[selected_car_name]
    selected_damages = st.multiselect(
        "Select Damages",
        list(damage_map.keys())
    )
    submitted = st.form_submit_button("Submit Damages")

    if submitted:
        if not selected_damages:
            st.warning("Please select at least one damage type.")
        else:
            payload = []
            for dmg in selected_damages:
                dmg_id = damage_map[dmg]
                base_cost = next(d['base_cost'] for d in damages if d['id'] == dmg_id)
                payload.append({
                    "car_id": car_id,
                    "damage_type_id": dmg_id,
                    "cost_at_time": base_cost
                })
            
            # Send POST request
            
            resp = requests.post(f"{API}/car-damages", json=payload,headers=headers )
            if resp.status_code in (200, 201):
                car_display = id_to_car.get(car_id, f"Car ID {car_id}")
                st.success(f"Damages for {car_display} submitted successfully!")
            else:
                st.error(f"Failed to submit damages: {resp.text}")


st.header("Car Damage Overview")
resp_totals = requests.get(f"{API}/car-damages", headers=headers)
if resp_totals.status_code in (200, 201):
    totals = resp_totals.json()
    # Sort by car id (use numeric sort when possible)
    try:
        totals = sorted(totals, key=lambda c: int(c.get('car_id', 0)))
    except Exception:
        totals = sorted(totals, key=lambda c: str(c.get('car_id', '')))
    for car in totals:
        # Look up the car name from id_to_car (use make/model instead of id)
        car_name = id_to_car.get(car['car_id'], f"Car ID {car['car_id']}")
        st.subheader(f"{car_name}")
        st.write(f"**Total Damage Cost:** ${car['total_cost']}")
        for dmg in car['damages']:
            st.write(f"- {dmg['name']}: ${dmg['cost_at_time']}")