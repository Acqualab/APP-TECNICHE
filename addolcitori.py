import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Dimensionamento Addolcitori", page_icon="🚰", layout="centered")

# --- STILE CSS PER RISULTATI CHIARI ---
st.markdown("""
    <style>
    .valore-evidenziato {
        font-size: 30px !important;
        font-weight: bold;
        color: #00AEEF;
    }
    .titolo-sezione {
        font-size: 20px;
        font-weight: bold;
        color: var(--text-color);
        border-bottom: 2px solid #00AEEF;
        margin-bottom: 15px;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚰 Modulo Addolcitori")
st.write("Strumento professionale per il calcolo di autonomia, sale e salamoia.")

# --- INPUT DATI ---
st.markdown('<p class="titolo-sezione">1. Parametri Impianto</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    v_resina = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
    durezza_in = st.number_input("Durezza Acqua Grezza (°f)", min_value=1, value=35)
with c2:
    durezza_out = st.number_input("Durezza Miscelata Uscita (°f)", min_value=0, value=15)
    cons_m3_giorno = st.number_input("Consumo Acqua Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

# --- LOGICA DI CALCOLO ---
durezza_da_abbattere = durezza_in - durezza_out

if durezza_da_abbattere <= 0:
    st.error("Errore: La durezza in uscita deve essere inferiore a quella in entrata.")
else:
    # 1. Capacità Ciclica (standard 5.0 m3*°f per litro resina)
    cap_ciclica = v_resina * 5 
    
    # 2. Autonomia Ciclica (m3 di acqua dolce prodotti)
    m3_ciclo = cap_ciclica / durezza_da_abbattere
    
    # 3. Giorni tra rigenerazioni
    giorni_autonomia = m3_ciclo / cons_m3_giorno
    
    # 4. Consumo sale per singola rigenerazione (140g/L resina)
    sale_per_rig_kg = (v_resina * 140) / 1000
    
    # 5. Volume Salamoia Satura (1kg sale produce circa 3L di salamoia satura)
    salamoia_litri = sale_per_rig_kg * 3
    
    # 6. Consumo acqua stimato per rigenerazione (circa 7 volte il vol. resina)
    acqua_scarico_rig = (v_resina * 7) / 1000

    # --- VISUALIZZAZIONE RISULTATI ---
    st.markdown('<p class="titolo-sezione">2. Risultati Calcolo</p>', unsafe_allow_html=True)
    
    res1, res2 = st.columns(2)
    with res1:
        st.write("🌊 **Produzione Acqua Dolce**")
        st.markdown(f'<span class="valore-evidenziato">{m3_ciclo:.2f} m³</span>', unsafe_allow_html=True)
        st.write(f"Ogni {giorni_autonomia:.1f} giorni l'impianto rigenera.")

    with res2:
        st.write("🧂 **Consumo Sale**")
        st.markdown(f'<span class="valore-evidenziato">{sale_per_rig_kg:.2f} kg</span>', unsafe_allow_html=True)
        st.write(f"Sale per singola rigenerazione.")

    st.markdown("---")
    
    st.write("📊 **Dettagli Tecnici per Settaggio Valvola:**")
    det1, det2, det3 = st.columns(3)
    det1.metric("Capacità Ciclica", f"{cap_ciclica} m³·°f")
    det2.metric("Volume Salamoia", f"{salamoia_litri:.1f} Litri")
    det3.metric("Acqua Scarico", f"{acqua_scarico_rig*1000:.0f} Litri")

    # --- ALERT DIMENSIONAMENTO ---
    if giorni_autonomia < 1:
        st.warning("⚠️ **ATTENZIONE:** L'addolcitore è troppo piccolo per questo consumo. Rigenerazione troppo frequente.")
    elif giorni_autonomia > 7:
        st.info("ℹ️ **NOTA:** L'autonomia supera i 7 giorni. Assicurarsi che la valvola abbia la rigenerazione forzata a tempo per igiene resine.")
    else:
        st.success("✅ **DIMENSIONAMENTO CORRETTO:** Equilibrio ottimale tra resine e consumo.")

    # --- STIMA ANNUALE ---
    st.markdown('<p class="titolo-sezione">3. Previsione Annuale</p>', unsafe_allow_html=True)
    rigenerazioni_anno = 365 / giorni_autonomia
    sale_anno_kg = rigenerazioni_anno * sale_per_rig_kg
    sacchi_anno = sale_anno_kg / 25
    
    col_a, col_b = st.columns(2)
    col_a.write(f"📅 Rigenerazioni stimatate: **{int(rigenerazioni_anno)}/anno**")
    col_b.write(f"📦 Sacchi sale (25kg): **{int(sacchi_anno) + 1} sacchi/anno**")
