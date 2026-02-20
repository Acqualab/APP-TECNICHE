import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Suite", page_icon="💧", layout="centered")

# --- STILE CSS UNIVERSALE ---
st.markdown("""
    <style>
    .misura-grande { font-size: 36px !important; font-weight: bold; color: #FF4B4B; margin-left: 5px; }
    .nome-prodotto { font-size: 17px; font-weight: 600; color: var(--text-color); }
    .unita-misura { font-size: 18px; color: #00AEEF; font-weight: bold; }
    .result-box { 
        padding: 12px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.3); 
        background-color: rgba(128, 128, 128, 0.05); margin-bottom: 10px; 
    }
    .metric-card {
        background-color: rgba(0, 174, 239, 0.05); padding: 15px; border-radius: 10px;
        border-left: 5px solid #00AEEF; margin-bottom: 10px;
    }
    .highlight-red { font-size: 22px; font-weight: bold; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR LOGO ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.title("🧪 Suite Professionale Acqualab")

# --- DEFINIZIONE TAB ---
tab_pool, tab_sol, tab_add_dim, tab_add_cons = st.tabs([
    "🏊 Pool Assistant", "💧 Soluzione", "🏢 Addolcitori: Progetto", "🧂 Addolcitori: Consumi"
])

# ==========================================
# TAB 1: POOL ASSISTANT
# ==========================================
with tab_pool:
    st.header("Analisi Piscina")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0, key="pool_v")
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
        cl_tot = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    with c2:
        cl_lib = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)
        sale_ril = st.number_input("Sale (mg/L - ppm)", min_value=0.0, value=0.0, step=100.0)
    
    cl_comb = max(0.0, cl_tot - cl_lib)
    st.info(f"💡 Cloro Combinato (CC): **{cl_comb:.2f} ppm**")

    if st.button("🚀 CALCOLA DOSAGGI PISCINA", type="primary", use_container_width=True):
        st.divider()
        # Sezione Sale
        st.subheader("🧂 Sale")
        sale_gl = sale_ril / 1000
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">Standard (4.5):</span> <span class="misura-grande">{max(0.0, (4.5-sale_gl)*v_piscina):.1f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        # Sezione pH
        st.subheader("📊 pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">pH meno G:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        elif ph_ril < 7.2:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">pH Plus:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        # Sezione Cloro & Shock
        st.subheader("💥 Cloro & Shock")
        if cl_lib < 1.5:
            d_cl = 1.5 - cl_lib
            st.write(f"Integrazione Ripristino (+{d_cl:.1f} ppm):")
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        if cl_comb >= 0.4:
            st.warning(f"Shock necessario per Breakpoint (CC: {cl_comb:.2f})")
            ppm_shock = max(0.0, (cl_comb * 10) - cl_lib)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

        # Sezione Alghicida e CYA
        st.subheader("🌿 Altri")
        cya_reale = cya_ril / 2
        st.write(f"Cianurico Reale: {cya_reale:.1f} ppm")
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🌿 Algiprevent Mantenimento:</span> <span class="misura-grande">{(v_piscina*1)/100:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: SOLUZIONE
# ==========================================
with tab_sol:
    st.header("Preparazione Vasca Soluzione")
    v_v = st.number_input("Volume Vasca (L)", min_value=0.0, value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", min_value=0.0, value=10.0)
    p_c = st.number_input("% Prodotto Commerciale", min_value=0.0, value=15.0)
    if v_v > 0:
        st.success(f"### ✅ Programmazione: {(l_i / v_v) * p_c:.2f} %")

# ==========================================
# TAB 3: ADDOLCITORI - PROGETTO
# ==========================================
with tab_add_dim:
    st.header("🏢 Dimensionamento Impianto")
    c_d1, c_d2 = st.columns(2)
    with c_d1:
        dur_in = st.number_input("Durezza Entrata (°f)", value=35, key="add_in")
    with c_d2:
        dur_out = st.number_input("Durezza Uscita (°f)", value=15, key="add_out")
    
    dur_abb = max(0, dur_in - dur_out)
    tipo = st.radio("Tipo:", ["Villetta", "Condominio"])
    
    if tipo == "Villetta":
        persone = st.number_input("Persone", value=4)
        m3_giorno = persone * 0.2
        picco = 1.2
    else:
        app = st.number_input("Appartamenti", value=10)
        m3_giorno = app * 3 * 0.2
        picco = round(0.20 * math.sqrt(app * 3) + 0.8, 2)

    st.divider()
    col_a, col_b = st.columns(2)
    col_a.markdown(f'<div class="metric-card">Consumo Stimato:<br><span class="highlight-red">{m3_giorno:.2f} m³/g</span></div>', unsafe_allow_html=True)
    col_b.markdown(f'<div class="metric-card">Portata Picco:<br><span class="highlight-red">{picco:.2f} m³/h</span></div>', unsafe_allow_html=True)
    
    v_res_cons = (m3_giorno * 4 * dur_abb) / 5
    st.success(f"🛠 Taglia consigliata per 4gg autonomia: **{math.ceil(v_res_cons)} Litri**")

# ==========================================
# TAB 4: ADDOLCITORI - CONSUMI
# ==========================================
with tab_add_cons:
    st.header("🧂 Gestione e Costi")
    v_eff = st.number_input("Volume Resina Macchina (L)", value=25)
    
    # Riutilizzo valori da Tab 3 se possibile
    cap_c = v_eff * 5
    m3_c = cap_c / dur_abb if dur_abb > 0 else 0
    gg_aut = m3_c / m3_giorno if m3_giorno > 0 else 0
    s_rig = v_eff * 0.14
    
    st.markdown(f"""
    <div class="result-box">
    🌊 Acqua per ciclo: <b>{m3_c:.2f} m³</b><br>
    📅 Rigenerazione ogni: <b>{gg_aut:.1f} giorni</b><br>
    🧂 Sale per rigenerazione: <b>{s_rig:.2f} kg</b><br>
    🧪 Salamoia: <b>{s_rig * 3:.1f} Litri</b>
    </div>
    """, unsafe_allow_html=True)
    
    s_anno = (365/gg_aut) * s_rig if gg_aut > 0 else 0
    st.write(f"📦 Consumo annuale: **{math.ceil(s_anno/25)} sacchi** da 25kg")
