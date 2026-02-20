import streamlit as st
import math

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Acqualab PRO", layout="centered")

# --- CSS DEFINITIVO (Fix per stabilità grafica) ---
st.markdown("""
    <style>
    .valore-box { padding: 20px; border-radius: 10px; background: #f8f9fa; border: 1px solid #dee2e6; text-align: center; margin-bottom: 10px; }
    .label-tecnica { font-size: 14px; color: #666; text-transform: uppercase; font-weight: bold; }
    .dato-tecnico { font-size: 24px; font-weight: bold; color: #007bff; }
    .box-dosaggio { padding: 15px; border-radius: 10px; background: white; border: 2px solid #eee; text-align: center; }
    .misura-kg { font-size: 30px; font-weight: bold; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Suite Calcoli PRO")

# Navigazione
tab1, tab2, tab3, tab4 = st.tabs(["🏊 Piscina", "💧 Soluzione", "🚰 Gestione", "📐 Progetto"])

# --- 1. PISCINA (Dosaggi e Analisi) ---
with tab1:
    st.header("Analisi e Interventi Piscina")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        v_piscina = st.number_input("Volume Piscina (m³)", value=100.0)
        ph_ril = st.number_input("pH Rilevato", value=7.8, step=0.1)
    with col_p2:
        cl_lib = st.number_input("Cloro Libero (ppm)", value=1.0)
        cl_tot = st.number_input("Cloro Totale (ppm)", value=1.5)
    
    cl_comb = max(0.0, cl_tot - cl_lib)
    st.info(f"💡 Cloro Combinato (CC): **{cl_comb:.2f} ppm**")
    
    st.subheader("Dosaggi Consigliati")
    res_p1, res_p2 = st.columns(2)
    
    if ph_ril > 7.4:
        kg_ph = (v_piscina * 10 * ((ph_ril - 7.2) / 0.1)) / 1000
        res_p1.markdown(f'<div class="box-dosaggio">👉 pH meno G<br><span class="misura-kg">{kg_ph:.2f} kg</span></div>', unsafe_allow_html=True)
    
    if cl_comb >= 0.4:
        kg_shock = (v_piscina * 1.5 * ((cl_comb * 10) - cl_lib)) / 1000
        res_p2.markdown(f'<div class="box-dosaggio">🔥 Shock Chemacal 70<br><span class="misura-kg">{kg_shock:.2f} kg</span></div>', unsafe_allow_html=True)

# --- 2. SOLUZIONE ---
with tab2:
    st.header("Preparazione Soluzione")
    v_vasca = st.number_input("Volume Vasca (L)", value=100.0)
    l_prod = st.number_input("Litri prodotto versati (L)", value=10.0)
    perc_comm = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_prod/v_vasca)*perc_comm:.2f} %")

# --- 3. GESTIONE (Macchina e Ciclo) ---
with tab3:
    st.header("🚰 Verifica Macchina Installata")
    g1, g2 = st.columns(2)
    with g1:
        vr = st.number_input("Resina (L)", value=25)
        de = st.number_input("Durezza Entrata (°f)", value=35)
    with g2:
        du = st.number_input("Durezza Uscita (°f)", value=15)
        co = st.number_input("Consumo (m³/gg)", value=0.6)
    
    d_netta = max(0.1, de - du)
    cap_cic = vr * 5
    m3_aut = cap_cic / d_netta
    sale_rig = (vr * 140) / 1000
    gg_int = m3_aut / co if co > 0 else 0

    st.subheader("Dati di Ciclo")
    c_res1, c_res2 = st.columns(2)
    c_res1.metric("Autonomia", f"{m3_aut:.2f} m³", f"Ogni {gg_int:.1f} giorni")
    c_res2.metric("Sale / Ciclo", f"{sale_rig:.2f} kg", "A rigenerazione")

    st.subheader("Dettagli Tecnici Singola Rigenerazione")
    d1, d2, d3 = st.columns(3)
    d1.markdown(f'<div class="valore-box"><span class="label-tecnica">Cap. Ciclica</span><br><span class="dato-tecnico">{cap_cic} m³f</span></div>', unsafe_allow_html=True)
    d2.markdown(f'<div class="valore-box"><span class="label-tecnica">Salamoia</span><br><span class="dato-tecnico">{(sale_rig*3):.1f} L</span></div>', unsafe_allow_html=True)
    d3.markdown(f'<div class="valore-box"><span class="label-tecnica">Scarico</span><br><span class="dato-tecnico">{vr*7} L</span></div>', unsafe_allow_html=True)

# --- 4. PROGETTO (UNI 9182 e Risparmio) ---
with tab4:
    st.header("📐 Progettazione UNI 9182")
    pr1, pr2 = st.columns(2)
    with pr1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        p_in = st.number_input("Durezza In (°f)", value=35, key="pin")
        p_out = st.number_input("Durezza Out (°f)", value=15, key="pout")
    with pr2:
        if tipo == "Villetta":
            pers = st.number_input("Persone", value=4)
            f_gg = pers * 0.2
            q_p = 1.20
        else:
            app = st.number_input("Appartamenti", value=10)
            f_gg = (app * 3) * 0.2
            q_p = round(0.2 * math.sqrt(app * 3) + 0.8, 2)

    p_delta = max(0.1, p_in - p_out)
    taglia = min([t for t in [8,12,15,20,25,30,40,50,75,100,125,150,200,250,300] if t >= (f_gg*3*p_delta)/5] or [300])
    
    st.success(f"### Taglia Suggerita: {taglia} Litri Resina")
    
    c_p1, c_p2 = st.columns(2)
    c_p1.metric("Consumo Giornaliero", f"{f_gg:.2f} m³/gg")
    c_p2.metric("Portata di Picco", f"{q_p} m³/h")

    st.subheader("📊 Analisi Annuale: Standard vs Clack")
    n_rig = 365 / (((taglia * 5) / p_delta) / f_gg)
    s_std = (taglia * 0.14) * n_rig
    st.table({
        "Dati Annuali": ["Sale Totale", "Sacchi (25kg)", "Acqua Scarico", "N. Rigenerazioni"],
        "Standard": [f"{s_std:.0f} kg", f"{math.ceil(s_std/25)}", f"{(taglia*7*n_rig)/1000:.2f} m³", f"{n_rig:.0f}"],
        "Clack Impression": [f"{s_std*0.8:.0f} kg", f"{math.ceil(s_std*0.8/25)}", f"{(taglia*7*n_rig*0.8)/1000:.2f} m³", "Ottimizzata"]
    })
