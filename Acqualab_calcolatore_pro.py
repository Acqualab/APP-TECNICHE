import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Acqualab PRO - Suite Tecnica", 
    page_icon="🏢", 
    layout="centered"
)

# --- STILE CSS PROFESSIONALE ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .misura-grande { font-size: 38px !important; font-weight: bold; color: #FF4B4B; margin-left: 10px; }
    .valore-evidenziato { font-size: 30px !important; font-weight: bold; color: #00AEEF; }
    .nome-prodotto { font-size: 18px; font-weight: 600; color: #333; }
    .unita-misura { font-size: 18px; color: #00AEEF; font-weight: bold; }
    .result-box { 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid rgba(128, 128, 128, 0.2); 
        background-color: white; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px; 
    }
    .titolo-sezione { 
        font-size: 22px; 
        font-weight: bold; 
        color: #1E3A8A; 
        border-bottom: 3px solid #00AEEF; 
        padding-bottom: 5px;
        margin-bottom: 20px; 
        margin-top: 25px; 
    }
    .stat-label { font-size: 12px; color: #6B7280; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 20px; font-weight: bold; color: #111827; display: block; }
    .highlight-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #00AEEF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR TECNICA ---
with st.sidebar:
    try:
        st.image("Color con payoff - senza sfondo.png", use_container_width=True)
    except:
        st.title("ACQUALAB S.R.L.")
    st.markdown("---")
    st.subheader("Parametri Economici")
    costo_sale_sacco = st.number_input("Costo Sale (€/25kg)", value=12.0)
    st.markdown("---")
    st.info("🛠 **ENGINEERING MODE**\nModulo Progettazione UNI 9182 Rev. 2026")
    st.write("Versione: 2.1.0-PRO")

st.title("🧪 Suite Progettazione Acqualab")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione Impianto", "📐 Progetto Nuovo"])

# --- TAB 1: POOL ASSISTANT ---
with tab1:
    st.header("Analisi Chimica e Interventi Correttivi")
    col1, col2 = st.columns(2)
    with col1:
        vol_p = st.number_input("Volume Vasca (m³)", min_value=1.0, value=80.0, step=10.0)
        ph_r = st.number_input("pH Analizzato", min_value=0.0, max_value=14.0, value=7.9, step=0.1)
    with col2:
        cl_l = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=0.8, step=0.1)
        cl_t = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.4, step=0.1)
    
    cl_comb = max(0.0, cl_t - cl_l)
    st.warning(f"⚠️ Cloro Combinato rilevato: **{cl_comb:.2f} ppm**")
    
    if st.button("🚀 GENERA REPORT DOSAGGI", use_container_width=True):
        st.markdown('<p class="titolo-sezione">Piano d\'intervento</p>', unsafe_allow_html=True)
        r_col1, r_col2 = st.columns(2)
        
        if ph_r > 7.4:
            kg_ph_m = (vol_p * 10 * ((ph_r - 7.2) / 0.1)) / 1000
            r_col1.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH meno Granulare</span><br><span class="misura-grande">{kg_ph_m:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        if cl_comb >= 0.4:
            fabbisogno_ppm = max(0.0, (cl_comb * 10) - cl_l)
            kg_shock = (vol_p * 1.5 * fabbisogno_ppm) / 1000
            r_col2.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70</span><br><span class="misura-grande">{kg_shock:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Analisi Cloro conforme: nessuna clorazione d'urto necessaria.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Calcolo Concentrazione Soluzione")
    st.write("Utilizzare questo modulo per la preparazione delle vasche di dosaggio.")
    with st.container():
        c_v1, c_v2 = st.columns(2)
        v_vasca = c_v1.number_input("Volume Acqua in Vasca (L)", value=100.0)
        l_prodotto = c_v1.number_input("Litri Prodotto Puro Aggiunti (L)", value=10.0)
        p_comm = c_v2.number_input("Concentrazione Prodotto (%)", value=15.0)
        
        risultato_perc = (l_prodotto / v_vasca) * p_comm if v_vasca > 0 else 0
        st.success(f"### 🎯 Concentrazione Finale: {risultato_perc:.2f} %")

# --- TAB 3: GESTIONE IMPIANTO ESISTENTE ---
with tab3:
    st.header("🚰 Verifica Diagnostica Addolcitore")
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        vr_es = st.number_input("Resina Installata (Litri)", value=30)
        de_es = st.number_input("Durezza Ingresso (°f)", value=40)
    with g_col2:
        du_es = st.number_input("Durezza Uscita Desiderata (°f)", value=15)
        co_es = st.number_input("Consumo Giornaliero (m³/gg)", value=0.8)

    d_da_togliere = max(0.1, de_es - du_es)
    cap_ciclo = vr_es * 5
    m3_autonomia = cap_ciclo / d_da_togliere
    sale_per_ciclo = (vr_es * 140) / 1000  # 140g per litro resina
    intervallo_es = m3_autonomia / co_es if co_es > 0 else 0

    st.markdown('<p class="titolo-sezione">Parametri di Funzionamento</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="result-box">
            Capacità Ciclica: <b>{cap_ciclo} m³f</b> | 
            Autonomia: <span class="valore-evidenziato">{m3_autonomia:.2f} m³</span><br>
            Frequenza Rigenerazione: <b>ogni {intervallo_es:.1f} giorni</b>
        </div>
    """, unsafe_allow_html=True)

    d_res1, d_res2, d_res3 = st.columns(3)
    with d_res1:
        st.markdown(f"<span class='stat-label'>Sale per Rig.</span><br><span class='stat-value'>{sale_per_rig:.2f} kg</span>", unsafe_allow_html=True)
    with d_res2:
        st.markdown(f"<span class='stat-label'>Vol. Salamoia</span><br><span class='stat-value'>{(sale_per_rig*3):.1f} L</span>", unsafe_allow_html=True)
    with d_res3:
        st.markdown(f"<span class='stat-label'>Acqua Scarico</span><br><span class='stat-value'>{vr_es*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO NUOVO IMPIANTO ---
with tab4:
    st.header("📐 Dimensionamento Professionale UNI 9182")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        utenza = st.selectbox("Tipo Utenza", ["Abitazione Singola", "Condominio Plurifamiliare"])
        d_ingresso = st.number_input("Durezza Analizzata (°f)", value=35, key="d_ing")
        d_miscelata = st.number_input("Durezza Mix Finale (°f)", value=15, key="d_mix")
    with p_col2:
        if utenza == "Abitazione Singola":
            persone = st.number_input("Numero Persone", min_value=1, value=4)
            cons_m3_gg = persone * 0.20
            p_picco = 1.20
        else:
            unità = st.number_input("Numero Appartamenti", min_value=1, value=12)
            cons_m3_gg = (unità * 3) * 0.20
            p_picco = round(0.20 * math.sqrt(unità * 3) + 0.8, 2)

    d_netta_pro = max(0.1, d_ingresso - d_miscelata)
    
    # Calcolo taglia ideale per rigenerazione ogni 4 giorni
    litri_resina_ideali = (cons_m3_gg * 4 * d_netta_pro) / 5
    lista_taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_proposta = min([t for t in lista_taglie if t >= litri_resina_ideali] or [300])
    
    m3_ciclo_pro = (taglia_proposta * 5) / d_netta_pro
    gg_intervallo_pro = m3_ciclo_pro / cons_m3_gg

    st.markdown('<p class="titolo-sezione">Specifiche di Progetto</p>', unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Fabbisogno", f"{cons_m3_gg:.2f} m³/gg")
    m_col2.metric("Portata Picco", f"{p_picco:.2f} m³/h")
    m_col3.metric("Durezza Netta", f"{d_netta_pro:.0f} °f")

    st.markdown(f"""
    <div class="highlight-card">
        🎯 <b>CONFIGURAZIONE OTTIMALE:</b> Addolcitore da <b>{taglia_proposta} Litri Resina</b><br>
        • Autonomia ciclica: <b>{m3_ciclo_pro:.2f} m³</b><br>
        • Intervallo rigenerazione: <b>Ogni {gg_intervallo_pro:.1f} giorni</b>
    </div>
    """, unsafe_allow_html=True)

    # --- COMPARATIVA CONSUMI ANNUALI ---
    st.markdown('<p class="titolo-sezione">📊 Analisi dei Consumi e Risparmio (12 mesi)</p>', unsafe_allow_html=True)
    
    n_cicli_anno = 365 / gg_intervallo_pro
    kg_sale_std = (taglia_proposta * 0.14) * n_cicli_anno
    kg_sale_clack = kg_sale_std * 0.82 # Risparmio del 18% con Clack
    
    sacchi_std = math.ceil(kg_sale_std / 25)
    sacchi_clack = math.ceil(kg_sale_clack / 25)
    
    costo_annuo_std = sacchi_std * costo_sale_sacco
    costo_annuo_clack = sacchi_clack * costo_sale_sacco

    st.table({
        "Parametro Annuale": ["Consumo Sale (kg)", "Sacchi (25kg)", "Costo Sale (€)", "Acqua Scarico (m³)"],
        "Valvola Standard": [f"{kg_sale_std:.0f}", f"{sacchi_std}", f"{costo_annuo_std:.2f} €", f"{(taglia_proposta*7*n_cicli_anno)/1000:.2f}"],
        "Clack Impression": [f"{kg_sale_clack:.0f}", f"{sacchi_clack}", f"{costo_annuo_clack:.2f} €", f"{(taglia_proposta*6*n_cicli_anno*0.82)/1000:.2f}"]
    })
    
    risparmio_totale = costo_annuo_std - costo_annuo_clack
    if risparmio_totale > 0:
        st.success(f"💰 Risparmio Economico stimato con tecnologia Proporzionale Clack: **{risparmio_totale:.2f} €/anno**")
