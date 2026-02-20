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
    .label-pro { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione UNI 9182 Attivo")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ereditato dalla Light) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Parametri cloro sotto controllo.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ADDOLCITORI (Macchine Esistenti) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = di_gest - do_gest
    if da_gest > 0:
        m3_ciclo = (vr_gest * 5) / da_gest
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_ciclo:.2f} m³</span><br>Rigenerazione ogni {m3_ciclo/co_gest:.1f} giorni</div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Dimensionamento UNI 9182) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        durezza_pro = st.number_input("Durezza da abbattere (°f)", value=25, help="Differenza tra durezza ingresso e uscita desiderata")
    
    with cp2:
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 # 200 litri/testa
            # Portata di picco semplificata per villetta (doccia + rubinetto)
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 # Media 3 persone/app
            cons_pro = persone * 0.200
            # Formula contemporaneità UNI 9182
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO
    # 1. Volume resina per avere almeno 3-4 giorni di autonomia (evita usura valvola)
    resina_consigliata = (cons_pro * 3 * durezza_pro) / 5
    # Arrotondamento a taglie commerciali standard
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_consigliata] or [max(taglie)])

    st.subheader("🛠 Configurazione Impianto Suggerita")
    st.markdown(f"""
    <div class="result-box">
        <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
        <p style="margin-top:10px;"><b>Requisiti Tecnici minimi:</b><br>
        • Portata Valvola: > {picco_pro} m³/h (in esercizio)<br>
        • Autonomia stimata: {((taglia_scelta*5)/durezza_pro)/cons_pro:.1f} giorni</p>
    </div>
    """, unsafe_allow_html=True)
    
    if picco_pro > 2.5:
        st.warning("⚠️ ATTENZIONE: La portata di picco richiede una valvola da almeno 1\" 1/4 o 1\" 1/2.")
    else:
        st.success("✅ Una valvola standard da 1\" è sufficiente per questa portata.")import streamlit as st
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
    .label-pro { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione UNI 9182 Attivo")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ereditato dalla Light) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Parametri cloro sotto controllo.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ADDOLCITORI (Macchine Esistenti) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = di_gest - do_gest
    if da_gest > 0:
        m3_ciclo = (vr_gest * 5) / da_gest
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_ciclo:.2f} m³</span><br>Rigenerazione ogni {m3_ciclo/co_gest:.1f} giorni</div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Dimensionamento UNI 9182) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        durezza_pro = st.number_input("Durezza da abbattere (°f)", value=25, help="Differenza tra durezza ingresso e uscita desiderata")
    
    with cp2:
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 # 200 litri/testa
            # Portata di picco semplificata per villetta (doccia + rubinetto)
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 # Media 3 persone/app
            cons_pro = persone * 0.200
            # Formula contemporaneità UNI 9182
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO
    # 1. Volume resina per avere almeno 3-4 giorni di autonomia (evita usura valvola)
    resina_consigliata = (cons_pro * 3 * durezza_pro) / 5
    # Arrotondamento a taglie commerciali standard
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_consigliata] or [max(taglie)])

    st.subheader("🛠 Configurazione Impianto Suggerita")
    st.markdown(f"""
    <div class="result-box">
        <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
        <p style="margin-top:10px;"><b>Requisiti Tecnici minimi:</b><br>
        • Portata Valvola: > {picco_pro} m³/h (in esercizio)<br>
        • Autonomia stimata: {((taglia_scelta*5)/durezza_pro)/cons_pro:.1f} giorni</p>
    </div>
    """, unsafe_allow_html=True)
    
    if picco_pro > 2.5:
        st.warning("⚠️ ATTENZIONE: La portata di picco richiede una valvola da almeno 1\" 1/4 o 1\" 1/2.")
    else:
        st.success("✅ Una valvola standard da 1\" è sufficiente per questa portata.")import streamlit as st
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
    .label-pro { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione UNI 9182 Attivo")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ereditato dalla Light) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Parametri cloro sotto controllo.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ADDOLCITORI (Macchine Esistenti) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = di_gest - do_gest
    if da_gest > 0:
        m3_ciclo = (vr_gest * 5) / da_gest
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_ciclo:.2f} m³</span><br>Rigenerazione ogni {m3_ciclo/co_gest:.1f} giorni</div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Dimensionamento UNI 9182) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        durezza_pro = st.number_input("Durezza da abbattere (°f)", value=25, help="Differenza tra durezza ingresso e uscita desiderata")
    
    with cp2:
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 # 200 litri/testa
            # Portata di picco semplificata per villetta (doccia + rubinetto)
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 # Media 3 persone/app
            cons_pro = persone * 0.200
            # Formula contemporaneità UNI 9182
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO
    # 1. Volume resina per avere almeno 3-4 giorni di autonomia (evita usura valvola)
    resina_consigliata = (cons_pro * 3 * durezza_pro) / 5
    # Arrotondamento a taglie commerciali standard
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_consigliata] or [max(taglie)])

    st.subheader("🛠 Configurazione Impianto Suggerita")
    st.markdown(f"""
    <div class="result-box">
        <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
        <p style="margin-top:10px;"><b>Requisiti Tecnici minimi:</b><br>
        • Portata Valvola: > {picco_pro} m³/h (in esercizio)<br>
        • Autonomia stimata: {((taglia_scelta*5)/durezza_pro)/cons_pro:.1f} giorni</p>
    </div>
    """, unsafe_allow_html=True)
    
    if picco_pro > 2.5:
        st.warning("⚠️ ATTENZIONE: La portata di picco richiede una valvola da almeno 1\" 1/4 o 1\" 1/2.")
    else:
        st.success("✅ Una valvola standard da 1\" è sufficiente per questa portata.")import streamlit as st
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
    .label-pro { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione UNI 9182 Attivo")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ereditato dalla Light) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Parametri cloro sotto controllo.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ADDOLCITORI (Macchine Esistenti) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = di_gest - do_gest
    if da_gest > 0:
        m3_ciclo = (vr_gest * 5) / da_gest
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_ciclo:.2f} m³</span><br>Rigenerazione ogni {m3_ciclo/co_gest:.1f} giorni</div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Dimensionamento UNI 9182) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        durezza_pro = st.number_input("Durezza da abbattere (°f)", value=25, help="Differenza tra durezza ingresso e uscita desiderata")
    
    with cp2:
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 # 200 litri/testa
            # Portata di picco semplificata per villetta (doccia + rubinetto)
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 # Media 3 persone/app
            cons_pro = persone * 0.200
            # Formula contemporaneità UNI 9182
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO
    # 1. Volume resina per avere almeno 3-4 giorni di autonomia (evita usura valvola)
    resina_consigliata = (cons_pro * 3 * durezza_pro) / 5
    # Arrotondamento a taglie commerciali standard
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_consigliata] or [max(taglie)])

    st.subheader("🛠 Configurazione Impianto Suggerita")
    st.markdown(f"""
    <div class="result-box">
        <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
        <p style="margin-top:10px;"><b>Requisiti Tecnici minimi:</b><br>
        • Portata Valvola: > {picco_pro} m³/h (in esercizio)<br>
        • Autonomia stimata: {((taglia_scelta*5)/durezza_pro)/cons_pro:.1f} giorni</p>
    </div>
    """, unsafe_allow_html=True)
    
    if picco_pro > 2.5:
        st.warning("⚠️ ATTENZIONE: La portata di picco richiede una valvola da almeno 1\" 1/4 o 1\" 1/2.")
    else:
        st.success("✅ Una valvola standard da 1\" è sufficiente per questa portata.")import streamlit as st
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
    .label-pro { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione UNI 9182 Attivo")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ereditato dalla Light) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Parametri cloro sotto controllo.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ADDOLCITORI (Macchine Esistenti) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = di_gest - do_gest
    if da_gest > 0:
        m3_ciclo = (vr_gest * 5) / da_gest
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_ciclo:.2f} m³</span><br>Rigenerazione ogni {m3_ciclo/co_gest:.1f} giorni</div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Dimensionamento UNI 9182) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        durezza_pro = st.number_input("Durezza da abbattere (°f)", value=25, help="Differenza tra durezza ingresso e uscita desiderata")
    
    with cp2:
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 # 200 litri/testa
            # Portata di picco semplificata per villetta (doccia + rubinetto)
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 # Media 3 persone/app
            cons_pro = persone * 0.200
            # Formula contemporaneità UNI 9182
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO
    # 1. Volume resina per avere almeno 3-4 giorni di autonomia (evita usura valvola)
    resina_consigliata = (cons_pro * 3 * durezza_pro) / 5
    # Arrotondamento a taglie commerciali standard
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_consigliata] or [max(taglie)])

    st.subheader("🛠 Configurazione Impianto Suggerita")
    st.markdown(f"""
    <div class="result-box">
        <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
        <p style="margin-top:10px;"><b>Requisiti Tecnici minimi:</b><br>
        • Portata Valvola: > {picco_pro} m³/h (in esercizio)<br>
        • Autonomia stimata: {((taglia_scelta*5)/durezza_pro)/cons_pro:.1f} giorni</p>
    </div>
    """, unsafe_allow_html=True)
    
    if picco_pro > 2.5:
        st.warning("⚠️ ATTENZIONE: La portata di picco richiede una valvola da almeno 1\" 1/4 o 1\" 1/2.")
    else:
        st.success("✅ Una valvola standard da 1\" è sufficiente per questa portata.")import streamlit as st
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
    .label-pro { color: #FF4B4B; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 **VERSIONE PRO**\nModulo Progettazione UNI 9182 Attivo")

st.title("🧪 Suite Calcoli PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: POOL ASSISTANT (Ereditato dalla Light) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato: **{cl_combinato:.2f} ppm**")
    
    if st.button("🚀 CALCOLA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        if cl_combinato >= 0.4:
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Parametri cloro sotto controllo.")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE ADDOLCITORI (Macchine Esistenti) ---
with tab3:
    st.header("🚰 Verifica Impianto Esistente")
    ca1, ca2 = st.columns(2)
    with ca1:
        vr_gest = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        di_gest = st.number_input("Durezza Entrata (°f)", min_value=1, value=35)
    with ca2:
        do_gest = st.number_input("Durezza Uscita (°f)", min_value=0, value=15)
        co_gest = st.number_input("Consumo Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    da_gest = di_gest - do_gest
    if da_gest > 0:
        m3_ciclo = (vr_gest * 5) / da_gest
        st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{m3_ciclo:.2f} m³</span><br>Rigenerazione ogni {m3_ciclo/co_gest:.1f} giorni</div>', unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Dimensionamento UNI 9182) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        durezza_pro = st.number_input("Durezza da abbattere (°f)", value=25, help="Differenza tra durezza ingresso e uscita desiderata")
    
    with cp2:
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 # 200 litri/testa
            # Portata di picco semplificata per villetta (doccia + rubinetto)
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 # Media 3 persone/app
            cons_pro = persone * 0.200
            # Formula contemporaneità UNI 9182
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO
    # 1. Volume resina per avere almeno 3-4 giorni di autonomia (evita usura valvola)
    resina_consigliata = (cons_pro * 3 * durezza_pro) / 5
    # Arrotondamento a taglie commerciali standard
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie if t >= resina_consigliata] or [max(taglie)])

    st.subheader("🛠 Configurazione Impianto Suggerita")
    st.markdown(f"""
    <div class="result-box">
        <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
        <p style="margin-top:10px;"><b>Requisiti Tecnici minimi:</b><br>
        • Portata Valvola: > {picco_pro} m³/h (in esercizio)<br>
        • Autonomia stimata: {((taglia_scelta*5)/durezza_pro)/cons_pro:.1f} giorni</p>
    </div>
    """, unsafe_allow_html=True)
    
    if picco_pro > 2.5:
        st.warning("⚠️ ATTENZIONE: La portata di picco richiede una valvola da almeno 1\" 1/4 o 1\" 1/2.")
    else:
        st.success("✅ Una valvola standard da 1\" è sufficiente per questa portata.")
