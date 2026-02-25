import streamlit as st
import math
import matplotlib.pyplot as plt

# Funzione per mappare il diametro commerciale PVC (Approssimativo PN10)
def suggerisci_pvc(d_interno):
    tabella_pvc = {
        32: 28, 40: 36, 50: 45, 63: 57, 
        75: 69, 90: 82, 110: 100, 125: 114, 
        140: 127, 160: 146, 200: 184
    }
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno:
            return esterno, interno
    return "Fuori scala", d_interno

st.set_page_config(page_title="Progetto Professionale UNI 10637", layout="wide")

st.title("🛠️ Suite Professionale Progettazione Piscine")
st.subheader("Calcolo Avanzato Condotte e Componenti - UNI 10637:2024")

# --- SIDEBAR ---
with st.sidebar:
    st.header("📋 Dati di Progetto")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    
    st.divider()
    st.header("🌊 Limiti Idraulici")
    v_asp_lim = 1.7  # m/s (Tua specifica)
    v_man_lim = 2.5  # m/s (Tua specifica)
    cap_bocchetta = st.number_input("Portata Bocchetta (m³/h)", value=6.0)

# --- CALCOLO PORTATA (PROSPETTO 3) ---
superficie_tot = L * W
pendenza = (h_max - h_min) / L
q_tot = 0
passo = 0.05

for i in range(int(L/passo)):
    h_c = h_min + (i * passo * pendenza)
    t = 3.0 if h_c > 1.35 else (2.5 if h_c > 0.6 else (1.0 if h_c > 0.4 else 0.5))
    q_tot += ((passo * W) * h_c) / t

# --- COMPONENTI ---
if superficie_tot <= 100:
    n_skimmer = math.ceil(superficie_tot / 20)
    q_stacco_asp = q_tot / n_skimmer
else:
    n_skimmer = 0 # Obbligo Sfioro
    q_stacco_asp = 0

n_bocchette = math.ceil(q_tot / cap_bocchetta)
q_stacco_man = q_tot / n_bocchette

# --- LOGICA DIAMETRI ---
def calcola_e_mappa(q, v_lim):
    if q <= 0: return 0, 0
    d_int = math.sqrt(((q/3600)/v_lim)/math.pi) * 2 * 1000
    return suggerisci_pvc(d_int)

# 1. Collettori (Velocità ridotta per efficienza)
est_coll_asp, int_coll_asp = calcola_e_mappa(q_tot, 1.2)
est_coll_man, int_coll_man = calcola_e_mappa(q_tot, 1.8)

# 2. Stacchi (Tue specifiche)
est_stacco_asp, int_stacco_asp = calcola_e_mappa(q_stacco_asp, v_asp_lim)
est_stacco_man, int_stacco_man = calcola_e_mappa(q_stacco_man, v_man_lim)

# --- DISPLAY ---
st.info(f"### 📊 Riepilogo Idraulico Generale (Q = {q_tot:.2f} m³/h)")
col1, col2 = st.columns(2)

with col1:
    st.write("#### 📥 Aspirazione")
    st.write(f"**Collettore Centrale:** Ø Est. {est_coll_asp} mm (Int. {int_coll_asp} mm)")
    if n_skimmer > 0:
        st.write(f"**Stacco Skimmer (x{n_skimmer}):** Ø Est. {est_stacco_asp} mm")
    else:
        st.error("SISTEMA A SFIORO OBBLIGATORIO")

with col2:
    st.write("#### 📤 Mandata")
    st.write(f"**Collettore Centrale:** Ø Est. {est_coll_man} mm (Int. {int_coll_man} mm)")
    st.write(f"**Stacco Bocchetta (x{n_bocchette}):** Ø Est. {est_stacco_man} mm")



# --- TABELLA TECNICA ---
st.divider()
st.subheader("📋 Tabella Riassuntiva per Relazione Tecnica")
dati_tabella = {
    "Elemento": ["Collettore Aspirazione", "Collettore Mandata", "Stacco Skimmer", "Stacco Bocchetta"],
    "Portata (m3/h)": [q_tot, q_tot, q_stacco_asp, q_stacco_man],
    "Velocità (m/s)": [1.2, 1.8, v_asp_lim, v_man_lim],
    "Tubo PVC consigliato (Ø)": [est_coll_asp, est_coll_man, est_stacco_asp, est_stacco_man]
}
st.table(dati_tabella)
