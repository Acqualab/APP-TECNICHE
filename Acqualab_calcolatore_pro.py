import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab PRO Suite", page_icon="💧", layout="centered")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .valore-evidenziato { font-size: 30px !important; font-weight: bold; color: #00AEEF; }
    .result-box { padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; background-color: #f9f9f9; margin-bottom: 15px; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: #1E3A8A; border-bottom: 2px solid #00AEEF; padding-bottom: 5px; margin-bottom: 15px; }
    .stat-label { font-size: 12px; color: #666; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 20px; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Parametri Economici")
    prezzo_sacco = st.number_input("Prezzo Sale (€/25kg)", min_value=1.0, value=12.0)
    st.divider()
    st.info("Configurazione: **Clack Impression PRO**")

st.title("🧪 Suite Tecnica Acqualab")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Piscina", "💧 Soluzione", "🚰 Gestione Macchina", "📐 Progetto Nuovo"])

# --- TAB 1: PISCINA ---
with tab1:
    st.header("Analisi Acqua Piscina")
    p1, p2 = st.columns(2)
    vol_vasca = p1.number_input("Volume Piscina (m³)", value=100.0)
    ph_att = p1.number_input("pH Rilevato", value=7.8, step=0.1)
    cl_lib = p2.number_input("Cloro Libero (ppm)", value=1.0)
    cl_tot = p2.number_input("Cloro Totale (ppm)", value=1.6)
    
    c_comb = max(0.0, cl_tot - cl_lib)
    st.info(f"Cloro Combinato: **{c_comb:.2f} ppm**")
    
    if ph_att > 7.4:
        dose_ph = (vol_vasca * 10 * ((ph_att - 7.2) / 0.1)) / 1000
        st.error(f"👉 Dosare **{dose_ph:.2f} kg** di pH Meno G")
    
    if c_comb >= 0.4:
        fabb_shock = max(0.0, (c_comb * 10) - cl_lib)
        dose_shock = (vol_vasca * 1.5 * fabb_shock) / 1000
        st.error(f"🔥 Dosare **{dose_shock:.2f} kg** di Chemacal 70 (Shock)")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Dosaggio Pompe")
    v_s = st.number_input("Litri acqua in vasca", value=100.0)
    l_p = st.number_input("Litri prodotto puro inseriti", value=10.0)
    perc = st.number_input("% Prodotto commerciale", value=15.0)
    if v_s > 0:
        ris_sol = (l_p / v_s) * perc
        st.success(f"Impostazione Pompa: **{ris_sol:.2f} %**")

# --- TAB 3: GESTIONE MACCHINA ESISTENTE ---
with tab3:
    st.header("Analisi Macchina in Funzione")
    g1, g2 = st.columns(2)
    res_litri = g1.number_input("Litri Resina Macchina", value=30)
    dur_in_g = g1.number_input("Durezza Entrata (°f)", value=40)
    dur_out_g = g2.number_input("Durezza Uscita (°f)", value=15)
    cons_gg_g = g2.number_input("Consumo Acqua (m³/giorno)", value=0.6)

    d_netta = max(0.1, dur_in_g - dur_out_g)
    cap_ciclica = res_litri * 5
    autonomia_m3 = cap_ciclica / d_netta
    
    # Calcolo SALE per rigenerazione (Tab 3 specifica richiesta)
    sale_per_rig = (res_litri * 140) / 1000 # 140g per litro
    giorni_autonomia = autonomia_m3 / cons_gg_g if cons_gg_g > 0 else 0

    st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{autonomia_m3:.2f} m³</span><br>Rigenera ogni: <b>{giorni_autonomia:.1f} giorni</b></div>', unsafe_allow_html=True)
    
    c_a, c_b, c_c = st.columns(3)
    c_a.write(f"<span class='stat-label'>Sale / Rig.</span><br><span class='stat-value'>{sale_per_rig:.2f} kg</span>", unsafe_allow_html=True)
    c_b.write(f"<span class='stat-label'>Salamoia</span><br><span class='stat-value'>{(sale_per_rig*3):.1f} L</span>", unsafe_allow_html=True)
    c_c.write(f"<span class='stat-label'>Scarico</span><br><span class='stat-value'>{res_litri*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO NUOVO ---
with tab4:
    st.header("Progettazione e Mix")
    pr1, pr2 = st.columns(2)
    tipo_ut = pr1.selectbox("Utenza", ["Villetta", "Condominio"])
    d_ing_p = pr1.number_input("Durezza Acquedotto (°f)", value=35)
    d_mix_p = pr1.number_input("Durezza Mix Desiderata (°f)", value=15) # DUREZZA MIX RICHIESTA
    
    if tipo_ut == "Villetta":
        n_p = pr2.number_input("Persone", value=4)
        c_gg = n_p * 0.2
        picco = 1.2
    else:
        n_app = pr2.number_input("Appartamenti", value=10)
        c_gg = (n_app * 3) * 0.2
        picco = round(0.2 * math.sqrt(n_app * 3) + 0.8, 2)

    d_abbattere = max(0.1, d_ing_p - d_mix_p)
    taglia_ideale = (c_gg * 4 * d_abbattere) / 5 # Dimensionato su 4 giorni
    taglie_std = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    taglia_scelta = min([t for t in taglie_std if t >= taglia_ideale] or [300])

    # INTERVALLO DI RIGENERAZIONE (Tab 4 specifica richiesta)
    m3_nuovo = (taglia_scelta * 5) / d_abbattere
    intervallo_gg_nuovo = m3_nuovo / c_gg if c_gg > 0 else 0

    st.markdown(f"""
    <div class="result-box" style="border-left: 5px solid #00AEEF">
        🎯 <b>TAGLIA CONSIGLIATA: {taglia_scelta} LITRI</b><br>
        Portata Picco: {picco} m³/h | Autonomia: {m3_nuovo:.2f} m³<br>
        Intervallo rigenerazione: <b>Ogni {intervallo_gg_nuovo:.1f} giorni</b>
    </div>
    """, unsafe_allow_html=True)

    # --- CONFRONTO ANNUALE ---
    st.markdown('<p class="titolo-sezione">📊 Confronto Risparmio Annuale</p>', unsafe_allow_html=True)
    n_rig_anno = 365 / intervallo_gg_nuovo if intervallo_gg_nuovo > 0 else 0
    sale_anno_std = (taglia_scelta * 0.14) * n_rig_anno
    sale_anno_clack = sale_anno_std * 0.75 # Risparmio 25%
    
    sacchi_std = math.ceil(sale_anno_std / 25)
    sacchi_clack = math.ceil(sale_anno_clack / 25)

    st.table({
        "Dati Annuali": ["Sale (kg)", "Sacchi (25kg)", "Costo Sale (€)", "Scarico (m³)"],
        "Valvola Standard": [f"{sale_anno_std:.0f}", f"{sacchi_std}", f"{sacchi_std*prezzo_sacco:.0f}€", f"{(taglia_scelta*7*n_rig_anno)/1000:.1f}"],
        "Clack Impression": [f"{sale_anno_clack:.0f}", f"{sacchi_clack}", f"{sacchi_clack*prezzo_sacco:.0f}€", f"{(taglia_scelta*5*n_rig_anno)/1000:.1f}"]
    })
