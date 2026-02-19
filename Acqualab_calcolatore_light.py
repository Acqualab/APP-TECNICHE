import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Light", page_icon="💧", layout="centered")

# --- STILE CSS PER GRANDEZZA FONT E COLORI ---
st.markdown("""
    <style>
    .misura-grande {
        font-size: 36px !important;
        font-weight: bold;
        color: #E63946;
        margin-left: 15px;
    }
    .nome-prodotto {
        font-size: 19px;
        font-weight: 500;
        color: #1D3557;
    }
    .unita-misura {
        font-size: 22px;
        color: #457B9D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR E TITOLO ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.title("🧪 Suite Calcoli Light")

tab1, tab2 = st.tabs(["💧 Soluzione", "🏊 Pool Assistant"])

with tab1:
    st.header("1. Preparazione Soluzione")
    col_a, col_b = st.columns(2)
    with col_a:
        vol_vasca = st.number_input("Volume Vasca Soluzione (L)", min_value=0.0, value=100.0)
        litri_inseriti = st.number_input("Litri prodotto versati (L)", min_value=0.0, value=10.0)
    with col_b:
        perc_prodotto = st.number_input("% Prodotto Commerciale", min_value=0.0, max_value=100.0, value=15.0)
    
    ris_perc = (litri_inseriti / vol_vasca) * perc_prodotto if vol_vasca > 0 else 0
    st.success(f"### ✅ Valore in programmazione: {ris_perc:.2f} %")

with tab2:
    st.header("2. 💧 Pool Assistant")
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_ril = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)

    st.markdown("---")
    st.subheader("🧂 Sezione Sale")
    # CORREZIONE: Inserimento in g/L (che equivale a kg/mc)
    sale_ril_gl = st.number_input("Sale rilevato (g/L)", min_value=0.0, value=0.0, step=0.1, help="Grammi per litro equivalgono a kg al metro cubo")

    if st.button("🚀 CALCOLA INTERVENTI", type="primary", use_container_width=True):
        st.divider()
        
        # LOGICA SALE (Target 4.5 g/L e 1.5 g/L)
        m_std = max(0.0, 4.5 - sale_ril_gl)
        m_ls = max(0.0, 1.5 - sale_ril_gl)
        
        col_s1, col_s2 = st.columns(2)
        col_s1.metric("Clorinatore Standard", f"{(v_piscina * m_std):.2f} kg")
        col_s2.metric("Bassa Salinità", f"{(v_piscina * m_ls):.2f} kg")

        # pH
        st.subheader("📊 Gestione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<p class="nome-prodotto">👉 Carisan pH meno G: <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">👉 Carisan pH meno L 15%: <span class="misura-grande">{(v_piscina*27*diff)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">👉 Carisan pH meno L 40%: <span class="misura-grande">{(v_piscina*9*diff)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<p class="nome-prodotto">👉 pH Plus: <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
        else:
            st.success("✅ pH ottimale (7.2).")

        # CLORO
        st.subheader("📊 Integrazione Cloro")
        if cl_ril < 1.5:
            d_cl = 1.5 - cl_ril
            st.markdown(f'<p class="nome-prodotto">👉 Chemacal 70: <span class="misura-grande">{(v_piscina*1.5*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">👉 Power Clor 56: <span class="misura-grande">{(v_piscina*1.8*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="nome-prodotto">👉 Chemaclor L: <span class="misura-grande">{(v_piscina*7*d_cl)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
        else:
            st.success("✅ Cloro a norma.")
            
        # STABILIZZANTE
        st.subheader("📊 Stabilizzante e Manutenzione")
        cya_reale = cya_ril / 2
        st.info(f"**Dato Cianurico Reale:** {cya_reale:.1f} ppm")
        if cya_reale < 30:
            st.markdown(f'<p class="nome-prodotto">👉 Dose Acido Cianurico: <span class="misura-grande">{(v_piscina*(30-cya_reale))/1000:.2f}</span> <span class="unita-misura">kg</span></p>', unsafe_allow_html=True)
        
        st.markdown(f'<p class="nome-prodotto">👉 Alghicida (Settimana): <span class="misura-grande">{(v_piscina*5)/1000:.2f}</span> <span class="unita-misura">L</span></p>', unsafe_allow_html=True)
