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
    .stat-label { font-size: 12px; color: gray; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 22px; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nCalcoli UNI 9182 e Risparmio Clack attivi.")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ripristinato) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.8, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.5, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    st.markdown('<p class="titolo-sezione">Dosaggi Consigliati</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    
    if ph_ril > 7.4:
        kg_ph = (v_piscina * 10 * ((ph_ril - 7.2) / 0.1)) / 1000
        res_p1.markdown(f'<div class="result-box">👉 pH meno G:<br><span class="misura-grande">{kg_ph:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
    
    if cl_combinato >= 0.4:
        ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
        kg_shock = (v_piscina * 1.5 * ppm_shock) / 1000
        res_p2.markdown(f'<div class="result-box">🔥 Shock Chemacal 70:<br><span class="misura-grande">{kg_shock:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE (Consumi Singola Rigenerazione) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = max(0.1, di_gest - do_gest)
    cap_ciclo = vr_gest * 5
    m3_ciclo = cap_ciclo / da_gest
    sale_rig = (vr_gest * 140) / 1000
    gg_intervallo = m3_ciclo / co_gest if co_gest > 0 else 0

    st.markdown('<p class="titolo-sezione">Risultati Ciclo e Autonomia</p>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    r1.metric("Produzione Acqua Dolce", f"{m3_ciclo:.2f} m³", f"Ogni {gg_intervallo:.1f} gg")
    r2.metric("Sale / Rigenerazione", f"{sale_rig:.2f} kg", "Consumo per ciclo")

    st.markdown('<p class="titolo-sezione">Dettagli Tecnici (Singolo Ciclo)</p>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    d1.write(f"<span class='stat-label'>Cap. Ciclica</span><br><span class='stat-value'>{cap_ciclo} m³f</span>", unsafe_allow_html=True)
    d2.write(f"<span class='stat-label'>Volume Salamoia</span><br><span class='stat-value'>{(sale_rig*3):.1f} L</span>", unsafe_allow_html=True)
    d3.write(f"<span class='stat-label'>Acqua Scarico</span><br><span class='stat-value'>{vr_gest*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Risparmio Annuale e UNI 9182) ---
with tab4:
    st.header("📐 Progettazione e Confronto")
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        d_in_p = st.number_input("Durezza Ingresso (°f)", value=35, key="d_in_p")
        d_out_p = st.number_input("Durezza Uscita (°f)", value=15, key="d_out_p")
    with cp2:
        if tipo == "Villetta":
            u_val = st.number_input("Numero Persone", value=4)
            cons_gg = u_val * 0.20
            picco_p = 1.20
        else:
            u_val = st.number_input("Numero Appartamenti", value=10)
            cons_gg = (u_val * 3) * 0.20
            picco_p = round(0.20 * math.sqrt(u_val * 3) + 0.8, 2)

    d_delta = max(0.1, d_in_p - d_out_p)
    res_nec = (cons_gg * 3 * d_delta) / 5
    taglie_std = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    scelta_p = min([t for t in taglie_std if t >= res_nec] or [max(taglie_std)])

    st.markdown(f'<div class="result-box">Taglia Suggerita: <span class="valore-evidenziato">{scelta_p} Litri Resina</span></div>', unsafe_allow_html=True)

    # Calcoli Annuali
    m3_anno = cons_gg * 365
    rig_anno = m3_anno / ((scelta_p * 5) / d_delta)
    sale_anno_std = (scelta_p * 0.14) * rig_anno
    acqua_anno_std = (scelta_p * 7 * rig_anno) / 1000

    st.markdown('<p class="titolo-sezione">📊 Risparmio Annuale: Standard vs Clack</p>', unsafe_allow_html=True)
    st.table({
        "Parametro (Annuo)": ["Sale Totale", "Sacchi (25kg)", "Acqua Scarico", "N. Rigenerazioni"],
        "Valvola Standard": [f"{sale_anno_std:.0f} kg", f"{math.ceil(sale_anno_std/25)}", f"{acqua_anno_std:.2f} m³", f"{rig_anno:.0f}"],
        "Clack Impression": [f"{sale_anno_std*0.8:.0f} kg", f"{math.ceil((sale_anno_std*0.8)/25)}", f"{acqua_anno_std*0.8:.2f} m³", "Ottimizzata"]
    })

    st.success(f"📉 **Risparmio Stimato:** {sale_anno_std*0.2:.0f} kg di sale e {(acqua_anno_std*0.2)*1000:.0f} L d'acqua ogni anno.")
    st.info(f"⚙️ **Portata di Picco UNI 9182:** {picco_p} m³/h")
