import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Progetto Professionale UNI 10637", layout="wide")

# --- FUNZIONI DI SUPPORTO ---
def suggerisci_pvc(d_interno):
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno, interno
    return "Fuori scala", d_interno

def get_t(h):
    if h > 1.35: return 3.0
    if h > 0.6:  return 2.5
    if h > 0.4:  return 1.0
    return 0.5

# --- INTERFACCIA ---
st.title("🛠️ Suite Professionale Progettazione Piscine")
st.subheader("Calcolo Idraulico Avanzato - UNI 10637:2024")

with st.sidebar:
    st.header("📋 Dati Vasca")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    
    st.divider()
    st.header("🛡️ Sicurezza Prese Fondo")
    q_max_produttore = st.number_input("Portata max griglia produttore (m³/h)", value=15.0)
    st.caption("Verificare sul datasheet della presa di fondo.")

# --- CALCOLO PORTATA GENERALE ---
superficie_tot = L * W
pendenza = (h_max - h_min) / L
q_tot = 0
passo = 0.05
for i in range(int(L/passo)):
    h_c = h_min + (i * passo * pendenza)
    q_tot += ((passo * W) * h_c) / get_t(h_c)

# --- DIMENSIONAMENTO COMPONENTI ---
# 1. SKIMMER
if superficie_tot <= 100:
    n_skimmer = math.ceil(superficie_tot / 20)
    q_stacco_skimmer = q_tot / n_skimmer
else:
    n_skimmer = 0
    q_stacco_skimmer = 0

# 2. PRESE DI FONDO (Minimo 2 in parallelo)
n_prese_fondo = 2
q_stacco_fondo = q_tot / n_prese_fondo # Caso peggiore: 100% portata dal fondo

# 3. BOCCHETTE
cap_bocchetta = 6.0 # m3/h default
n_bocchette = math.ceil(q_tot / cap_bocchetta)
q_stacco_man = q_tot / n_bocchette

# --- RISULTATI IDRAULICI ---
st.info(f"### 📊 Analisi Flussi (Portata Totale: {q_tot:.2f} m³/h)")

col1, col2 = st.columns(2)

with col1:
    st.write("#### 📥 Aspirazione")
    # Calcolo Tubi
    est_s_sk, _ = suggerisci_pvc(math.sqrt(((q_stacco_skimmer/3600)/1.7)/math.pi)*2000) if n_skimmer > 0 else (0,0)
    est_s_fo, _ = suggerisci_pvc(math.sqrt(((q_stacco_fondo/3600)/1.7)/math.pi)*2000)
    
    if n_skimmer > 0:
        st.write(f"🔹 **N. {n_skimmer} Skimmer**: Stacchi Ø {est_s_sk} mm")
    else:
        st.error("⚠️ OBBLIGO SFIORO (>100 m²)")

    st.write(f"🔹 **N. {n_prese_fondo} Prese di Fondo** (Parallelo)")
    st.write(f"• Distanza minima: **2.5 m**")
    st.write(f"• Stacchi singoli: **Ø {est_s_fo} mm**")
    
    # Verifica Portata Griglia
    if q_stacco_fondo > q_max_produttore:
        st.error(f"❌ PORTATA ECCESSIVA: {q_stacco_fondo:.1f} m³/h per griglia. Scegliere un modello più grande o aumentare il numero di prese.")
    else:
        st.success(f"✅ Verifica griglia: {q_stacco_fondo:.1f} m³/h < {q_max_produttore} m³/h")

with col2:
    st.write("#### 📤 Mandata")
    est_s_man, _ = suggerisci_pvc(math.sqrt(((q_stacco_man/3600)/2.5)/math.pi)*2000)
    st.write(f"🔹 **N. {n_bocchette} Bocchette**: Stacchi Ø {est_s_man} mm")

# --- SCHEMA TECNICO ---
st.divider()
st.subheader("📐 Schema di Collegamento Prese di Fondo")
st.write("Le due prese devono essere collegate 'a specchio' rispetto al collettore per garantire perdite di carico identiche.")



st.warning("⚠️ **Nota di Installazione:** Utilizzare un collettore di fondo di diametro adeguato prima di risalire verso il locale tecnico per mantenere la velocità < 1.0 m/s.")
# --- MODULO LOCALE TECNICO AGGIORNATO ---
st.divider()
st.subheader("🏗️ Dimensionamento Locale Tecnico")

col_tec1, col_tec2 = st.columns(2)

with col_tec1:
    st.write("#### 🔍 Scelta Filtrazione")
    
    # Selettore tipologia filtro
    tipo_filtro = st.radio("Tipologia Filtro:", ["Sabbia", "Cartuccia"], horizontal=True)
    
    # Calcolo superficie filtrante necessaria
    sup_filtrante_mq = q_tot / v_filtrazione
    
    if tipo_filtro == "Sabbia":
        # Calcolo diametro per filtri a sabbia (circolari)
        diam_filtro_mm = math.sqrt(sup_filtrante_mq / math.pi) * 2 * 1000
        st.metric("Superficie Filtrante Minima", f"{sup_filtrante_mq:.2f} m²")
        st.info(f"Ø Filtro a Sabbia consigliato: **{diam_filtro_mm:.0f} mm**")
    else:
        # Per i filtri a cartuccia si ragiona direttamente in superficie (mq o sq.ft)
        st.metric("Superficie Filtrante Minima", f"{sup_filtrante_mq:.2f} m²")
        st.success(f"Cerca una cartuccia con almeno **{sup_filtrante_mq:.2f} m²** di tessuto filtrante.")
        st.caption("Nota: I produttori spesso indicano la superficie in sq.ft (1 m² ≈ 10.76 sq.ft).")

with col_tec2:
    st.write("#### ⚙️ Circolazione")
    portata_pompa = q_tot * 1.10
    st.metric("Portata Nominale Pompa (+10%)", f"{portata_pompa:.2f} m³/h")
    prevalenza_stimata = st.selectbox("Prevalenza stimata (m.c.a.)", [10, 12, 15, 18], index=1)
    st.write(f"Punto di lavoro: **{q_tot:.2f} m³/h @ {prevalenza_stimata} m.c.a.**")
