import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="Pompe Dosatrici Pro", layout="centered")

st.title("🧪 Pompe Dosatrici - Suite Calcoli")

# Creazione delle Schede (Tab)
tab1, tab2 = st.tabs(["📊 Calcolo Portata", "⚗️ Conc. Soluzione"])

# --- TAB 1: CALCOLO PORTATA (Quello di prima) ---
with tab1:
    st.header("Determinazione Portata Dosatore")
    
    col_a, col_b = st.columns(2)
    with col_a:
        portata_imp = st.number_input("Portata impianto (mc/h)", min_value=0.1, value=10.0, key="p_imp")
        pressione = st.number_input("Pressione impianto (bar)", min_value=0.0, value=2.0, key="pres")
    
    with col_b:
        dosaggio = st.number_input("Dosaggio desiderato (g/mc o ppm)", min_value=0.0, value=2.0, key="dos")
        # Nota: usiamo il valore calcolato nella Tab 2 se l'utente vuole automatizzare, 
        # ma per ora lasciamolo manuale come l'Excel originale.
        conc_manuale = st.number_input("% Conc. soluzione prodotto", min_value=0.1, max_value=100.0, value=10.0, key="conc_m")

    # Calcoli
    principio_attivo_gh = portata_imp * dosaggio
    portata_dosatore_lh = (principio_attivo_gh / conc_manuale) * 100 / 1000

    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("Principio Attivo", f"{principio_attivo_gh:.2f} g/h")
    res2.metric("Portata Pompa", f"{portata_dosatore_lh:.2f} l/h")

# --- TAB 2: DETERMINAZIONE CONCENTRAZIONE (Nuova Tabella) ---
with tab2:
    st.header("Determinazione della Conc. Soluzione")
    st.info("Usa questa sezione per calcolare la percentuale da impostare sulla pompa in base alla miscela nel serbatoio.")

    v_soluzione = st.number_input("Volume soluzione (litri)", min_value=0.1, value=100.0)
    p_attivo_reagente = st.number_input("% del principio attivo (nel reagente puro)", min_value=0.1, max_value=100.0, value=15.0)
    lt_reagente = st.number_input("Litri di reagente inseriti", min_value=0.0, value=5.0)

    # Formula richiesta: (lt reagente * % principio attivo) / volume soluzione
    percentuale_prog = (lt_reagente * p_attivo_reagente) / v_soluzione

    st.divider()
    st.subheader("Risultato")
    st.success(f"**% da inserire in programmazione pompa: {percentuale_prog:.2f}%**")
    
    st.caption("Questo valore rappresenta la concentrazione reale della soluzione pronta al dosaggio.")