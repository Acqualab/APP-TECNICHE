import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO Suite", page_icon="🏢", layout="centered")

# --- STILE CSS UNIVERSALE ---
st.markdown("""
    <style>
    .misura-grande { font-size: 38px !important; font-weight: bold; color: #FF4B4B; margin-left: 10px; }
    .valore-evidenziato { font-size: 30px !important; font-weight: bold; color: #00AEEF; }
    .nome-prodotto { font-size: 18px; font-weight: 600; color: #333; }
    .unita-misura { font-size: 20px; color: #00AEEF; font-weight: bold; }
    .result-box { padding: 15px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.3); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 12px; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: #1E3A8A; border-bottom: 2px solid #00AEEF; margin-bottom: 15px; margin-top: 10px; }
    .comparison-card { background-color: #f1f8ff; border-radius: 10px; padding: 20px; border-left: 5px solid #00AEEF; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Integrato UNI 9182")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (VERSIONE LIGHT INTEGRATA) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato (CC): **{cl_combinato:.2f} ppm**")
    st.markdown("---")
    sale_ril_mgl = st.number_input("Sale rilevato (mg/L - ppm)", min_value=0.0, value=0.0, step=100.0)

    if st.button("🚀 CALCOLA TUTTI I DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        st.subheader("🧂 Sezione Sale")
        sale_gl = sale_ril_mgl / 1000
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🧂 Clorinatore Standard (4.5):</span> <span class="misura-grande">{(v_piscina * max(0.0, 4.5 - sale_gl)):.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        st.subheader("📊 Correzione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH meno G:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH Plus:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

        st.subheader("📊 Sezione Cloro")
        if cl_libero < 1.5:
            d_cl = 1.5 - cl_libero
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

        st.subheader("🌿 Sezione Alghicida")
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">✨ Algiprevent Mantenimento:</span> <span class="misura-grande">{(v_piscina*1)/100:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    vol_vasca_sol = st.number_input("Volume Vasca Soluzione (L)", min_value=1.0, value=100.0)
    litri_ins_sol = st.number_input("Litri prodotto versati (L)", value=10.0)
    perc_prod_sol = st.number_input("% Prodotto Commerciale", value=15.0)
    ris_p_sol = (litri_ins_sol / vol_vasca_sol) * perc_prod_sol if vol_vasca_sol > 0 else 0
    st.success(f"### ✅ Valore in programmazione: {ris_p_sol:.2f} %")

# --- TAB 3: GESTIONE (ESISTENTE) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (L)", min_value=1, value=25, key="vr_g")
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35, key="di_g")
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15, key="do_g")
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, key="co_g")

    da_gest = max(0.1, di_gest - do_gest)
    cap_c = vr_gest * 5 
    m3_c = cap_c / da_gest
    sale_rig = (vr_gest * 140) / 1000
    gg_a = m3_c / co_gest if co_gest > 0 else 0

    st.markdown('<p class="titolo-sezione">Risultati Ciclo</p>', unsafe_allow_html=True)
    r_c1, r_c2 = st.columns(2)
    r_c1.metric("Autonomia", f"{m3_c:.2f} m³", f"Ogni {gg_a:.1f} gg")
    r_c2.metric("Sale/Rigenerazione", f"{sale_rig:.2f} kg")

    d_c1, d_c2, d_c3 = st.columns(3)
    d_c1.metric("Cap. Ciclica", f"{cap_c} m³f")
    d_c2.metric("Salamoia", f"{(sale_rig*3):.1f} L")
    d_c3.metric("Scarico", f"{(vr_gest*7):.0f} L")

# --- TAB 4: PROGETTO (COMPLETA CON MIX E INTERVALLO) ---
with tab4:
    st.header("📐 Progettazione e Risparmio Clack")
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo_ut = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        d_ingresso = st.number_input("Durezza Acquedotto (°f)", value=35, key="d_ing_p")
        d_mix_des = st.number_input("Durezza Mix Desiderata (°f)", value=15,
