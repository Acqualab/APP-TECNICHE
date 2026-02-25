import streamlit as st
import math
import matplotlib.pyplot as plt

# Configurazione Pagina
st.set_page_config(page_title="UNI 10637:2024 - Progetto Piscine", layout="wide")

st.title("🏊 Partner di Programmazione: Progetto Piscine")
st.subheader("Dimensionamento Impianto Tipo 2 - Norma UNI 10637:2024")

# --- SIDEBAR: INPUT DATI ---
with st.sidebar:
    st.header("⚙️ Dati Geometrici")
    L = st.number_input("Lunghezza vasca (m)", min_value=1.0, value=12.0, step=0.5)
    W = st.number_input("Larghezza vasca (m)", min_value=1.0, value=6.0, step=0.5)
    h_min = st.number_input("Profondità minima (m)", min_value=0.0, value=1.0, step=0.1)
    h_max = st.number_input("Profondità massima (m)", min_value=0.0, value=1.6, step=0.1)
    
    st.divider()
    st.header("💧 Parametri Tecnici")
    v_filtrazione = st.slider("Velocità filtrazione (m/h)", 20, 50, 30)
    cap_bocchetta = st.number_input("Portata singola bocchetta (m³/h)", value=6.0, step=0.5)

# --- LOGICA DI CALCOLO (PROSPETTO 3) ---
def get_tempo_ricircolo(h):
    if h > 1.35: return 3.0    # Zona C
    if h > 0.6:  return 2.5    # Zona D
    if h > 0.4:  return 1.0    # Zona E
    return 0.5                 # Zona F

# Calcolo integrato per sezioni
passo = 0.05 # 5cm di precisione
portata_totale = 0
volume_totale = 0
superficie_totale = L * W
pendenza = (h_max - h_min) / L

x_grafico = []
h_grafico = []

for i in range(int(L/passo) + 1):
    dist_x = i * passo
    h_curr = h_min + (dist_x * pendenza)
    x_grafico.append(dist_x)
    h_grafico.append(-h_curr)
    
    if i < int(L/passo):
        t_zona = get_tempo_ricircolo(h_curr)
        v_seg = (passo * W) * h_curr
        portata_totale += v_seg / t_zona
        volume_totale += v_seg

# --- CALCOLO COMPONENTI ---
# Skimmer: 1 ogni 20mq di superficie (Norma UNI 10637 Tipo 2)
n_skimmer = math.ceil(superficie_totale / 20)

# Bocchette: basate sulla portata totale
n_bocchette = math.ceil(portata_totale / cap_bocchetta)

# Tubazioni (V_mandata = 1.5 m/s, V_aspirazione = 1.0 m/s)
d_mandata = math.sqrt(((portata_totale/3600)/1.5)/math.pi) * 2 * 1000
d_aspirazione = math.sqrt(((portata_totale/3600)/1.0)/math.pi) * 2 * 1000

# --- VISUALIZZAZIONE GRAFICA ---
st.subheader("📉 Profilo Vasca e Analisi Zone")
fig, ax = plt.subplots(figsize=(10, 3))
ax.fill_between(x_grafico, h_grafico, color='#3498db', alpha=0.4, label='Volume Acqua')
ax.plot(x_grafico, h_grafico, color='#2980b9', lw=3)

# Linee soglia Norma
soglie = [0.4, 0.6, 1.35]
colori_soglie = ['#e74c3c', '#e67e22', '#f1c40f']
for s, col in zip(soglie, colori_soglie):
    if h_min < s < h_max:
        ax.axhline(-s, color=col, linestyle='--', alpha=0.6, label=f'Limite {s}m')

ax.set_ylim(-(h_max + 0.5), 0.2)
ax.legend(loc='lower left', fontsize='small')
st.pyplot(fig)

# --- RISULTATI FINALI ---
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Volume Totale", f"{volume_totale:.1f} m³")
    st.metric("Superficie Acqua", f"{superficie_totale:.1f} m²")

with c2:
    st.metric("Portata di Progetto (Q)", f"{portata_totale:.2f} m³/h")
    area_f = portata_totale / v_filtrazione
    st.metric("Superficie Filtrazione", f"{area_f:.2f} m²")

with c3:
    st.subheader("📦 Componenti Necessari")
    st.write(f"✅ **N. {n_skimmer}** Skimmer (1/20m²)")
    st.write(f"✅ **N. {n_bocchette}** Bocchette (a {cap_bocchetta} m³/h)")

st.divider()
st.subheader("📐 Dimension
