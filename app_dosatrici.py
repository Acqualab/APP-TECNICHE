import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Acqualab - Suite Calcoli", 
    page_icon="💧",
    layout="centered"
)

# --- LOGICA DI RESET DEFINITIVA ---
# Inizializziamo un contatore per le chiavi dei widget se non esiste
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def reset_all():
    # Incrementiamo il contatore: questo cambia le chiavi di tutti i widget
    # obbligando Streamlit a ricrearli da zero con i valori di default
    st.session_state.reset_counter += 1
    # Puliamo anche eventuali altri stati residui
    for key in list(st.session_state.keys()):
        if key != 'reset_counter':
            del st.session_state[key]

# Generiamo un prefisso dinamico per le chiavi basato sul contatore
suffix = f"_{st.session_state.reset_counter}"

# --- SIDEBAR: LOGO E INFO ---
try:
    st.sidebar.image("Color con payoff - senza sfondo.png", use_container_width=True)
except:
    st.sidebar.title("ACQUALAB S.R.L.")

st.sidebar.markdown("---")
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
        vol_vasca = st.number_input("Volume Vasca Soluzione (L)", min_value=0.0, value=100.0, key=f"v_vasca{suffix}")
        litri_inseriti = st.number_input("Litri di prodotto versati (L)", min_value=0.0, value=10.0, key=f"l_ins{suffix}")
    with col_b:
        perc_prodotto = st.number_input("% Prodotto Commerciale (es. 15%)", min_value=0.0, max_value=100.0, value=15.0, key=f"p_prod{suffix}")
    
    risultato_perc = (litri_inseriti / vol_vasca) * perc_prodotto if vol_vasca > 0 else 0
    st.success(f"**Valore da inserire in programmazione: {risultato_perc:.2f} %**")

# --- TAB 2: CALCOLO PORTATA POMPA ---
with tab2:
    st.header("2. Determinazione Portata Dosatore")
    col1, col2 = st.columns(2)
    with col1:
        portata_imp = st.number_input("Portata impianto (mc/h)", min_value=0.0, value=10.0, key=f"p_imp{suffix}")
        pressione = st.number_input("Pressione impianto (bar)", min_value=0.0, value=2.0, key=f"press{suffix}")
    with col2:
        dosaggio_des = st.number_input("Dosaggio desiderato (g/mc o ppm)", min_value=0.0, value=2.0, key=f"dos_des{suffix}")
        # Valore dinamico basato sul Tab 1
        conc_sol = st.number_input("% Conc. soluzione impostata", min_value=0.01, value=risultato_perc if risultato_perc > 0 else 10.0, key=f"c_sol{suffix}")

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
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=0.0, value=0.0, key=f"v_pisc{suffix}")
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.2, step=0.1, key=f"ph_r{suffix}")
    with c2:
        cl_ril = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=0.0, step=0.1, key=f"cl_r{suffix}")
        cya_ril = st.number_input("Acido Cianurico rilevato (ppm)", min_value=0.0, value=0.0, key=f"cya_r{suffix}")

    st.markdown("---")
    st.subheader("🧂 Sezione Sale (Clorinatori)")
    sale_ril_g = st.number_input("Sale rilevato (g/mc)", min_value=0.0, value=0.0, step=100.0, key=f"s_ril{suffix}")

    # BOTTONI AZIONE
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        calcola = st.button("CALCOLA INTERVENTI", type="primary", use_container_width=True)
    with col_btn2:
        # Questo pulsante ora garantisce il reset di OGNI campo
        st.button("RESET", on_click=reset_all, use_container_width=True)

    if calcola:
        if v_piscina <= 0:
            st.error("Inserisci il volume della piscina per procedere.")
        else:
            st.divider()
            
            # SALE
            sale_ril_kg = sale_ril_g / 1000
            st.subheader("Integrazione Sale")
            m_std = max(0.0, 4.5 - sale_ril_kg)
            m_ls = max(0.0, 1.5 - sale_ril_kg)
            
            sc1, sc2 = st.columns(2)
            sc1.metric("Clorinatore Standard", f"{v_piscina * m_std:.2f} kg")
            sc2.metric("Bassa Salinità", f"{v_piscina * m_ls:.2f} kg")

            st.divider()

            # PARAMETRI CHIMICI
            cya_reale = cya_ril / 2
            st.info(f"**Dato Cianurico Reale:** {cya_reale:.1f} ppm")
            
            # pH
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

            # Cloro
            st.subheader("Integrazione Cloro")
            if cl_ril < 1.5:
                d_cl = 1.5 - cl_ril
                st.error(f"**Cloro BASSO.** Inserire:\n"
                         f"- Chemacal 70: **{(v_piscina*1.5*d_cl)/1000:.2f} kg**\n"
                         f"- Power Clor 56: **{(v_piscina*1.8*d_cl)/1000:.2f} kg**\n"
                         f"- Chemaclor L: **{(v_piscina*7*d_cl)/1000:.2f} L**")
            else:
                st.success("Cloro a norma.")
                
            # Cianurico
            if cya_reale < 30:
                st.subheader("Stabilizzante")
                st.warning(f"Dose Acido Cianurico: **{(v_piscina*(30-cya_reale))/1000:.2f} kg**")
            
            st.divider()
            st.write(f"**Alghicida (Mantenimento):** {(v_piscina*5)/1000:.2f} L/settimana")
