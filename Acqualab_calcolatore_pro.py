import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO", page_icon="🏢", layout="centered")

# --- STILE CSS UNIVERSALE ---
st.markdown("""
    <style>
    .misura-grande { font-size: 38px !important; font-weight: bold; color: #FF4B4B; margin-left: 10px; }
    .valore-evidenziato { font-size: 30px !important; font-weight: bold; color: #00AEEF; }
    .nome-prodotto { font-size: 18px; font-weight: 600; color: #333; }
    .unita-misura { font-size: 20px; color: #00AEEF; font-weight: bold; }
    .result-box { padding: 15px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.3); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 12px; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: #1E3A8A; border-bottom: 2px solid #00AEEF; margin-bottom: 15px; margin-top: 10px; }
    .stat-label { font-size: 12px; color: gray; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 22px; font-weight: bold; color: #333; }
    .comparison-card { background-color: #f1f8ff; border-radius: 10px; padding: 20px; border-left: 5px solid #00AEEF; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione & Clack")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (CORRETTA) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=1.0, value=100.0)
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
    else:
        res_p1.success("pH nei limiti ottimali.")
    
    if cl_combinato >= 0.4:
        ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
        kg_shock = (v_piscina * 1.5 * ppm_shock) / 1000
        res_p2.markdown(f'<div class="result-box">🔥 Shock Chemacal 70:<br><span class="misura-grande">{kg_shock:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
    else:
        res_p2.success("Cloro combinato OK.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", min_value=1.0, value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p:.2f} %")

# --- TAB 3: GESTIONE (CON SALE PER RIG) ---
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
    sale_rig = (vr_gest * 140) / 1000 # 140g per litro resina
    gg_intervallo = m3_ciclo / co_gest if co_gest > 0 else 0

    st.markdown('<p class="titolo-sezione">Risultati Ciclo e Autonomia</p>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    r1.metric("Autonomia Reale", f"{m3_ciclo:.2f} m³", f"Ogni {gg_intervallo:.1f} gg")
    r2.metric("Sale per Ciclo", f"{sale_rig:.2f} kg", "Quantità per rigenerazione")

    st.markdown('<p class="titolo-sezione">Dettagli Tecnici Singola Rigenerazione</p>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    d1.write(f"<span class='stat-label'>Cap. Ciclica</span><br><span class='stat-value'>{cap_ciclo} m³f</span>", unsafe_allow_html=True)
    d2.write(f"<span class='stat-label'>Vol. Salamoia</span><br><span class='stat-value'>{(sale_rig*3):.1f} L</span>", unsafe_allow_html=True)
    d3.write(f"<span class='stat-label'>Acqua Scarico</span><br><span class='stat-value'>{vr_gest*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO (CON MIX E INTERVALLO GG) ---
with tab4:
    st.header("📐 Progettazione e Analisi di Risparmio")
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        d_in_pro = st.number_input("Durezza Ingresso (°f)", min_value=1, value=35)
        d_mix_pro = st.number_input("Durezza Mix Desiderata (°f)", min_value=0, value=15)
    with cp2:
        if tipo == "Villetta":
            u_val = st.number_input("Numero Persone", min_value=1, value=4)
            cons_gg = u_val * 0.20
            q_picco = 1.20
        else:
            u_val = st.number_input("Numero Appartamenti", min_value=1, value=10)
            cons_gg = (u_val * 3) * 0.20
            q_picco = round(0.20 * math.sqrt(u_val * 3) + 0.8, 2)

    d_delta = max(0.1, d_in_pro - d_mix_pro) # Durezza da abbattere
    resina_nec = (cons_gg * 4 * d_delta) / 5 # Dimensionato su 4 giorni
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_nec] or [max(taglie)])
    
    autonomia_p = (taglia_scelta * 5) / d_delta
    intervallo_p = autonomia_p / cons_gg if cons_gg > 0 else 0

    st.markdown(f'<div class="result-box">Taglia Suggerita: <span class="valore-evidenziato">{taglia_scelta} Litri</span><br>Intervallo Rigenerazione: <b>Ogni {intervallo_p:.1f} giorni</b></div>', unsafe_allow_html=True)

    # --- LOGICA CONFRONTO ANNUALE ---
    m3_anno = cons_gg * 365
    rig_anno = m3_anno / autonomia_p if autonomia_p > 0 else 0
    sale_std = (taglia_scelta * 0.14) * rig_anno
    acqua_std = (taglia_scelta * 7 * rig_anno) / 1000
    sale_clack = sale_std * 0.75
    acqua_clack = acqua_std * 0.75

    st.markdown('<p class="titolo-sezione">📊 Confronto Annuale: Standard vs Clack</p>', unsafe_allow_html=True)
    st.table({
        "Parametro Annuo": ["Sale Totale (kg)", "Sacchi da 25kg", "Acqua Scarico (m³)", "N. Rigenerazioni"],
        "Valvola Standard": [f"{sale_std:.1f}", f"{math.ceil(sale_std/25)}", f"{acqua_std:.2f}", f"{rig_anno:.0f}"],
        "Clack Impression": [f"{sale_clack:.1f}", f"{math.ceil(sale_clack/25)}", f"{acqua_clack:.2f}", "Variabile (Ottimizzata)"]
    })

    risparmio_kg = sale_std - sale_clack
    risparmio_sacchi = math.ceil(sale_std/25) - math.ceil(sale_clack/25)
    
    st.markdown(f"""
    <div class="comparison-card">
        <h4>💰 Risparmio Stimato con Clack</h4>
        • <b>{risparmio_kg:.1f} kg</b> di sale risparmiati all'anno<br>
        • Circa <b>{risparmio_sacchi} sacchi</b> di sale in meno<br>
        • Portata di Picco (UNI 9182): <b>{q_picco} m³/h</b>
    </div>
    """, unsafe_allow_html=True)
