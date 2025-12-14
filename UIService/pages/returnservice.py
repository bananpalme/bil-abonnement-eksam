import streamlit as st
import requests
import pandas as pd
import json
import os # Importér os

# Henter URL fra Docker Compose miljøvariablen
# Hvis variablen ikke findes (lokal kørsel), bruges fallback (hvilket burde være api_gateway:5000 i Docker)
# Vi sætter den nu til at hente fra miljøvariabel
API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL", "http://127.0.0.1:5000") 

st.set_page_config(layout="wide", page_title="Bilabonnement - Intern Håndtering")
st.title("Intern Håndtering af Bilaflevering 🚗")

# --- Tabs for Adskilte Funktioner ---
tab1, tab2 = st.tabs(["Kunde Aflevering (Log)", 
                      "Medarbejder Håndtering (Bekræft Nøgle)"])

# ***********************************
# Tab 1: Log Aflevering i Nøgleboks (Kunde-flow)
# ***********************************
# ***********************************
# Tab 1: Log Aflevering i Nøgleboks (Kunde-flow)
# ***********************************
with tab1:
    st.header("Log Aflevering i Nøgleboks")
    
    # --- START FORM ---
    with st.form(key='aflevering_form'):
        
        # Inputfelter flyttes ind i formularen
        lp = st.text_input("Nummerplade:", key="lp_return_input")
        ci = st.text_input("Kontrakt ID:", key="ci_return_input")
        
        # Knappen skal også være inde i formularen
        submit_button = st.form_submit_button(label='Log Aflevering')
    # --- SLUT FORM ---

    customer_token = "SIMULERET_CUSTOMER_JWT_TOKEN" 

    # Udfør handlingen kun HVIS formularen er blevet submit'et
    if submit_button:
        # Nu valideres input EFTER trykket er registreret
        if lp and ci:
            try:
                # Kald til endpoint for at logge nøgleaflevering
                response = requests.post(
                    f"{API_GATEWAY_URL}/return/log",
                    json={"license_plate": lp, "contract_id": ci},
                    headers={"Authorization": f"Bearer {customer_token}"} 
                )
                
                if response.status_code == 201:
                    st.success(f"Aflevering logget for {lp}. Status: Nøgle venter på afhentning.")
                    st.balloons()
                else:
                    # Forbedret fejlhåndtering, som du selv har tilføjet
                    try:
                        err_msg = response.json().get('error', 'Ukendt fejl')
                    except Exception:
                        err_msg = response.text[:200] if response.text else 'Ukendt fejl'
                    st.error(f"Fejl ved logging: {response.status_code} - {err_msg}")
            
            except requests.exceptions.ConnectionError:
                st.error("Kunne ikke oprette forbindelse til Flask Backend. Er app.py aktiv?")
        else:
            # Denne warning vises kun, hvis felterne er tomme ved submit
            st.warning("Udfyld venligst både Nummerplade og Kontrakt ID.")

# ***********************************
# Tab 2: Bekræft Nøgleafhentning (Medarbejder-flow)
# ***********************************
with tab2:
    st.header("Medarbejder Bekræftelse af Nøgle")
    st.markdown("Medarbejderen bekræfter, at nøglen er hentet, og systemet sender besked til kunden.")
    
    lp_pickup = st.text_input("Nummerplade (Afhentning):", key="lp_pickup_input")
    employee_id = st.text_input("Medarbejder ID (Dataregistrering):", key="employee_id_input")

    if st.button("Bekræft Nøgleafhentning"):
        if lp_pickup and employee_id:
            try:
                # Kald til endpoint for nøgleafhentning
                response = requests.post(
                    f"{API_GATEWAY_URL}/return/key_pickup",
                    json={"license_plate": lp_pickup, "employee_id": employee_id},
                    # Antager, at medarbejderen har et gyldigt JWT i headeren
                    headers={"Authorization": "Bearer SIMULERET_STAFF_JWT"} 
                )

                if response.status_code == 200:
                    st.success(f"Nøgle til {lp_pickup} bekræftet af Medarbejder {employee_id}. Kunden er notificeret.")
                elif response.status_code == 404:
                    st.error("Fejl: Ingen aktiv aflevering fundet for denne nummerplade.")
                else:
                    st.error(f"Fejl ved afhentning: {response.status_code} - {response.json().get('error', 'Ukendt fejl')}")

            except requests.exceptions.ConnectionError:
                st.error("Kunne ikke oprette forbindelse til Flask Backend.")
        else:
            st.warning("Udfyld venligst Nummerplade og Medarbejder ID.")