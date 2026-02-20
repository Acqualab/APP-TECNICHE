import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO - Enterprise", page_icon="🏢", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .misura-grande { font-size: 34px !important; font-weight: bold; color: #FF4B4B; }
    .valore-evidenziato { font-size: 32px !important; font-weight: bold; color: #00AEEF; }
    .result-box { padding: 20px; border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 15px; text-align: center; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 15px; margin-top: 15px; }
    .stat-label { font-size: 13px; color: gray; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("ACQUALAB S.R.L.")

st.title("🧪 Suite Calcoli PRO")

# Definizione Tab
tab1, tab2, tab3, tab4 = st.tabs(["🏊 Piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto UNI 9182"])

# --- TAB 1: ANALISI PISCINA ---
with tab1:
    st.header("Analisi e Interventi Piscina")
    cp1, cp2 = st.columns(2)
    with cp1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=1.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.8, step=0.1)
    with cp2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.5)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato (CC): **{cl_combinato:.2f} ppm**")
    
    st.markdown('<p class="titolo-sezione">Dosaggi Consigliati</p>', unsafe_allow_html=True)
    d_col1, d_col2 = st.columns(2)
    
    if ph_ril > 7.4:
        kg_ph = (v_piscina * 10 * ((ph_ril - 7.2) / 0.1)) / 1000
        d_col1.markdown(f'<div class="result-box">👉 pH meno G:<br><span class="misura-grande">{kg_ph:.2f} kg</span></div>', unsafe_allow_html=True)
    
    if cl_combinato >= 0.4:
        ppm_shock = (cl_combinato * 10) - cl_libero
        kg_shock = (v_piscina * 1.5 * ppm_shock) / 1000
        d_col2.markdown(f'<div class="result-box">🔥 Shock Chemacal 70:<br><span class="misura-grande">{kg_shock:.2f} kg</span></div>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca (L)", value=100.0)
    l_i = st.number_input("Litri prodotto (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE (CONSUMI SINGOLA RIGENERAZIONE E INTERVALLO) ---
with tab3:
    st.header("🚰 Verifica Macchina Installata")
    g1, g2 = st.columns(2)
    with g1:
        vr_g = st.number_input("Volume Resina (L)", value=25, key="vr_g")
        di_g = st.number_input("Durezza Entrata (°f)", value=35, key="di_g")
    with g2:
        do_g = st.number_input("Durezza Uscita (°f)", value=15, key="do_g")
        co_g = st.number_input("Consumo (m³/gg)", value=0.60, key="co_g")
    
    delta_g = max(0.1, di_g - do_g)
    cap_cic = vr_g * 5
    m3_autonomia = cap_cic / delta_g
    sale_rig = (vr_g * 140) / 1000
    gg_intervallo = m3_autonomia / co_g if co_g > 0 else 0

    st.markdown('<p class="titolo-sezione">Risultati Ciclo</p>', unsafe_allow_html=True)
    res1, res2 = st.columns(2)
    res1.metric("Autonomia", f"{m3_autonomia:.2f} m³", f"Ogni {gg_intervallo:.1f} gg")
    res2.metric("Sale per Ciclo", f"{sale_rig:.2f} kg", "A rigenerazione")

    st.markdown('<p class="titolo-sezione">Dettagli Tecnici (Singola Rigenerazione)</p>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    d1.write(f"<span class='stat-label'>Cap. Ciclica</span><br><span class='stat-value'>{cap_cic} m³f</span>", unsafe_allow_html=True)
    d2.write(f"<span class='stat-label'>Salamoia</span><br><span class='stat-value'>{(sale_rig*3):.1f} L</span>", unsafe_allow_html=True)
    d3.write(f"<span class='stat-label'>Scarico</span><br><span class='stat-value'>{vr_g*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO UNI 9182 & CONFRONTO ---
with tab4:
    st.header("📐 Progettazione e Analisi Portate")
    p1, p2 = st.columns(2)
    with p1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"], key="p_tipo")
        p_in = st.number_input("Durezza Ingresso (°f)", value=35, key="p_in")
        p_out = st.number_input("Durezza Uscita desiderata (°f)", value=15, key="p_out")
    with p2:
        if tipo == "Villetta":
            pers = st.number_input("Persone", value=4, key="p_p")
            f_gg = pers * 0.20
            q_p = 1.20
        else:
            app = st.number_input("Appartamenti", value=10, key="p_a")
            f_gg = (app * 3) * 0.20
            q_p = round(0.20 * math.sqrt(app * 3) + 0.8, 2)

    p_delta_pro = max(0.1, p_in - p_out)
    taglia_nec = (f_gg * 3 * p_delta_pro) / 5
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    scelta = min([t for t in taglie if t >= taglia_nec] or [max(taglie)])
    
    n_rig_anno = 365 / (((scelta * 5) / p_delta_pro) / f_gg)
    sale_anno = (scelta * 0.14) * n_rig_anno
    acqua_anno = (scelta * 7 * n_rig_anno) / 1000

    st.markdown(f'<div class="result-box">Taglia Suggerita: <span class="valore-evidenziato">{scelta} Litri Resina</span></div>', unsafe_allow_html=True)

    st.markdown('<p class="titolo-sezione">Dati di Progetto (UNI 9182)</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Consumo Giornaliero", f"{f_gg:.2f} m³/gg")
    c2.metric("Portata di Picco", f"{q_p} m³/h")

    st.markdown('<p class="titolo-sezione">📊 Confronto Annuale: Standard vs Clack</p>', unsafe_allow_html=True)
    st.table({
        "Dati Annuali": ["Sale Totale", "Sacchi (25kg)", "Acqua Scarico", "N. Rigenerazioni"],
        "Valvola Standard": [f"{sale_anno:.0f} kg", f"{math.ceil(sale_anno/25)}", f"{acqua_anno:.2f} m³", f"{n_rig_anno:.0f}"],
        "Clack Impression": [f"{sale_anno*0.8:.0f} kg", f"{math.ceil((sale_anno*0.8)/25)}", f"{acqua_anno*0.8:.2f} m³", "Ottimizzata"]
    })
    
    st.success(f"📉 **Risparmio stimato con Clack:** {(sale_anno*0.2):.0f} kg di sale e {(acqua_anno*0.2)*1000:.0f} L d'acqua ogni anno.")
