import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Acqualab - Suite Calcoli", 
    page_icon="💧",
    layout="centered"
)

# --- SIDEBAR: LOGO E INFO ---
try:
    # Utilizzo del nome file esatto fornito dall'utente
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.sidebar.markdown("---")
st.sidebar.info("Strumenti di calcolo ad uso interno per i tecnici di ACQUALAB S.R.L.")
st.sidebar.write("V1.0 | 2024")

# --- TITOLO PRINCIPALE ---
st.title("🧪 Suite Calcoli Dosaggio")

# Creazione dei Tab per navigare tra le diverse funzioni
tab1, tab2, tab3 = st.tabs(["💧 Soluzione", "⚙️ Pompa Dosatrice", "🏊 Pool Assistant"])

# --- TAB 1: PREPARAZIONE SOLUZIONE ---
with tab1:
    st.header("1. Preparazione Soluzione")
    st.write("Calcola la concentrazione reale nel bidone dopo la diluizione.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        vol_vasca = st.number_input("Volume Vasca Soluzione (L)", min_value=0.0, value=100.0)
        litri_inseriti = st.number_input("Litri di prodotto versati (L)", min_value=0.0, value=10.0)
    with col_b:
        perc_prodotto = st.number_input("% Prodotto Commerciale (es. 15%)", min_value=0.0, max_value=100.0, value=15.0)
    
    # Calcolo concentrazione
    risultato_perc = (litri_inseriti / vol_vasca) * perc_prodotto if vol_vasca > 0 else 0
    st.success(f"Concentrazione Reale nella vasca: **{risultato_perc:.2f} %**")

# --- TAB 2: CALCOLO PORTATA POMPA ---
with tab2:
    st.header("2. Determinazione Portata Dosatore")
    st.write("Calcola la portata necessaria della pompa dosatrice.")
    
    col1, col2 = st.columns(2)
    with col1:
        portata_imp = st.number_input("Portata impianto (mc/h)", min_value=0.0, value=10.0)
        pressione = st.number_input("Pressione impianto (bar)", min_value=0.0, value=2.0)
    with col2:
        dosaggio_des = st.number_input("Dosaggio desiderato (g/mc o ppm)", min_value=0.0, value=2.0)
        # Il valore di default è legato al Tab 1 per comodità
        conc_sol = st.number_input("% Conc. soluzione nel bidone", min_value=0.01, value=risultato_perc if risultato_perc > 0 else 10.0)

    # Formule di calcolo
    principio_attivo = portata_imp * dosaggio_des
    portata_pompa = principio_attivo / (conc_sol * 10) if conc_sol > 0 else 0

    st.divider()
    res_c1, res_c2 = st.columns(2)
    res_c1.metric("Principio Attivo", f"{principio_attivo:.2f} g/h")
    res_c2.metric("Portata Pompa", f"{portata_pompa:.2f} l/h")

# --- TAB 3: POOL ASSISTANT (Convertito da Pool Assistant.html) ---
with tab3:
    st.header("3. 💧 Pool Assistant")
    st.write("Calcolo dosaggi per manutenzione piscina.")
    
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=100.0, key="vol_p")
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
    with c2:
        cl_ril = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=0.0)

    if st.button("CALCOLA INTERVENTI", type="primary", use_container_width=True):
        st.divider()
        cya_reale = cya_ril / 2  # Logica derivata dal tuo file HTML originale
        st.info(f"**Dato Cianurico Reale:** {cya_reale:.1f} ppm")
        
        # LOGICA PH (Target 7.2)
        st.subheader("Gestione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.warning(f"**pH ALTO.** Prodotti consigliati:\n\n"
                       f"* Carisan pH meno G: **{(v_piscina*10*diff)/1000:.2f} kg**\n"
                       f"* Carisan pH meno L 15%: **{(v_piscina*27*diff)/1000:.2f} L**\n"
                       f"* Carisan pH meno L 40%: **{(v_piscina*9*diff)/1000:.2f} L**")
        elif ph_ril < 7.2 and ph_ril > 0:
            diff = (7.2 - ph_ril) / 0.1
            st.info(f"**pH BASSO.** Inserire:\n\n* Carisan pH Plus: **{(v_piscina*10*diff)/1000:.2f} kg**")
        else:
            st.success("Il pH è ottimale (7.2).")

        # LOGICA CLORO (Target 1.5)
        st.subheader("Integrazione Cloro")
        if cl_ril < 1.5:
            diff_cl = 1.5 - cl_ril
            st.error(f"**Cloro BASSO.** Prodotti consigliati:\n\n"
                     f"* Chemacal 70: **{(v_piscina*1.5*diff_cl)/1000:.2f} kg**\n"
                     f"* Power Clor 56: **{(v_piscina*1.8*diff_cl)/1000:.2f} kg**\n"
                     f"* Chemaclor L: **{(v_piscina*7*diff_cl)/1000:.2f} L**")
        else:
            st.success("Il livello di Cloro è a norma.")
            
        # LOGICA ALGHICIDA E CIANURICO
        st.
