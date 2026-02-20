import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO - Enterprise", page_icon="🏢", layout="centered")

# --- STILE CSS AVANZATO ---
st.markdown("""
    <style>
    .misura-grande { font-size: 36px !important; font-weight: bold; color: #FF4B4B; }
    .valore-evidenziato { font-size: 32px !important; font-weight: bold; color: #00AEEF; }
    .result-box { padding: 20px; border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 15px; text-align: center; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 15px; margin-top: 15px; }
    .stat-label { font-size: 14px; color: gray; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.title("🧪 Suite Calcoli PRO")

# Definizione sicura dei Tab
tab1, tab2, tab3, tab4 = st.tabs(["🏊 Piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto & Risparmio"])

# --- TAB 1 & 2 (Logiche standard) ---
with tab1: st.header("Analisi Piscina")
with tab2: st.header("Soluzione Dosaggio")

# --- TAB 3: GESTIONE (Replica Light Totale) ---
with tab3:
    st.header("🚰 Verifica Macchina Installata")
    st.markdown('<p class="titolo-sezione">Parametri Impianto</p>', unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        vr = st.number_input("Volume Resina (L)", value=25, key="vr_g")
        di = st.number_input("Durezza Entrata (°f)", value=35, key="di_g")
    with g2:
        do = st.number_input("Durezza Uscita (°f)", value=15, key="do_g")
        co = st.number_input("Consumo (m³/gg)", value=0.60, key="co_g")
    
    delta = max(0.1, di - do)
    cap_c = vr * 5
    m3_c = cap_c / delta
    s_rig = (vr * 140) / 1000

    st.markdown('<p class="titolo-sezione">Risultati Tecnici</p>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    r1.metric("Produzione Acqua Dolce", f"{m3_c:.2f} m³", f"Ogni {m3_c/co:.1f} gg")
    r2.metric("Consumo Sale", f"{s_rig:.2f} kg", "A rigenerazione")

    st.markdown("---")
    d1, d2, d3 = st.columns(3)
    d1.write(f"<span class='stat-label'>Cap. Ciclica</span><br><span class='stat-value'>{cap_c} m³f</span>", unsafe_allow_html=True)
    d2.write(f"<span class='stat-label'>Salamoia</span><br><span class='stat-value'>{(s_rig*3):.1f} L</span>", unsafe_allow_html=True)
    d3.write(f"<span class='stat-label'>Scarico</span><br><span class='stat-value'>{vr*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO & CONFRONTO ESAUSTIVO ---
with tab4:
    st.header("📐 Progettazione e Risparmio")
    
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

    p_delta = max(0.1, p_in - p_out)
    res_nec = (f_gg * 3 * p_delta) / 5
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    scelta = min([t for t in taglie if t >= res_nec] or [max(taglie)])
    
    # Calcoli Annuali
    m3_disp = (scelta * 5) / p_delta
    g_int = m3_disp / f_gg
    n_rig = 365 / g_int
    
    # Standard vs Clack
    sale_std = (scelta * 0.14) * n_rig
    acqua_std = (scelta * 7 * n_rig) / 1000
    
    sale_clack = sale_std * 0.80
    acqua_clack = acqua_std * 0.80

    st.markdown(f'<div class="result-box">Taglia Suggerita: <span class="valore-evidenziato">{scelta} Litri Resina</span></div>', unsafe_allow_html=True)

    st.table({
        "Dati Annuali": ["Sale Totale", "Sacchi (25kg)", "Acqua Scarico", "N. Rigenerazioni"],
        "Valvola Standard": [f"{sale_std:.0f} kg", f"{math.ceil(sale_std/25)}", f"{acqua_std:.2f} m³", f"{n_rig:.0f}"],
        "Clack Impression": [f"{sale_clack:.0f} kg", f"{math.ceil(sale_clack/25)}", f"{acqua_clack:.2f} m³", "Ottimizzata"]
    })

    st.success(f"📉 **Risparmio Clack:** {sale_std - sale_clack:.0f} kg di sale e { (acqua_std - acqua_clack)*1000 :.0f} L d'acqua all'anno.")
