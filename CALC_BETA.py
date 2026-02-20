import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Light Beta", page_icon="💧", layout="centered")

# --- STILE CSS PER TEMA SCURO E LEGIBILITÀ ---
st.markdown("""
    <style>
    .misura-grande {
        font-size: 40px !important;
        font-weight: bold;
        color: #FF4B4B; /* Rosso acceso */
        margin-left: 10px;
    }
    .nome-prodotto {
        font-size: 18px;
        font-weight: 500;
        color: #F0F0F0; /* Testo chiaro per Dark Mode */
    }
    .unita-misura {
        font-size: 22px;
        color: #00D1FF; /* Azzurro brillante */
        font-weight: bold;
    }
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
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
    
    # INPUT DATI
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.0, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)
    
    # CALCOLO CLORO COMBINATO
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato (CC): **{cl_combinato:.2f} ppm**")

    st.markdown("---")
    # SALE: Input in mg/L (ppm) dalle strisce reattive
    sale_ril_mgl = st.number_input("Sale rilevato (mg/L - ppm)", min_value=0.0, value=0.0, step=100.0)

    if st.button("🚀 CALCOLA TUTTI I DOSAGGI", type="primary"):
        st.divider()
        
        # 1. SEZIONE SALE
        st.subheader("🧂 Sezione Sale")
        sale_gl = sale_ril_mgl / 1000
        m_std = max(0.0, 4.5 - sale_gl)
        m_ls = max(0.0, 1.5 - sale_gl)
        st.markdown(f'<p class="nome-prodotto">🧂 Clorinatore Standard (4.5): <span class="misura-grande">{(v_piscina * m_std):.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p class="nome-prodotto">🧂 Bassa Salinità (1.5): <span class="misura-grande">{(v_piscina * m_ls):.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
        st.divider()

        # 2. SEZIONE PH
        st.subheader("📊 Correzione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<p class="nome-prodotto">👉 Carisan pH meno G: <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">👉 pH meno L 15%: <span class="misura-grande">{(v_piscina*27*diff)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">👉 pH meno L 40%: <span class="misura-grande">{(v_piscina*9*diff)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<p class="nome-prodotto">👉 pH Plus: <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
        else:
            st.success("✅ pH ottimale.")
        st.divider()

        # 3. SEZIONE CLORO (RIPRISTINO + SHOCK)
        st.subheader("📊 Sezione Cloro")
        
        # Ripristino Cloro Libero (Target 1.5)
        if cl_libero < 1.5:
            d_cl = 1.5 - cl_libero
            st.write("🛠 **Dosaggio per Ripristino (Target 1.5 ppm):**")
            st.markdown(f'<p class="nome-prodotto">🔹 Chemacal 70: <span class="misura-grande">{(v_piscina*1.5*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">🔹 Power Clor 56: <span class="misura-grande">{(v_piscina*1.8*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">🔹 Chemaclor L: <span class="misura-grande">{(v_piscina*7*d_cl)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        
        # TRATTAMENTO SHOCK (Breakpoint: 10x Cloro Combinato)
        if cl_combinato > 0.1:
            st.write(f"💥 **Trattamento SHOCK (Breakpoint per CC {cl_combinato:.2f} ppm):**")
            # Formula breakpoint: (CC * 10) - Libero esistente
            ppm_necessari = max(0.0, (cl_combinato * 10) - cl_libero)
            if ppm_necessari > 0:
                st.markdown(f'<p class="nome-prodotto">🔥 Shock Chemacal 70: <span class="misura-grande">{(v_piscina*1.5*ppm_necessari)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
                st.markdown(f'<p class="nome-prodotto">🔥 Shock Power Clor 56: <span class="misura-grande">{(v_piscina*1.8*ppm_necessari)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
                st.markdown(f'<p class="nome-prodotto">🔥 Shock Chemaclor L: <span class="misura-grande">{(v_piscina*7*ppm_necessari)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        st.divider()
            
        # 4. SEZIONE STABILIZZANTE
        st.subheader("📊 Stabilizzante")
        cya_reale = cya_ril / 2
        st.info(f"Dato Cianurico Reale: {cya_reale:.1f} ppm")
        if cya_reale < 30:
            st.markdown(f'<p class="nome-prodotto">👉 Dose Acido Cianurico: <span class="misura-grande">{(v_piscina*(30-cya_reale))/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
        st.divider()
        
        # 5. SEZIONE ALGHICIDA
        st.subheader("🌿 Alghicida")
        st.markdown(f'<p class="nome-prodotto">✨ Algiprevent Inizio: <span class="misura-grande">{(v_piscina*2)/100:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p class="nome-prodotto">✨ Algiprevent Urto: <span class="misura-grande">{(v_piscina*5)/100:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p class="nome-prodotto">✨ Algiprevent Mantenimento: <span class="misura-grande">{(v_piscina*1)/100:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione Vasca")
    vol_vasca = st.number_input("Volume Vasca Soluzione (L)", min_value=0.0, value=100.0)
    litri_ins = st.number_input("Litri prodotto versati (L)", min_value=0.0, value=10.0)
    perc_prod = st.number_input("% Prodotto Commerciale", min_value=0.0, max_value=100.0, value=15.0)
    
    ris_p = (litri_ins / vol_vasca) * perc_prod if vol_vasca > 0 else 0
    st.success(f"### ✅ Valore in programmazione: {ris_p:.2f} %")
