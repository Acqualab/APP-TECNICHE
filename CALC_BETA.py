import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Light Beta", page_icon="💧", layout="centered")

# --- STILE CSS OTTIMIZZATO PER CHIARO E SCURO ---
st.markdown("""
    <style>
    /* Numero gigante in rosso (visibile ovunque) */
    .misura-grande {
        font-size: 38px !important;
        font-weight: bold;
        color: #E63946; 
        margin-left: 10px;
    }
    /* Nome prodotto con colore adattivo o grigio medio scuro */
    .nome-prodotto {
        font-size: 18px;
        font-weight: 600;
        color: #495057; /* Grigio antracite leggibile su bianco */
    }
    /* Se siamo in Dark Mode, forziamo il testo più chiaro */
    @media (prefers-color-scheme: dark) {
        .nome-prodotto {
            color: #E9ECEF; 
        }
    }
    /* Unità di misura in azzurro corazzato */
    .unita-misura {
        font-size: 20px;
        color: #457B9D;
        font-weight: bold;
    }
    /* Box per i risultati per dare profondità */
    .result-box {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(128, 128, 128, 0.1);
        margin-bottom: 10px;
        border-left: 5px solid #E63946;
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

    if st.button("🚀 CALCOLA TUTTI I DOSAGGI", type="primary"):
        st.divider()
        
        # 1. SEZIONE SALE
        st.subheader("🧂 Sezione Sale")
        sale_gl = sale_ril_mgl / 1000
        m_std = max(0.0, 4.5 - sale_gl)
        m_ls = max(0.0, 1.5 - sale_gl)
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🧂 Clorinatore Standard (4.5):</span> <span class="misura-grande">{(v_piscina * m_std):.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">🧂 Bassa Salinità (1.5):</span> <span class="misura-grande">{(v_piscina * m_ls):.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        
        # 2. SEZIONE PH
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

        # 3. SEZIONE CLORO
        st.subheader("📊 Sezione Cloro")
        if cl_libero < 1.5:
            d_cl = 1.5 - cl_libero
            st.write("🛠 **Dosaggio per Ripristino (Target 1.5 ppm):**")
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Power Clor 56:</span> <span class="misura-grande">{(v_piscina*1.8*d_cl)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">🔹 Chemaclor L:
