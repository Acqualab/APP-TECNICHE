import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Addolcitori PRO", page_icon="🏢", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .metric-card {
        background-color: rgba(128, 128, 128, 0.05);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00AEEF;
        margin-bottom: 10px;
    }
    .highlight {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏢 Dimensionamento Addolcitori PRO")

tab1, tab2 = st.tabs(["📏 Dimensionamento Impianto", "💰 Autonomia e Consumi"])

# --- DATI COMUNI ---
with st.sidebar:
    st.header("Dati Acqua")
    durezza_in = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    durezza_out = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
    st.divider()
    st.info("La durezza da abbattere è: " + str(durezza_in - durezza_out) + " °f")

# --- TAB 1: DIMENSIONAMENTO (SCELTA TAGLIA) ---
with tab1:
    st.subheader("Calcolo Carico Idrico e Portata")
    
    tipo_utenza = st.radio("Tipo di Utenza:", ["Privato/Villetta", "Condominio"])
    
    if tipo_utenza == "Privato/Villetta":
        n_persone = st.number_input("Numero di persone", min_value=1, value=4)
        fabbisogno_die = n_persone * 200 / 1000 # 200 litri/testa
        # Portata picco stimata per villetta (2 rubinetti contemporanei)
        portata_picco = 1.2 # m3/h
    else:
        n_app = st.number_input("Numero di Appartamenti", min_value=2, value=10)
        n_persone = n_app * 3 # Media 3 persone/app
        fabbisogno_die = n_persone * 200 / 1000
        # Formula portata istantanea Condomini (Coefficiente di contemporaneità)
        # Formula semplificata: Q = 0.25 * sqrt(n_app * 2) + 0.5
        portata_picco = round(0.20 * math.sqrt(n_app * 3) + 0.8, 2)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="metric-card">Consumo Giornaliero stimato:<br><span class="highlight">{fabbisogno_die:.2f} m³/giorno</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card">Portata Istantanea (Picco):<br><span class="highlight">{portata_picco:.2f} m³/h</span></div>', unsafe_allow_html=True)

    st.write("### 🛠 Taglia Resina Consigliata")
    # Calcolo resina per avere rigenerazione ogni 4 giorni
    durezza_abb = durezza_in - durezza_out
    volume_resina_consigliato = (fabbisogno_die * 4 * durezza_abb) / 5
    
    st.success(f"Per garantire 4 giorni di autonomia, servono almeno **{math.ceil(volume_resina_consigliato)} Litri** di resina.")
    st.caption("Nota: Assicurarsi che la valvola scelta sopporti la Portata Istantanea calcolata sopra.")

# --- TAB 2: AUTONOMIA E CONSUMI ---
with tab2:
    st.subheader("Calcolo Ciclo e Costi")
    v_resina_scelta = st.number_input("Volume Resina Effettivo (L)", min_value=1, value=math.ceil(volume_resina_consigliato) if volume_resina_consigliato > 0 else 25)
    
    # Calcoli
    cap_ciclica = v_resina_scelta * 5
    durezza_abb = durezza_in - durezza_out
    m3_ciclo = cap_ciclica / durezza_abb
    giorni_autonomia = m3_ciclo / fabbisogno_die
    sale_rig = (v_resina_scelta * 0.14) # 140g per litro
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Dati Ciclo:**")
        st.write(f"💧 Acqua addolcita per ciclo: **{m3_ciclo:.2f} m³**")
        st.write(f"📅 Giorni tra rigenerazioni: **{giorni_autonomia:.1f}**")
    
    with c2:
        st.write("**Dati Rigenerazione:**")
        st.write(f"🧂 Sale per rigenerazione: **{sale_rig:.2f} kg**")
        st.write(f"🧪 Salamoia richiesta: **{sale_rig * 3:.1f} litri**")

    # Stima Annuale
    st.markdown('<p style="border-bottom: 2px solid #00AEEF; font-weight:bold;">Previsione Annuale</p>', unsafe_allow_html=True)
    num_rig_anno = 365 / giorni_autonomia
    sale_anno = num_rig_anno * sale_rig
    sacchi_anno = math.ceil(sale_anno / 25)
    
    st.write(f"L'utente consumerà circa **{sale_anno:.0f} kg** di sale all'anno (**{sacchi_anno} sacchi**).")
