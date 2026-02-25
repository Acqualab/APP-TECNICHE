import streamlit as st
import math

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="UNI 10637:2024 Pro", layout="wide")

def suggerisci_pvc(d_interno):
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno
    return "N/D"

# --- SIDEBAR INPUT ---
with st.sidebar:
    st.header("📋 Dati Vasca")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    st.divider()
    v_sabbia = st.slider("Velocità Filtro Sabbia (m/h)", 20, 50, 30)
    cap_bocchetta = st.number_input("Portata Bocchetta (m³/h)", value=6.0)

# --- LOGICA ANALITICA (PROSPETTO 3) ---
passo = 0.01  # Analisi ogni centimetro per massima precisione professionale
q_tot = 0
vol_tot = 0
q_zone = {"C (>1.35m)": 0, "D (0.6-1.35m)": 0, "E (0.4-0.6m)": 0, "F (<0.4m)": 0}

for i in range(int(L/passo)):
    # Calcolo profondità puntuale
    h_c = h_min + (i * passo * (h_max - h_min) / L)
    v_segmento = (passo * W) * h_c
    vol_tot += v_segmento
    
    # Assegnazione tempo di ricircolo e calcolo portata locale
    if h_c > 1.35:
        t, zona = 3.0, "C (>1.35m)"
    elif h_c > 0.6:
        t, zona = 2.5, "D (0.6-1.35m)"
    elif h_c > 0.4:
        t, zona = 1.0, "E (0.4-0.6m)"
    else:
        t, zona = 0.5, "F (<0.4m)"
    
    portata_segmento = v_segmento / t
    q_tot += portata_segmento
    q_zone[zona] += portata_segmento

# --- DISPLAY RISULTATI GENERALI ---
st.header("📊 Analisi Volumetrica e Portate Differenziate")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Volume Totale Vasca", f"{vol_tot:.2f} m³")
with c2:
    st.metric("Portata di Progetto Totale (Q)", f"{q_tot:.2f} m³/h")
with c3:
    st.metric("Superficie Specchio d'Acqua", f"{L*W:.2f} m²")

st.write("#### Suddivisione Portate per Zona (Prospetto 3):")
st.table([{"Zona": k, "Portata Associata (m³/h)": f"{v:.2f}"} for k, v in q_zone.items() if v > 0])

# --- LOCALE TECNICO ---
st.divider()
st.subheader("🏗️ Filtrazione")
tipo_f = st.radio("Tecnologia:", ["Sabbia", "Cartuccia"], horizontal=True)
v_eff = 1.0 if tipo_f == "Cartuccia" else v_sabbia
sup_f = q_tot / v_eff

col_f1, col_f2 = st.columns(2)
with col_f1:
    st.metric(f"Superficie Filtrante ({tipo_f})", f"{sup_f:.2f} m²")
    if tipo_f == "Sabbia":
        st.info(f"Ø Filtro consigliato: {math.sqrt(sup_f/math.pi)*2000:.0f} mm")
    else:
        st.warning("Velocità vincolata a 1 m/h (UNI 10637)")

# --- IDRAULICA (COLLETTORI E STACCHI) ---
st.divider()
st.subheader("🏛️ Dimensionamento Condotte PVC")

# Calcolo Diametri
d_coll_asp = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.0)/math.pi)*2000)
d_coll_man = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.5)/math.pi)*2000)

n_boc = math.ceil(q_tot / cap_bocchetta)
d_boc = suggerisci_pvc(math.sqrt((( (q_tot/n_boc) /3600)/2.5)/math.pi)*2000)

st.table({
    "Componente": ["Collettore Aspirazione", "Collettore Mandata", "Stacchi Bocchette (n."+str(n_boc)+")", "Stacchi Fondo (n.2)"],
    "Portata Totale (m³/h)": [q_tot, q_tot, q_tot, q_tot],
    "Velocità Limite (m/s)": [1.0, 1.5, 2.5, 1.7],
    "Diametro Esterno Consigliato": [f"Ø {d_coll_asp}", f"Ø {d_coll_man}", f"Ø {d_boc}", "Vedi calcolo stacco"]
})
