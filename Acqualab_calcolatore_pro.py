import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO", page_icon="🏢", layout="centered")

# --- STILE CSS AVANZATO (Stile Light + PRO) ---
st.markdown("""
    <style>
    .misura-grande { font-size: 36px !important; font-weight: bold; color: #FF4B4B; }
    .valore-evidenziato { font-size: 32px !important; font-weight: bold; color: #00AEEF; }
    .nome-prodotto { font-size: 18px; font-weight: 600; color: var(--text-color); }
    .unita-misura { font-size: 20px; color: #00AEEF; font-weight: bold; }
    .result-box { padding: 20px; border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 15px; text-align: center; }
    .titolo-sezione { font-size: 22px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 20px; margin-top: 15px; }
    .stat-label { font-size: 14px; color: gray; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")
st.sidebar.markdown("---")
st.sidebar.success("🚀 **VERSIONE PRO ATTIVA**")

st.title("🧪 Suite Calcoli PRO")

# Definizione corretta dei 4 Tab per evitare NameError
tab1, tab2, tab3, tab4 = st.tabs(["🏊 Assistente Piscina", "💧 Soluzione", "🚰 Gestione Impianto", "📐 Progetto UNI 9182"])

# --- TAB 1: PISCINA (Completo) ---
with tab1:
    st.header("Analisi e Interventi")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=1.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_lib = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0)
        cl_tot = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0)
    
    cl_comb = max(0.0, cl_tot - cl_lib)
    st.info(f"💡 Cloro Combinato (CC): **{cl_comb:.2f} ppm**")
    
    if st.button("🚀 GENERA DOSAGGI", use_container_width=True):
        st.markdown('<p class="titolo-sezione">Dosaggi Consigliati</p>', unsafe_allow_html=True)
        # Logica pH
        if ph_ril > 7.4:
            st.markdown(f'<div class="result-box">pH meno G: <span class="misura-grande">{(v_piscina*10*((ph_ril-7.2)/0.1))/1000:.2f} kg</span></div>', unsafe_allow_html=True)
        # Logica Cloro Shock
        if cl_comb >= 0.4:
            ppm_shock = (cl_comb * 10) - cl_lib
            st.markdown(f'<div class="result-box">Shock Chemacal 70: <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f} kg</span></div>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_vasca = st.number_input("Volume Vasca Soluzione (L)", value=100.0)
    l_prod = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_comm = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Programmazione Pompa: {(l_prod/v_vasca)*p_comm if v_vasca > 0 else 0:.2f} %")

# --- TAB 3: GESTIONE (Replica Grafica Light) ---
with tab3:
    st.header("🚰 Verifica Macchina Installata")
    st.markdown('<p class="titolo-sezione">1. Parametri Impianto</p>', unsafe_allow_html=True)
    cg1, cg2 = st.columns(2)
    with cg1:
        vr_g = st.number_input("Volume Resina (Litri)", value=25, key="vr_g")
        di_g = st.number_input("Durezza Acqua Grezza (°f)", value=35, key="di_g")
    with cg2:
        do_g = st.number_input("Durezza Miscelata Uscita (°f)", value=15, key="do_g")
        co_g = st.number_input("Consumo Acqua Giornaliero (m³)", value=0.6, key="co_g")

    delta_g = max(0, di_g - do_g)
    if delta_g > 0:
        cap_c = vr_g * 5
        m3_c = cap_c / delta_g
        s_rig = (vr_g * 140) / 1000
        
        st.markdown('<p class="titolo-sezione">2. Risultati Calcolo</p>', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.write("🌊 **Produzione Acqua Dolce**")
            st.markdown(f'<div class="result-box"><span class="valore-evidenziato">{m3_c:.2f} m³</span><br>Ogni {m3_c/co_g:.1f} giorni</div>', unsafe_allow_html=True)
        with r2:
            st.write("🧂 **Consumo Sale**")
            st.markdown(f'<div class="result-box"><span class="valore-evidenziato">{s_rig:.2f} kg</span><br>A rigenerazione</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.write("📊 **Dettagli Tecnici:**")
        d1, d2, d3 = st.columns(3)
        d1.write(f"<span class='stat-label'>Cap. Ciclica</span><br><span class='stat-value'>{cap_c} m³f</span>", unsafe_allow_html=True)
        d2.write(f"<span class='stat-label'>Salamoia</span><br><span class='stat-value'>{(s_rig*3):.1f} L</span>", unsafe_allow_html=True)
        d3.write(f"<span class='stat-label'>Scarico</span><br><span class='stat-value'>{(vr_g*7):.0f} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO (Versione PRO con Statistiche Annue) ---
with tab4:
    st.header("📐 Progettazione e Preventivazione")
    st.markdown('<p class="titolo-sezione">Parametri di Progetto</p>', unsafe_allow_html=True)
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        d_in = st.number_input("Durezza Ingresso (°f)", value=35)
        d_out = st.number_input("Durezza Uscita desiderata (°f)", value=15)
    with cp2:
        if tipo == "Villetta":
            pers = st.number_input("Numero Persone", value=4)
            fabb_gg = pers * 0.20
            q_picco = 1.20
        else:
            apps = st.number_input("Numero Appartamenti", value=10)
            fabb_gg = (apps * 3) * 0.20
            q_picco = round(0.20 * math.sqrt(apps * 3) + 0.8, 2)

    d_netta = max(0, d_in - d_out)
    
    if d_netta > 0:
        # Calcolo taglia
        res_nec = (fabb_gg * 3 * d_netta) / 5 # 3 giorni autonomia
        taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
        scelta = min([t for t in taglie if t >= res_nec] or [max(taglie)])
        
        # Calcoli Statistici Annui
        m3_anno = fabb_gg * 365
        sale_anno = (m3_anno * d_netta * 0.028) # 28g di sale per ogni m3 per ogni grado francese
        sacchi_anno = math.ceil(sale_anno / 25)

        st.markdown(f'<div class="result-box"><span class="nome-prodotto">Taglia Addolcitore Consigliata:</span><br><span class="valore-evidenziato" style="font-size:45px !important;">{scelta} Litri Resina</span></div>', unsafe_allow_html=True)

        st.markdown('<p class="titolo-sezione">Statistiche e Consumi Stimati</p>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        s1.metric("Acqua annua", f"{m3_anno:.0f} m³")
        s2.metric("Sale annuo", f"{sale_anno:.0f} kg")
        s3.metric("Sacchi (25kg)", f"{sacchi_anno}")
        
        st.info(f"👉 **Nota Tecnica:** Portata di picco calcolata: **{q_picco} m³/h**. Assicurarsi che la valvola supporti tale flusso.")
