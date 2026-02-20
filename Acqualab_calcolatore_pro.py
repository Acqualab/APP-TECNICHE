import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO", page_icon="🏢", layout="centered")

# --- STILE CSS UNIVERSALE ---
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

# Definizione corretta dei 4 Tab
tab1, tab2, tab3, tab4 = st.tabs(["🏊 Assistente piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT COMPLETO ---
with tab1:
    st.header("Analisi e Interventi Piscina")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato (CC): **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA TUTTI I DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        # Sezione pH
        st.subheader("📊 Correzione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH meno G:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH Plus:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

        # Sezione Cloro
        st.subheader("📊 Sezione Cloro")
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        # Sezione Alghicida
        st.subheader("🌿 Sezione Alghicida")
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">✨ Algiprevent Mantenimento:</span> <span class="misura-grande">{(v_piscina*1)/100:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        vol_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
        lit_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    with col_v2:
        per_p = st.number_input("% Prodotto Commerciale", value=15.0)
    
    risultato_sol = (lit_i / vol_v) * per_p if vol_v > 0 else 0
    st.success(f"### ✅ Valore in programmazione: {risultato_sol:.2f} %")

# --- TAB 3: GESTIONE (Macchina Esistente) ---
with tab3:
    st.header("🚰 Verifica Macchina Installata")
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        vr_g = st.number_input("Volume Resina (L)", min_value=1, value=25, key="g_res")
        di_g = st.number_input("Durezza Entrata (°f)", min_value=1, value=35, key="g_in")
    with c_g2:
        do_g = st.number_input("Durezza Uscita (°f)", min_value=0, value=15, key="g_out")
        co_g = st.number_input("Consumo Acqua (m³/gg)", min_value=0.01, value=0.6, key="g_cons")
    
    da_g = di_g - do_g
    if da_g > 0:
        cap_ciclica = vr_g * 5
        m3_c = cap_ciclica / da_g
        s_rig = (vr_g * 140) / 1000
        
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_c:.2f} m³</span><br>Giorni stimati tra rigenerazioni: {m3_c/co_g:.1f}</div>', unsafe_allow_html=True)
        st.write(f"📊 **Dettagli tecnici:** Cap. Ciclica: {cap_ciclica} m³f | Sale per rigenerazione: {s_rig:.2f} kg")

# --- TAB 4: PROGETTO (Dimensionamento Professionale) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        tipo_u = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        dur_in_p = st.number_input("Durezza Acqua Grezza (°f)", value=35, key="p_in")
    with col_p2:
        dur_out_p = st.number_input("Durezza Miscelata desiderata (°f)", value=15, key="p_out")
        if tipo_u == "Villetta / Abitazione Singola":
            n_p = st.number_input("Numero persone", min_value=1, value=4)
            fabbisogno_p = n_p * 0.200
            q_picco_p = 1.20
        else:
            n_a = st.number_input("Numero appartamenti", min_value=1, value=10)
            fabbisogno_p = (n_a * 3) * 0.200
            q_picco_p = round(0.20 * math.sqrt(n_a * 3) + 0.8, 2)

    dur_netta_p = max(0, dur_in_p - dur_out_p)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    rp1, rp2 = st.columns(2)
    rp1.metric("Consumo stimato", f"{fabbisogno_p:.2f} m³/gg")
    rp2.metric("Portata di Picco (UNI 9182)", f"{q_picco_p:.2f} m³/h")

    if dur_netta_p > 0:
        resina_req = (fabbisogno_p * 3 * dur_netta_p) / 5
        taglie_comm = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300, 500]
        scelta_p = min([t for t in taglie_comm if t >= resina_req] or [max(taglie_comm)])

        st.markdown(f"""
        <div class="result-box">
            <span class="nome-prodotto">Taglia Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{scelta_p} L</span><br>
            <small>Dimensionato su delta durezza di {dur_netta_p}°f e 3gg di autonomia.</small>
        </div>
        """, unsafe_allow_html=True)
        
        if q_picco_p > 2.5:
            st.warning(f"⚠️ Portata di picco elevata ({q_picco_p} m³/h). Valutare valvola da 1\" 1/4 o superiore.")
    else:
        st.error("La durezza in uscita non può essere superiore o uguale a quella in entrata.")
