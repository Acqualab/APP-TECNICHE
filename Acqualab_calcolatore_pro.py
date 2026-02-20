import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO - Clack Edition", page_icon="🏢", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .misura-grande { font-size: 36px !important; font-weight: bold; color: #FF4B4B; }
    .valore-evidenziato { font-size: 32px !important; font-weight: bold; color: #00AEEF; }
    .result-box { padding: 20px; border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 15px; text-align: center; }
    .titolo-sezione { font-size: 22px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 20px; margin-top: 15px; }
    .label-risparmio { color: #28a745; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Assistente Piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto & Risparmio"])

# ... (Tab 1, 2 e 3 rimangono invariati rispetto alla versione precedente)

# --- TAB 4: PROGETTO AVANZATO & CLACK IMPRESSION ---
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
        # 1. Dimensionamento Taglia
        res_nec = (fabb_gg * 3 * d_netta) / 5 
        taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
        scelta = min([t for t in taglie if t >= res_nec] or [max(taglie)])
        
        # 2. Metriche richieste (Disponibilità per ciclo e intervallo)
        cap_ciclica = scelta * 5
        m3_disponibili = cap_ciclica / d_netta
        giorni_intervallo = m3_disponibili / fabb_gg
        
        # 3. Consumi tecnici per rigenerazione
        acqua_rig = scelta * 7 # Litri medi per rigenerazione
        sale_rig = (scelta * 140) / 1000 # kg sale per rigenerazione
        
        # 4. Statistiche Annuali Standard
        n_rig_anno = 365 / giorni_intervallo
        acqua_rig_annua = acqua_rig * n_rig_anno
        sale_anno_standard = sale_rig * n_rig_anno
        m3_anno_utenza = fabb_gg * 365

        st.markdown(f'<div class="result-box"><span class="nome-prodotto">Taglia Consigliata:</span><br><span class="valore-evidenziato" style="font-size:45px !important;">{scelta} Litri Resina</span></div>', unsafe_allow_html=True)

        st.markdown('<p class="titolo-sezione">Dettagli Ciclo e Autonomia</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Acqua per Ciclo", f"{m3_disponibili:.2f} m³")
        col2.metric("Intervallo Rig.", f"{giorni_intervallo:.1f} gg")
        col3.metric("Acqua Scarico", f"{acqua_rig} L")

        st.markdown('<p class="titolo-sezione">💡 Analisi Clack Impression (Proporzionale)</p>', unsafe_allow_html=True)
        st.write("Confronto tra addolcitore standard e sistema a rigenerazione proporzionale Clack Impression.")
        
        # Stima risparmio Clack (tipicamente 15-20% su sale e acqua grazie al calcolo del reale consumo)
        perc_risparmio = 0.18 # 18% medio
        risparmio_sale = sale_anno_standard * perc_risparmio
        risparmio_acqua = acqua_rig_annua * perc_risparmio
        
        c_clack1, c_clack2 = st.columns(2)
        with c_clack1:
            st.write("📉 **Risparmio Annuo Stimato**")
            st.markdown(f'<span class="label-risparmio">-{risparmio_sale:.1f} kg di Sale</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="label-risparmio">-{risparmio_acqua:.0f} L di Acqua</span>', unsafe_allow_html=True)
        
        with c_clack2:
            st.write("📊 **Consumi Totali con Clack**")
            st.write(f"Sale annuo: **{(sale_anno_standard - risparmio_sale)/25:.0f} sacchi**")
            st.write(f"Acqua scarico annua: **{(acqua_rig_annua - risparmio_acqua)/1000:.2f} m³**")

        st.info(f"⚙️ **Nota Tecnica:** La valvola Clack Impression ottimizza la salamoia in base all'esaurimento reale. I valori sopra sono stime basate su un utilizzo medio dell'utenza.")
    else:
        st.error("Verificare i parametri di durezza.")
