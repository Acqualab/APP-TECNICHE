import streamlit as st
import math
import matplotlib.pyplot as plt

# --- CONFIGURAZIONE FISSA ---
st.set_page_config(page_title="Progetto Professionale UNI 10637", layout="wide")

def suggerisci_pvc(d_interno):
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno
    return "N/A"

# --- 1. LAYOUT APPROVATO: INPUT E GEOMETRIA ---
st.title("🛠️ Suite Professionale Progettazione Piscine")
st.subheader("Calcolo Integrato UNI 10637:2024")

with st.sidebar:
    st.header("📋 Dati Vasca")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    
    st.divider()
    st.header("🚀 Parametri Tecnici")
    v_filtrazione = st.slider("Velocità filtrazione (m/h)", 20, 50, 30)
    q_max_griglia = st.number_input("Portata max griglia fondo (m³/h)", value=15.0)
    cap_bocchetta = st.number_input("Portata singola bocchetta (m³/h)", value=6.0)

# Calcolo Portata Totale (Prospetto 3)
superficie_tot = L * W
passo = 0.1
q_tot = 0
for i in range(int(L/passo)):
    h_c = h_min + (i * passo * (h_max - h_min) / L)
    # Tempi di ricircolo Prospetto 3
    t = 3.0 if h_c > 1.35 else (2.5 if h_c > 0.6 else (1.0 if h_c > 0.4 else 0.5))
    q_tot += ((passo * W) * h_c) / t

# --- 2. LAYOUT APPROVATO: COMPONENTI E IDRAULICA ---
st.info(f"### 📊 Analisi Generale (Portata: {q_tot:.2f} m³/h - Sup: {superficie_tot:.2f} m²)")

col1, col2 = st.columns(2)
with col1:
    st.write("#### 📥 Aspirazione")
    if superficie_tot <= 100:
        n_skimmer = math.ceil(superficie_tot / 20)
        q_sk = q_tot / n_skimmer
        d_sk = suggerisci_pvc(math.sqrt(((q_sk/3600)/1.7)/math.pi)*2000)
        st.write(f"🔹 **N. {n_skimmer} Skimmer**: Tubo Ø {d_sk} mm")
    else:
        st.error("⚠️ OLTRE 100 m²: OBBLIGO SFIORO")
    
    q_fo = q_tot / 2
    d_fo = suggerisci_pvc(math.sqrt(((q_fo/3600)/1.7)/math.pi)*2000)
    st.write(f"🔹 **N. 2 Prese Fondo**: Tubo Ø {d_fo} mm (Dist. 2.5m)")
    if q_fo > q_max_griglia: st.error(f"Griglia insufficiente ({q_fo:.1f} m³/h)")

with col2:
    st.write("#### 📤 Mandata")
    n_boc = math.ceil(q_tot / cap_bocchetta)
    q_boc = q_tot / n_boc
    d_boc = suggerisci_pvc(math.sqrt(((q_boc/3600)/2.5)/math.pi)*2000)
    st.write(f"🔹 **N. {n_boc} Bocchette**: Tubo Ø {d_boc} mm")

# --- 3. NUOVO MODULO: LOCALE TECNICO ---
st.divider()
st.subheader("🏗️ Dimensionamento Locale Tecnico")
c_tec1, c_tec2 = st.columns(2)

with c_tec1:
    tipo_filtro = st.radio("Tipologia Filtro:", ["Sabbia", "Cartuccia"], horizontal=True)
    sup_filtrante_mq = q_tot / v_filtrazione
    st.metric("Superficie Filtrante Minima", f"{sup_filtrante_mq:.2f} m²")
    
    if tipo_filtro == "Sabbia":
        diam_f = math.sqrt(sup_filtrante_mq / math.pi) * 2000
        st.info(f"Ø Filtro consigliato: **{diam_f:.0f} mm**")
    else:
        st.success(f"Richiesti **{sup_filtrante_mq * 10.76:.0f} sq.ft** di superficie filtrante")

with c_tec2:
    st.write("#### ⚙️ Pompa di Circolazione")
    st.metric("Punto di Lavoro", f"{q_tot:.2f} m³/h")
    prevalenza = st.selectbox("Prevalenza (m.c.a.)", [10, 12, 15, 18], index=1)
    st.caption(f"Selezionare pompa capace di {q_tot:.1f} m³/h a {prevalenza} m di prevalenza.")            
# --- MODULO AGGIORNATO: COLLETTORI E RIEPILOGO IDRAULICO ---
st.divider()
st.subheader("🏛️ Dimensionamento Collettori Principali")

col_coll1, col_coll2 = st.columns(2)

with col_coll1:
    st.write("#### 📥 Collettore di Aspirazione")
    # Velocità prudenziale per collettore aspirazione: 1.0 m/s
    d_int_coll_asp = math.sqrt(((q_tot/3600)/1.0)/math.pi) * 2000
    est_coll_asp = suggerisci_pvc(d_int_coll_asp)
    
    st.metric("Portata Tot. Aspirazione", f"{q_tot:.2f} m³/h")
    st.success(f"Diametro consigliato: **Ø {est_coll_asp} mm**")
    st.caption("Calcolato con velocità di 1.0 m/s per prevenire cavitazione.")

with col_coll2:
    st.write("#### 📤 Collettore di Mandata")
    # Velocità prudenziale per collettore mandata: 1.5 m/s
    d_int_coll_man = math.sqrt(((q_tot/3600)/1.5)/math.pi) * 2000
    est_coll_man = suggerisci_pvc(d_int_coll_man)
    
    st.metric("Portata Tot. Mandata", f"{q_tot:.2f} m³/h")
    st.success(f"Diametro consigliato: **Ø {est_coll_man} mm**")
    st.caption("Calcolato con velocità di 1.5 m/s.")

# --- TABELLA RIASSUNTIVA FINALE PER RELAZIONE ---
st.divider()
st.subheader("📋 Riepilogo Dimensioni Tubazioni (Diametri Esterni PVC)")

dati_tubi = {
    "Tratto": ["Collettore Aspirazione", "Collettore Mandata", "Stacco Skimmer", "Stacco Presa Fondo", "Stacco Bocchetta"],
    "Portata (m³/h)": [q_tot, q_tot, q_sk if n_skimmer > 0 else 0, q_fo, q_boc],
    "Velocità (m/s)": [1.0, 1.5, 1.7, 1.7, 2.5],
    "Diametro PVC (Ø)": [est_coll_asp, est_coll_man, d_sk if n_skimmer > 0 else "N/A", d_fo, d_boc]
}
st.table(dati_tubi)
