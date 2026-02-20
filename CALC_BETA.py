import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Light Beta", page_icon="💧", layout="centered")

# --- STILE CSS UNIVERSALE (AUTO-ADATTIVO) ---
st.markdown("""
    <style>
    /* Numero gigante rosso - funziona su entrambi i temi */
    .misura-grande {
        font-size: 38px !important;
        font-weight: bold;
        color: #FF4B4B; 
        margin-left: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    /* Nome prodotto - USA IL COLORE DI TESTO DEL TEMA ATTIVO */
    .nome-prodotto {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-color); /* CAMBIA DA SOLO TRA BIANCO E NERO */
    }
    /* Unità di misura in azzurro vivace */
    .unita-misura {
        font-size: 20px;
        color: #00AEEF;
        font-weight: bold;
    }
    /* Box con bordo colorato per far risaltare il contenuto */
    .result-box {
        padding: 12px;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.3);
        background-color: rgba(128, 128, 128, 0.05);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.title("🧪 Suite Calcoli Light Beta")

tab1, tab2 = st.tabs(["🏊 Pool Assistant", "💧 Soluzione"])

# --- TAB 1: POOL ASSISTANT ---
with tab1:
    st.header("Analisi e Interventi")
    
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato (CC): **{cl_combinato:.2f} ppm**")

    st.markdown("---")
    sale_ril_mgl = st.number_input("Sale rilevato (mg/L - ppm)", min_value=0.0, value=0.0, step=100.0)

    if st.button("🚀 CALCOLA TUTTI I DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        
        # 1. SALE
        st.subheader("🧂 Sezione Sale")
        sale_gl = sale_ril_mgl / 1000
        m_std = max(0.0, 4.5 - sale_gl)
        m_ls = max(0.0, 1.5 - sale_gl)
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🧂 Clorinatore Standard (4.5):</span> <span class="misura-grande">{(v_piscina * m_std):.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🧂 Bassa Salinità (1.5):</span> <span class="misura-grande">{(v_piscina * m_ls):.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        # 2. PH
        st.subheader("📊 Correzione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 Carisan pH meno G:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH meno L 15%:</span> <span class="misura-grande">{(v_piscina*27*diff)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH meno L 40%:</span> <span class="misura-grande">{(v_piscina*9*diff)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 pH Plus:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("✅ pH ottimale.")

        # 3. CLORO
        st.subheader("📊 Sezione Cloro")
        if cl_libero < 1.5:
            d_cl = 1.5 - cl_libero
            st.write("🛠 **Integrazione Ripristino (Target 1.5):**")
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Power Clor 56:</span> <span class="misura-grande">{(v_piscina*1.8*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Chemaclor L:</span> <span class="misura-grande">{(v_piscina*7*d_cl)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)
        
        if cl_combinato >= 0.4:
            st.write(f"💥 **Trattamento SHOCK (CC: {cl_combinato:.2f}):**")
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            if ppm_shock > 0:
                st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Power Clor 56:</span> <span class="misura-grande">{(v_piscina*1.8*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔥 Shock Chemaclor L:</span> <span class="misura-grande">{(v_piscina*7*ppm_shock)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)
        else:
            st.success("✅ Cloro Combinato ok.")
            
        # 4. ALTRI
        st.subheader("📊 Altri Interventi")
        cya_reale = cya_ril / 2
        if cya_reale < 30:
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">👉 Acido Cianurico:</span> <span class="misura-grande">{(v_piscina*(30-cya_reale))/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🌿 Algiprevent Mantenimento:</span> <span class="misura-grande">{(v_piscina*1)/100:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca (L)", min_value=0.0, value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", min_value=0.0, value=10.0)
    p_c = st.number_input("% Prodotto Commerciale", min_value=0.0, max_value=100.0, value=15.0)
    res = (l_i / v_v) * p_c if v_v > 0 else 0
    st.success(f"### ✅ Programmazione: {res:.2f} %")
