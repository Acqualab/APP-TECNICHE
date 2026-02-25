import streamlit as st
import math

# Configurazione della pagina
st.set_page_config(page_title="UNI 10637:2024 Calc", layout="wide")

st.title("🏊 Calcolatore Professionale Piscine Tipo 2")
st.write("Dimensionamento secondo la norma **UNI 10637:2024**")

# --- INPUT NELLA SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Parametri Vasca")
    L = st.number_input("Lunghezza (m)", min_value=0.1, value=12.0, step=0.5)
    W = st.number_input("Larghezza (m)", min_value=0.1, value=6.0, step=0.5)
    h_min = st.number_input("Profondità minima (m)", min_value=0.0, value=1.0, step=0.1)
    h_max = st.number_input("Profondità massima (m)", min_value=0.0, value=1.5, step=0.1)
    
    st.divider()
    v_filtrazione = st.slider("Velocità filtrazione (m/h)", 10, 50, 30)

# --- LOGICA DI CALCOLO ---
def get_tempo_ricircolo(h):
    # Basato sul Prospetto 3 fornito dall'utente
    if h > 1.35: return 3.0    # Zona C
    if h > 0.6:  return 2.5    # Zona D
    if h > 0.4:  return 1.0    # Zona E
    return 0.5                 # Zona F

# Calcolo tramite integrazione (passo 5cm per massima precisione)
passo = 0.05
portata_totale = 0
volume_totale = 0
pendenza = (h_max - h_min) / L

for i in range(int(L/passo)):
    distanza = i * passo
    h_corrente = h_min + (distanza * pendenza)
    t_zona = get_tempo_ricircolo(h_corrente)
    v_segmento = (passo * W) * h_corrente
    portata_totale += v_segmento / t_zona
    volume_totale += v_segmento

# Calcolo tecnico componenti
area_filtro = portata_totale / v_filtrazione
# Diametro con v=1.5 m/s (mandata)
diam_mandata = math.sqrt(((portata_totale/3600)/1.5)/math.pi) * 2 * 1000
# Diametro con v=1.0 m/s (aspirazione)
diam_aspirazione = math.sqrt(((portata_totale/3600)/1.0)/math.pi) * 2 * 1000

# --- VISUALIZZAZIONE RISULTATI ---
c1, c2, c3 = st.columns(3)
c1.metric("Volume Totale", f"{volume_totale:.1f} m³")
c2.metric("Portata Progetto", f"{portata_totale:.2f} m³/h")
c3.metric("Area Filtro", f"{area_filtro:.2f} m²")

st.subheader("📐 Dimensionamento Tubazioni (Diametri Interni)")
col_a, col_b = st.columns(2)
col_a.success(f"Mandata (1.5 m/s): **{diam_mandata:.0f} mm**")
col_b.warning(f"Aspirazione (1.0 m/s): **{diam_aspirazione:.0f} mm**")

st.divider()
st.caption("Il software calcola la portata integrando i diversi tempi di ricircolo lungo il profilo della vasca.")
