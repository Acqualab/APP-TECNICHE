import streamlit as st
import math

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Acqualab Suite PRO", layout="centered")

# --- STILE ---
st.markdown("""
    <style>
    .valore-evidenziato { font-size: 28px; font-weight: bold; color: #00AEEF; }
    .result-box { padding: 20px; border-radius: 10px; border: 1px solid #ddd; background-color: #fcfcfc; margin-bottom: 20px; }
    .stat-label { font-size: 12px; color: #777; font-weight: bold; text-transform: uppercase; }
    .stat-value { font-size: 20px; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Suite Tecnica PRO")

tab1, tab2, tab3, tab4 = st.tabs(["🏊 Piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- TAB 1: PISCINA ---
with tab1:
    st.header("Trattamento Acqua")
    c1, c2 = st.columns(2)
    vol = c1.number_input("Volume (m³)", value=100.0)
    ph = c1.number_input("pH", value=7.8)
    cl_l = c2.number_input("Cloro Libero", value=1.0)
    cl_t = c2.number_input("Cloro Totale", value=1.6)
    c_comb = max(0.0, cl_t - cl_l)
    if ph > 7.4:
        st.error(f"Dosare {(vol * 10 * ((ph - 7.2) / 0.1)) / 1000:.2f} kg di pH Meno")
    if c_comb >= 0.4:
        st.error(f"Dosare {(vol * 1.5 * ((c_comb * 10) - cl_l)) / 1000:.2f} kg di Shock")

# --- TAB 2: SOLUZIONE ---
with tab2:
    st.header("Calcolo Pompa")
    v_v = st.number_input("Vasca (L)", value=100.0)
    l_p = st.number_input("Prodotto (L)", value=10.0)
    if v_v > 0: st.success(f"Risultato: {(l_p / v_v) * 15:.2f} %")

# --- TAB 3: GESTIONE (SALE PER RIG) ---
with tab3:
    st.header("Analisi Macchina")
    g1, g2 = st.columns(2)
    res = g1.number_input("Litri Resina", value=30)
    d_in = g1.number_input("Durezza In", value=35)
    d_out = g2.number_input("Durezza Out", value=15)
    cons = g2.number_input("Consumo m³/gg", value=0.6)
    
    dn = max(0.1, d_in - d_out)
    aut = (res * 5) / dn
    # RICHIESTA: SALE PER RIGENERAZIONE
    s_rig = (res * 140) / 1000 
    st.markdown(f'<div class="result-box">Autonomia: <span class="valore-evidenziato">{aut:.2f} m³</span></div>', unsafe_allow_html=True)
    c_a, c_b, c_c = st.columns(3)
    c_a.write(f"<span class='stat-label'>Sale/Rig</span><br><span class='stat-value'>{s_rig:.2f} kg</span>", unsafe_allow_html=True)
    c_b.write(f"<span class='stat-label'>Salamoia</span><br><span class='stat-value'>{s_rig*3:.1f} L</span>", unsafe_allow_html=True)
    c_c.write(f"<span class='stat-label'>Scarico</span><br><span class='stat-value'>{res*7} L</span>", unsafe_allow_html=True)

# --- TAB 4: PROGETTO (DUREZZA MIX E INTERVALLO GG) ---
with tab4:
    st.header("Nuovo Progetto")
    p1, p2 = st.columns(2)
    d_ing = p1.number_input("Durezza Acquedotto", value=35, key="di")
    d_mix = p1.number_input("Durezza Mix Desiderata", value=15, key="dm") # RICHIESTA: MIX
    p_n = p2.number_input("Persone/App", value=4)
    
    dn_p = max(0.1, d_ing - d_mix)
    c_gg = p_n * 0.2
    t_id = (c_gg * 4 * dn_p) / 5
    t_scelta = min([t for t in [8,12,15,20,25,30,40,50,75,100] if t >= t_id] or [100])
    
    aut_p = (t_scelta * 5) / dn_p
    # RICHIESTA: INTERVALLO RIG
    int_gg = aut_p / c_gg if c_gg > 0 else 0
    
    st.info(f"Taglia: {t_scelta}L | Autonomia: {aut_p:.2f} m³ | Rigenerazione: ogni {int_gg:.1f} giorni")
    
    # CONFRONTO
    n_r = 365 / int_gg if int_gg > 0 else 0
    s_std = (t_scelta * 0.14) * n_r
    st.table({"Dato Annuale": ["Sale (kg)", "Sacchi (25kg)"], 
              "Standard": [f"{s_std:.0f}", f"{math.ceil(s_std/25)}"], 
              "Clack": [f"{s_std*0.8:.0f}", f"{math.ceil(s_std*0.8/25)}"]})
