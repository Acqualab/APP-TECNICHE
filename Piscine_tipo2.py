import streamlit as st
import math
import matplotlib.pyplot as plt

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="UNI 10637:2024 Pro", layout="wide")

def suggerisci_pvc(d_interno):
    # Tabella commerciale PVC PN10 (Esterno: Interno)
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno
    return "N/A"

# --- SIDEBAR (INPUT) ---
with st.sidebar:
    st.header("📋 Parametri di Progetto")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    st.divider()
    v_filtrazione = st.slider("Velocità filtrazione (m/h)", 20, 50, 30)
    cap_bocchetta = st.number_input("Portata Bocchetta (m³/h)", value=6.0)

# --- CALCOLO PORTATA (PROSPETTO 3) ---
superficie_tot = L * W
q_tot = 0
passo = 0.1
for i in range(int(L/passo)):
    h_c = h_min + (i * passo * (h_max - h_min) / L)
    t = 3.0 if h_c > 1.35 else (2.5 if h_c > 0.6 else (1.0 if h_c > 0.4 else 0.5))
    q_tot += ((passo * W) * h_c) / t

# --- IDRAULICA: COLLETTORI E STACCHI ---
# Collettori (V_asp = 1.0, V_man = 1.5)
d_coll_asp = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.0)/math.pi)*2000)
d_coll_man = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.5)/math.pi)*2000)

# Stacchi Aspirazione
if superficie_tot <= 100:
    n_skimmer = math.ceil(superficie_tot / 20)
    q_sk = q_tot / n_skimmer
    d_sk = suggerisci_pvc(math.sqrt(((q_sk/3600)/1.7)/math.pi)*2000)
else:
    n_skimmer = 0
    d_sk = "N/A"

q_fo = q_tot / 2
d_fo = suggerisci_pvc(math.sqrt(((q_fo/3600)/1.7)/math.pi)*2000)

# Stacchi Mandata
n_boc = math.ceil(q_tot / cap_bocchetta)
q_boc = q_tot / n_boc
d_boc = suggerisci_pvc(math.sqrt(((q_boc/3600)/2.5)/math.pi)*2000)

# --- VISUALIZZAZIONE RISULTATI ---
st.header("🏗️ Progetto Idraulico e Locale Tecnico")

# 1. Collettori Principali
c1, c2 = st.columns(2)
with c1:
    st.success(f"### 📥 Aspirazione\n**Collettore: Ø {d_coll_asp} mm**\n(Portata: {q_tot:.2f} m³/h)")
with c2:
    st.info(f"### 📤 Mandata\n**Collettore: Ø {d_coll_man} mm**\n(Portata: {q_tot:.2f} m³/h)")

# 2. Locale Tecnico
st.divider()
st.subheader("⚙️ Filtrazione e Pompa")
f1, f2 = st.columns(2)

with f1:
    tipo_f = st.radio("Tipo Filtro:", ["Sabbia", "Cartuccia"], horizontal=True)
    sup_f = q_tot / v_filtrazione
    st.metric("Superficie Filtrante", f"{sup_f:.2f} m²") # Espresso in MQ
    if tipo_f == "Sabbia":
        diam_f = math.sqrt(sup_f / math.pi) * 2000
        st.write(f"Consigliato: **Ø {diam_f:.0f} mm**")
    else:
        st.write(f"Selezionare cartuccia con min. **{sup_f:.2f} m²**")

with f2:
    st.metric("Pompa (Portata Progetto)", f"{q_tot:.2f} m³/h")
    st.write("Pressione d'esercizio stimata: **1.2 - 1.5 bar**")

# 3. Tabella Riepilogativa
st.divider()
st.subheader("📋 Tabella Tubazioni (Ø Esterno PVC)")
st.table({
    "Tratto": ["Collettore Asp.", "Collettore Man.", "Stacco Skimmer", "Stacco Fondo", "Stacco Bocchetta"],
    "Diametro": [f"Ø {d_coll_asp}", f"Ø {d_coll_man}", f"Ø {d_sk}", f"Ø {d_fo}", f"Ø {d_boc}"],
    "Velocità (m/s)": [1.0, 1.5, 1.7, 1.7, 2.5]
})
