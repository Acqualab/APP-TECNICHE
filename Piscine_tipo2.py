import streamlit as st
import math

# Configurazione della pagina per Streamlit
st.set_page_config(page_title="UNI 10637:2024", layout="wide")

st.title("🏊 Calcolatore Professionale Piscine Tipo 2")
st.write("Dimensionamento basato sul **Prospetto 3 (UNI 10637:2024)**")

# --- INTERFACCIA DI INPUT ---
with st.sidebar:
    st.header("⚙️ Parametri Vasca")
    L = st.number_input("Lunghezza totale (m)", min_value=0.1, value=12.0)
    W = st.number_input("Larghezza (m)", min_value=0.1, value=6.0)
    h_min = st.number_input("Profondità minima (m)", min_value=0.0, value=1.0)
    h_max = st.number_input("Profondità massima (m)", min_value=0.0, value=1.5)
    
    st.divider()
    v_filtrazione = st.slider("Velocità filtrazione (m/h)", 10, 50, 30)

# --- FUNZIONE LOGICA (PROSPETTO 3) ---
def get_tempo_ricircolo(h):
    if h > 1.35: return 3.0    # Zona C
    if h > 0.6:  return 2.5    # Zona D
    if h > 0.4:  return 1.0    # Zona E
    return 0.5                 # Zona F

# --- CALCOLO ---
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

# Dimensionamento tecnico
area_filtro = portata_totale / v_filtrazione
diam_mandata = math.sqrt(((portata_totale/3600)/1.5)/math.pi) * 2 * 1000
diam_aspirazione = math.sqrt(((portata_totale/3600)/1.0)/math.pi) * 2 * 1000

# --- MOSTRA I RISULTATI ---
c1, c2, c3 = st.columns(3)
c1.metric("Volume Totale", f"{volume_totale:.1f} m³")
c2.metric("Portata Totale (Q)", f"{portata_totale:.2f} m³/h")
c3.metric("Area Filtro Min.", f"{area_filtro:.2f} m²")

st.subheader("📐 Condotte (Diametri Interni)")
col_a, col_b = st.columns(2)
col_a.success(f"Mandata (1.5 m/s): {diam_mandata:.0f} mm")
col_b.warning(f"Aspirazione (1.0 m/s): {diam_aspirazione:.0f} mm")

st.info("I calcoli integrano automaticamente i tempi di ricircolo differenziati per zona di profondità.")
