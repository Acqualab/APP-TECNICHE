import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="UNI 10637:2024 - Progetto", layout="wide")

st.title("🏊 Calcolatore Professionale Piscine")
st.subheader("Analisi Geometrica e Idraulica - Tipo 2")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Parametri Vasca")
    L = st.number_input("Lunghezza totale (m)", min_value=0.1, value=12.0)
    W = st.number_input("Larghezza (m)", min_value=0.1, value=6.0)
    h_min = st.number_input("Profondità minima (m)", min_value=0.0, value=1.0)
    h_max = st.number_input("Profondità massima (m)", min_value=0.0, value=1.5)
    st.divider()
    v_filtrazione = st.slider("Velocità filtrazione (m/h)", 10, 50, 30)

# --- LOGICA DI CALCOLO ---
def get_tempo_ricircolo(h):
    if h > 1.35: return 3.0    # Zona C
    if h > 0.6:  return 2.5    # Zona D
    if h > 0.4:  return 1.0    # Zona E
    return 0.5                 # Zona F

passo = 0.05
portata_totale = 0
volume_totale = 0
pendenza = (h_max - h_min) / L
x_vals = []
h_vals = []

for i in range(int(L/passo) + 1):
    distanza = i * passo
    h_corrente = h_min + (distanza * pendenza)
    x_vals.append(distanza)
    h_vals.append(-h_corrente) # Negativo per il grafico (sott'acqua)
    
    if i < int(L/passo):
        t_zona = get_tempo_ricircolo(h_corrente)
        v_segmento = (passo * W) * h_corrente
        portata_totale += v_segmento / t_zona
        volume_totale += v_segmento

# --- SEZIONE GRAFICA ---
st.subheader("📉 Profilo Longitudinale e Zone di Ricircolo")
fig, ax = plt.subplots(figsize=(10, 3))
ax.fill_between(x_vals, h_vals, color='#0077be', alpha=0.3)
ax.plot(x_vals, h_vals, color='#0077be', lw=2)

# Linee di demarcazione Norma
for soglia in [0.4, 0.6, 1.35]:
    if h_min < soglia < h_max:
        ax.axhline(-soglia, color='red', linestyle='--', alpha=0.5)

ax.set_ylabel("Profondità (m)")
ax.set_xlabel("Lunghezza (m)")
ax.set_ylim(-(h_max + 0.5), 0.2)
st.pyplot(fig)



# --- RISULTATI ---
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Volume Totale", f"{volume_totale:.1f} m³")
with c2:
    st.metric("Portata (Q)", f"{portata_totale:.2f} m³/h")
with c3:
    area_filtro = portata_totale / v_filtrazione
    st.metric("Area Filtro", f"{area_filtro:.2f} m²")

st.subheader("📐 Suggerimento Condotte")
d_mandata = math.sqrt(((portata_totale/3600)/1.5)/math.pi) * 2 * 1000
st.success(f"Diametro interno mandata: **{d_mandata:.0f} mm** (V=1.5m/s)")
