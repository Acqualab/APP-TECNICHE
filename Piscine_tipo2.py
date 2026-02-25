import streamlit as st
import math

# --- CONFIGURAZIONE FISSA ---
st.set_page_config(page_title="UNI 10637:2024 Pro", layout="wide")

def suggerisci_pvc(d_interno):
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno
    return "N/A"

# --- 1. GEOMETRIA E PORTATE (LAYOUT APPROVATO) ---
with st.sidebar:
    st.header("📋 Parametri di Progetto")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    st.divider()
    v_sabbia = st.slider("Velocità Filtro Sabbia (m/h)", 20, 50, 30)
    cap_bocchetta = st.number_input("Portata Bocchetta (m³/h)", value=6.0)

# Calcolo Portata (Prospetto 3)
q_tot = 0
for i in range(int(L/0.1)):
    h_c = h_min + (i * 0.1 * (h_max - h_min) / L)
    t = 3.0 if h_c > 1.35 else (2.5 if h_c > 0.6 else (1.0 if h_c > 0.4 else 0.5))
    q_tot += ((0.1 * W) * h_c) / t

# --- 2. LOCALE TECNICO (CORREZIONE NORMA CARTUCCIA) ---
st.header("🏗️ Locale Tecnico e Filtrazione")
tipo_f = st.radio("Scegli tecnologia di filtrazione:", ["Sabbia", "Cartuccia"], horizontal=True)

f1, f2 = st.columns(2)
with f1:
    if tipo_f == "Cartuccia":
        v_effettiva = 1.0 # VINCOLO NORMATIVO UNI 10637
        sup_f = q_tot / v_effettiva
        st.warning(f"**Norma UNI 10637:** Velocità fissata a {v_effettiva} m/h per cartuccia.")
        st.metric("Superficie Cartuccia Necessaria", f"{sup_f:.2f} m²")
    else:
        v_effettiva = v_sabbia
        sup_f = q_tot / v_effettiva
        diam_f = math.sqrt(sup_f / math.pi) * 2000
        st.metric("Superficie Sabbia Necessaria", f"{sup_f:.2f} m²")
        st.info(f"Ø Filtro consigliato: **{diam_f:.0f} mm**")

with f2:
    st.metric("Portata di Progetto (Q)", f"{q_tot:.2f} m³/h")
    st.write(f"Velocità filtrazione applicata: **{v_effettiva} m/h**")

# --- 3. COLLETTORI E TABELLA (LAYOUT APPROVATO) ---
st.divider()
st.subheader("🏛️ Dimensionamento Collettori e Stacchi")

d_coll_asp = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.0)/math.pi)*2000)
d_coll_man = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.5)/math.pi)*2000)

st.table({
    "Tratto": ["Collettore Aspirazione", "Collettore Mandata"],
    "Portata (m³/h)": [q_tot, q_tot],
    "Diametro PVC consigliato": [f"Ø {d_coll_asp}", f"Ø {d_coll_man}"],
    "Velocità (m/s)": [1.0, 1.5]
})
