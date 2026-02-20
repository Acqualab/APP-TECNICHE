import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO - Comparison", page_icon="🏢", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .misura-grande { font-size: 36px !important; font-weight: bold; color: #FF4B4B; }
    .valore-evidenziato { font-size: 32px !important; font-weight: bold; color: #00AEEF; }
    .result-box { padding: 20px; border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 15px; text-align: center; }
    .titolo-sezione { font-size: 22px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 20px; margin-top: 15px; }
    .green-text { color: #28a745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Assistente Piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto & Confronto"])

# I primi 3 tab mantengono la logica consolidata...

# --- TAB 4: PROGETTO & CONFRONTO ESAUSTIVO ---
with tab4:
    st.header("📐 Progettazione e Analisi dei Consumi")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"], key="p_tipo")
        d_in = st.number_input("Durezza Ingresso (°f)", value=35, key="p_din")
        d_out = st.number_input("Durezza Uscita desiderata (°f)", value=15, key="p_dout")
    with cp2:
        if tipo == "Villetta":
            u_val = st.number_input("Numero Persone", value=4, key="p_pers")
            fabb_gg = u_val * 0.20
            q_picco = 1.20
        else:
            u_val = st.number_input("Numero Appartamenti", value=10, key="p_app")
            fabb_gg = (u_val * 3) * 0.20
            q_picco = round(0.20 * math.sqrt(u_val * 3) + 0.8, 2)

    d_netta = max(0, d_in - d_out)
    
    if d_netta > 0:
        # 1. Dimensionamento Taglia (3 giorni autonomia)
        res_nec = (fabb_gg * 3 * d_netta) / 5 
        taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
        scelta = min([t for t in taglie if t >= res_nec] or [max(taglie)])
        
        # 2. Dati Ciclo
        cap_ciclica = scelta * 5 #
        m3_disponibili = cap_ciclica / d_netta #
        g_intervallo = m3_disponibili / fabb_gg #
        
        # 3. Consumi Standard (per confronto)
        acqua_rig = scelta * 7 #
        sale_rig = (scelta * 140) / 1000 #
        n_rig_anno = 365 / g_intervallo
        
        # Totali Standard
        sale_std_anno = sale_rig * n_rig_anno #
        acqua_std_anno = (acqua_rig * n_rig_anno) / 1000
        
        # 4. Totali Clack Impression (Risparmio medio 20% su sale/acqua)
        sale_clack_anno = sale_std_anno * 0.80
        acqua_clack_anno = acqua_std_anno * 0.80

        st.markdown(f'<div class="result-box"><span class="nome-prodotto">Taglia Consigliata:</span><br><span class="valore-evidenziato">{scelta} Litri Resina</span></div>', unsafe_allow_html=True)

        st.markdown('<p class="titolo-sezione">📊 Report Efficienza: Standard vs Clack</p>', unsafe_allow_html=True)
        
        # Tabella di confronto
        st.write("Confronto basato su consumo annuo stimato:")
        st.table({
            "Parametro": ["Cap. Ciclica", "Intervallo Rig.", "Sale Annuo", "Sacchi (25kg)", "Acqua Scarico"],
            "Valvola Standard": [f"{cap_ciclica} m³f", f"{g_intervallo:.1f} gg", f"{
