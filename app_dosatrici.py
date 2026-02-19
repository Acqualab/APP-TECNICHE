import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Acqualab - Suite Calcoli", 
    page_icon="💧",
    layout="centered"
)

# --- FUNZIONE RESET ---
def reset_all():
    for key in st.session_state.keys():
        del st.session_state[key]

# --- SIDEBAR: LOGO E INFO ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.sidebar.markdown("---")
st.sidebar.button("🔄 RESET GENERALE", on_click=reset_all, use_container_width=True)
st.sidebar.info("Strumenti di calcolo ad uso interno per i tecnici di ACQUALAB S.R.L.")

# --- TITOLO PRINCIPALE ---
st.title("🧪 Suite Calcoli Dosaggio")

# Navigazione tra i Tab
tab1, tab2, tab3 = st.tabs(["💧 Soluzione", "⚙️ Pompa Dosatrice", "🏊 Pool Assistant"])

# --- TAB 1: PREPARAZIONE SOLUZIONE ---
with tab1:
    st.header("1. Preparazione Soluzione")
    col_a, col_b = st.columns(2)
    with col_a:
        vol_vasca = st.number_input("Volume Vasca Soluzione (L)", min_value=0.0, value=100.0, key="v_vasca")
        litri_inseriti = st.number_input("Litri di prodotto versati (L)", min_value=0.0, value=10.0, key="l_ins")
    with col_b:
        perc_prodotto = st.number_input("% Prodotto Commerciale (es. 15%)", min_value=0.0, max_value=100.0, value=15.0, key="p_prod")
    
    risultato_perc = (litri_inseriti / vol_vasca) * perc_prodotto if vol_vasca > 0 else 0
    st.success(f"**Valore da inserire in programmazione: {risultato_perc:.2f} %**")

# --- TAB 2: CALCOLO PORTATA POMPA ---
with tab2:
    st.header("2. Determinazione Portata Dosatore")
    col1, col2 = st.columns(2)
    with col1:
        portata_imp = st.number_input("Portata impianto (mc/h)", min_value=0.0, value=10.0, key="p_imp")
        pressione = st.number_input("Pressione impianto (bar)", min_value=0.0, value=2.0, key="press")
    with col2:
        dosaggio_des = st.number_input("Dosaggio desiderato (g/mc o ppm)", min_value=0.0, value=2.0, key="dos_des")
        conc_sol = st.number_input("% Conc. soluzione impostata", min_value=0.01, value=risultato_perc if risultato_perc > 0 else 10.0, key="c_sol")

    principio_attivo = portata_imp * dosaggio_des
    portata_pompa = principio_attivo / (conc_sol * 10) if conc_sol > 0 else 0

    st.divider()
    res_c1, res_c2 = st.columns(2)
    res_c1.metric("Principio Attivo", f"{principio_attivo:.2f} g/h")
    res_c2.metric("Portata Pompa", f"{portata_pompa:.2f} l/h")

# --- TAB 3: POOL ASSISTANT ---
with tab3:
    st.header("3. 💧 Pool Assistant")
    
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0, key="v_pisc")
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1, key="ph_r")
    with c2:
        cl_ril = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1, key="cl_r")
        cya_ril = st.number_input("Acido Cianurico rilevato (ppm)", min_value=0.0, value=0.0, key="cya_r")

    st.markdown("---")
    st.subheader("🧂 Sezione Sale (Clorinatori)")
    sale_ril = st.number_input("Sale rilevato (kg/mc)", min_value=0.0, value=0.0, step=0.1, key="s_ril", help="Inserisci il valore attuale in kg/mc")

    if st.button("CALCOLA INTERVENTI", type="primary", use_container_width=True):
        st.divider()
        
        # --- LOGICA SALE ---
        st.subheader("Integrazione Sale")
        mancante_std = max(0.0, 4.5 - sale_ril)
        tot_sale_std = v_piscina * mancante_std
        
        mancante_ls = max(0.0, 1.5 - sale_ril)
        tot_sale_ls = v_piscina * mancante_ls
        
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.metric("Clorinatore Standard", f"{tot_sale_std:.2f} kg")
            st.caption("Target: 4.5 kg/mc")
        with s_col2:
            st.metric("Bassa Salinità", f"{tot_sale_ls:.2f} kg")
            st.caption("Target: 1.5 kg/mc")

        st.divider()

        # --- LOGICA PH (Target 7.2) ---
        cya_reale = cya_ril / 2
        st.info(f"**Dato Cianurico Reale:** {cya_reale:.1f} ppm")
        
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
            st.success("pH ottimale.")

        # --- LOGICA CLORO (Target 1.5) ---
        st.subheader("Integrazione Cloro")
        if cl_ril < 1.5:
            d_cl = 1.5 - cl_ril
            st.error(f"**Cloro BASSO.** Inserire:\n"
                     f"- Chemacal 70: **{(v_piscina*1.5*d_cl)/1000:.2f} kg**\n"
                     f"- Power Clor 56: **{(v_piscina*1.8*d_cl)/1000:.2f} kg**\n"
                     f"- Chemaclor L: **{(v_piscina*7*d_cl)/1000:.2f} L**")
        else:
            st.success("Cloro a norma.")
            
        # --- ACIDO CIANURICO E ALGHICIDA ---
        st.subheader("Stabilizzante e Altri")
        if cya_reale < 30:
            st.warning(f"Dose Acido Cianurico: **{(v_piscina*(30-cya_reale))/1000:.2f} kg**")
        
        st.write(f"**Alghicida (Mantenimento):** {(v_piscina*5)/1000:.2f} L/settimana")
