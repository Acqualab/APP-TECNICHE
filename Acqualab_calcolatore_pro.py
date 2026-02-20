import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO", page_icon="🏢", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .misura-grande { font-size: 38px !important; font-weight: bold; color: #FF4B4B; margin-left: 10px; }
    .valore-evidenziato { font-size: 30px !important; font-weight: bold; color: #00AEEF; }
    .nome-prodotto { font-size: 18px; font-weight: 600; color: var(--text-color); }
    .unita-misura { font-size: 20px; color: #00AEEF; font-weight: bold; }
    .result-box { padding: 15px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.3); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 12px; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nCalcolo UNI 9182 integrato")

st.title("🧪 Suite Calcoli PRO")

# Definizione Tab (MOLTO IMPORTANTE: devono essere 4)
tab1, tab2, tab3, tab4 = st.tabs(["🏊 Assistente piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ---
with tab1:
    st.header("Analisi e Interventi")
    v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
    # ... (resto dei calcoli pool della Light)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione")
    vol_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    lit_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    per_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"Valore in programmazione: {(lit_i/vol_v)*per_p if vol_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ---
with tab3:
    st.header("🚰 Verifica Macchina Installata")
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        vr_g = st.number_input("Volume Resina (L)", value=25)
        di_g = st.number_input("Durezza Entrata (°f)", value=35)
    with c_g2:
        do_g = st.number_input("Durezza Uscita (°f)", value=15)
        co_g = st.number_input("Consumo (m³/gg)", value=0.6)
    
    da_g = di_g - do_g
    if da_g > 0:
        m3_c = (vr_g * 5) / da_g
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_c:.2f} m³</span></div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (DIMENSIONAMENTO) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        tipo_u = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        dur_in = st.number_input("Durezza Acqua Grezza (°f)", value=35, key="pro_in")
    with col_p2:
        dur_out = st.number_input("Durezza Miscelata desiderata (°f)", value=15, key="pro_out")
        if tipo_u == "Villetta":
            n_p = st.number_input("Persone", min_value=1, value=4)
            fabbisogno = n_p * 0.200
            q_picco = 1.20
        else:
            n_a = st.number_input("Appartamenti", min_value=1, value=10)
            fabbisogno = (n_a * 3) * 0.200
            q_picco = round(0.20 * math.sqrt(n_a * 3) + 0.8, 2)

    dur_netta = max(0, dur_in - dur_out)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    r1.metric("Consumo stimato", f"{fabbisogno:.2f} m³/gg")
    r2.metric("Portata di Picco", f"{q_picco:.2f} m³/h")

    if dur_netta > 0:
        # Calcolo resina per 3 giorni di autonomia
        resina_req = (fabbisogno * 3 * dur_netta) / 5
        taglie_comm = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
        scelta = min([t for t in taglie_comm if t >= resina_req] or [max(taglie_comm)])

        st.markdown(f"""
        <div class="result-box">
            <span class="nome-prodotto">Taglia Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{scelta} L</span><br>
            <small>Basato su una durezza netta di {dur_netta}°f</small>
        </div>
        """, unsafe_allow_html=True)
        
        if q_picco > 2.5:
            st.warning(f"⚠️ Portata di picco elevata ({q_picco} m³/h): necessaria valvola da 1\" 1/4 o superiore.")
