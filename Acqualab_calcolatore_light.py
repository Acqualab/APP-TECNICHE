import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Acqualab Light - Suite Calcoli", 
    page_icon="💧",
    layout="centered"
)

# --- SIDEBAR: LOGO E INFO ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.sidebar.markdown("---")
st.sidebar.info("Versione LIGHT - Strumenti rapidi per i tecnici ACQUALAB S.R.L.")

# --- TITOLO PRINCIPALE ---
st.title("🧪 Suite Calcoli Light")

# Navigazione tra i Tab (Solo 2 Tab)
tab1, tab2 = st.tabs(["💧 Soluzione", "🏊 Pool Assistant"])

# --- TAB 1: PREPARAZIONE SOLUZIONE ---
with tab1:
    st.header("1. Preparazione Soluzione")
    col_a, col_b = st.columns(2)
    with col_a:
        vol_vasca = st.number_input("Volume Vasca Soluzione (L)", min_value=0.0, value=100.0)
        litri_inseriti = st.number_input("Litri di prodotto versati (L)", min_value=0.0, value=10.0)
    with col_b:
        perc_prodotto = st.number_input("% Prodotto Commerciale (es. 15%)", min_value=0.0, max_value=100.0, value=15.0)
    
    risultato_perc = (litri_inseriti / vol_vasca) * perc_prodotto if vol_vasca > 0 else 0
    st.success(f"**Valore da inserire in programmazione: {risultato_perc:.2f} %**")

# --- TAB 2: POOL ASSISTANT (Inclusa Sezione Sale) ---
with tab2:
    st.header("2. 💧 Pool Assistant")
    
    # Dati dalla sorgente Pool Assistant.html
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_ril = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico rilevato (ppm)", min_value=0.0, value=0.0)

    st.markdown("---")
    st.subheader("🧂 Sezione Sale (Clorinatori)")
    sale_ril_g = st.number_input("Sale rilevato (g/mc)", min_value=0.0, value=0.0, step=100.0)

    if st.button("CALCOLA INTERVENTI", type="primary", use_container_width=True):
        st.divider()
        
        # LOGICA SALE
        sale_ril_kg = sale_ril_g / 1000
        
        st.subheader("Integrazione Sale")
        # Target Standard: 4.5 kg/mc
        mancante_std = max(0.0, 4.5 - sale_ril_kg)
        tot_sale_std = v_piscina * mancante_std
        
        # Target Bassa Salinità: 1.5 kg/mc
        mancante_ls = max(0.0, 1.5 - sale_ril_kg)
        tot_sale_ls = v_piscina * mancante_ls
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Clorinatore Standard", f"{tot_sale_std:.2f} kg")
            st.caption("Target: 4,5 kg/mc")
        with col_s2:
            st.metric("Bassa Salinità", f"{tot_sale_ls:.2f} kg")
            st.caption("Target: 1,5 kg/mc")

        st.divider()

        # LOGICA PARAMETRI CHIMICI
        cya_reale = cya_ril / 2
        st.info(f"**Dato Cianurico Reale:** {cya_reale:.1f} ppm")
        
        # pH (Target 7.2)
        st.subheader("Gestione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.warning(f"**pH ALTO.** Inserire:\n"
                       f"- Carisan pH meno G: **{(v_piscina*10*diff)/1000:.2f} kg**\n"
                       f"- Carisan pH meno L 15%: **{(v_piscina*27*diff)/1000:.2f} L**\n"
                       f"- Carisan pH meno L 40%: **{(v_piscina*9*diff)/1000:.2f} L**")
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.info(f"**pH BASSO.** Inserire: **{(v_piscina*10*diff)/1000:.2f} kg** di pH Plus")
        else:
            st.success("pH ottimale (7.2).")

        # Cloro (Target 1.5)
        st.subheader("Integrazione Cloro")
        if cl_ril < 1.5:
            d_cl = 1.5 - cl_ril
            st.error(f"**Cloro BASSO.** Inserire:\n"
                     f"- Chemacal 70: **{(v_piscina*1.5*d_cl)/1000:.2f} kg**\n"
                     f"- Power Clor 56: **{(v_piscina*1.8*d_cl)/1000:.2f} kg**\n"
                     f"- Chemaclor L: **{(v_piscina*7*d_cl)/1000:.2f} L**")
        else:
            st.success("Cloro a norma.")
            
        # Acido Cianurico
        if cya_reale < 30:
            st.subheader("Stabilizzante")
            st.warning(f"Dose Acido Cianurico: **{(v_piscina*(30-cya_reale))/1000:.2f} kg**")
        
        st.divider()
        st.write(f"**Alghicida (Mantenimento):** {(v_piscina*5)/1000:.2f} L/settimana")
