import streamlit as st
import math

# --- CONFIGURAZIONE FISSA ---
st.set_page_config(page_title="UNI 10637:2024 - Progetto Professionale", layout="wide")

def suggerisci_pvc(d_interno):
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno
    return "N/D"

# --- 1. INPUT DATI ---
with st.sidebar:
    st.header("📋 Dati Vasca")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    st.divider()
    st.header("⚙️ Parametri Impianto")
    v_sabbia = st.slider("Velocità Filtro Sabbia (m/h)", 20, 50, 30)
    cap_bocchetta = st.number_input("Portata Bocchetta (m³/h)", value=6.0)
    distanza_locale = st.number_input("Distanza Locale Tecnico (m)", value=10.0)

# --- 2. CALCOLO ANALITICO VOLUMI E PORTATE (PROSPETTO 3) ---
passo = 0.01 
q_tot, vol_tot = 0, 0
q_zone = {"C (>1.35m)": 0, "D (0.6-1.35m)": 0, "E (0.4-0.6m)": 0, "F (<0.4m)": 0}

for i in range(int(L/passo)):
    h_c = h_min + (i * passo * (h_max - h_min) / L)
    v_seg = (passo * W) * h_c
    vol_tot += v_seg
    # Assegnazione zone e tempi
    if h_c > 1.35: t, zona = 3.0, "C (>1.35m)"
    elif h_c > 0.6:  t, zona = 2.5, "D (0.6-1.35m)"
    elif h_c > 0.4:  t, zona = 1.0, "E (0.4-0.6m)"
    else:            t, zona = 0.5, "F (<0.4m)"
    q_seg = v_seg / t
    q_tot += q_seg
    q_zone[zona] += q_seg

# --- 3. DIMENSIONAMENTO POMPA E FILTRO ---
st.header("🏗️ Locale Tecnico: Filtrazione e Pompaggio")
tipo_f = st.radio("Tecnologia Filtro:", ["Sabbia", "Cartuccia"], horizontal=True)
v_eff = 1.0 if tipo_f == "Cartuccia" else v_sabbia
sup_f = q_tot / v_eff

# Calcolo Prevalenza Stimata (Perdite carico tubi + filtro + accessori)
# Semplificazione professionale: 8m (filtro sporco) + 0.1m per ogni metro di distanza
prevalenza_stima = 8 + (distanza_locale * 2 * 0.1) 

c_tec1, c_tec2 = st.columns(2)
with c_tec1:
    st.subheader("🔍 Filtro")
    st.metric("Superficie Filtrante", f"{sup_f:.2f} m²")
    if tipo_f == "Sabbia":
        st.info(f"Ø Filtro consigliato: {math.sqrt(sup_f/math.pi)*2000:.0f} mm")
    else:
        st.warning("Velocità vincolata a 1.0 m/h (UNI 10637)")

with c_tec2:
    st.subheader("⚙️ Pompa")
    st.metric("Portata di Esercizio", f"{q_tot:.2f} m³/h")
    st.metric("Prevalenza stimata", f"{prevalenza_stima:.1f} m.c.a.")
    st.caption(f"Selezionare pompa con punto di lavoro: {q_tot:.1f} m³/h @ {math.ceil(prevalenza_stima)} m")

# --- 4. IDRAULICA (COLLETTORI E STACCHI) ---
st.divider()
st.subheader("🏛️ Riepilogo Idraulico e Volumi")
res1, res2 = st.columns([1, 2])

with res1:
    st.write("**Dati Volumetrici**")
    st.write(f"Volume Totale: **{vol_tot:.2f} m³**")
    st.write(f"Superficie: **{L*W:.2f} m²**")
    st.write("**Ripartizione Portate:**")
    for z, q in q_zone.items():
        if q > 0: st.write(f"- {z}: {q:.2f} m³/h")

with res2:
    # Calcolo Diametri
    d_coll_asp = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.0)/math.pi)*2000)
    d_coll_man = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.5)/math.pi)*2000)
    n_boc = math.ceil(q_tot / cap_bocchetta)
    d_boc = suggerisci_pvc(math.sqrt((((q_tot/n_boc)/3600)/2.5)/math.pi)*2000)
    
    st.write("**Dimensionamento Tubazioni PVC PN10**")
    st.table({
        "Tratto": ["Collettore Aspirazione", "Collettore Mandata", f"Stacchi Bocchette (n.{n_boc})", "Stacchi Fondo (n.2)"],
        "Portata (m³/h)": [q_tot, q_tot, q_tot/n_boc, q_tot/2],
        "Ø Esterno": [f"Ø {d_coll_asp}", f"Ø {d_coll_man}", f"Ø {d_boc}", f"Ø {suggerisci_pvc(math.sqrt(((q_tot/2/3600)/1.7)/math.pi)*2000)}"]
    })
