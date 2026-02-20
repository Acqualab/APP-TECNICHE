import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Softener PRO", page_icon="🚰", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .valore-evidenziato { font-size: 32px !important; font-weight: bold; color: #00AEEF; }
    .titolo-sezione { font-size: 20px; font-weight: bold; color: var(--text-color); border-bottom: 2px solid #00AEEF; margin-bottom: 15px; margin-top: 10px; }
    .result-box { padding: 15px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.3); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚰 Acqualab Softener PRO")

tab1, tab2 = st.tabs(["⚙️ Gestione Impianto", "📐 Progettazione PRO"])

# --- TAB 1: GESTIONE ESISTENTE ---
with tab1:
    st.header("Verifica Impianto Installato")
    c1, c2 = st.columns(2)
    with c1:
        v_resina = st.number_input("Volume Resina (Litri)", min_value=1, value=25)
        dur_in = st.number_input("Durezza Acqua Grezza (°f)", min_value=1, value=35)
    with c2:
        dur_out = st.number_input("Durezza Miscelata Uscita (°f)", min_value=0, value=15)
        cons_m3 = st.number_input("Consumo Acqua Giornaliero (m³)", min_value=0.01, value=0.6, step=0.1)

    dur_abb = dur_in - dur_out
    if dur_abb > 0:
        cap_c = v_resina * 5 
        m3_c = cap_c / dur_abb
        gg_a = m3_c / cons_m3
        s_rig = (v_resina * 140) / 1000
        
        st.markdown('<p class="titolo-sezione">Risultati Ciclo</p>', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.write("🌊 **Produzione Acqua Dolce**")
            st.markdown(f'<div class="result-box"><span class="valore-evidenziato">{m3_c:.2f} m³</span></div>', unsafe_allow_html=True)
            st.caption(f"Rigenerazione ogni {gg_a:.1f} giorni")
        with r2:
            st.write("🧂 **Consumo Sale**")
            st.markdown(f'<div class="result-box"><span class="valore-evidenziato">{s_rig:.2f} kg</span></div>', unsafe_allow_html=True)
            st.caption("Per singola rigenerazione")
            
        st.divider()
        d1, d2, d3 = st.columns(3)
        d1.metric("Cap. Ciclica", f"{cap_c} m³f")
        d2.metric("Vol. Salamoia", f"{s_rig * 3:.1f} L")
        d3.metric("Scarico stimato", f"{v_resina * 7} L")

# --- TAB 2: PROGETTAZIONE E CLACK ---
with tab2:
    st.header("Dimensionamento e Risparmio")
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo_ut = st.selectbox("Tipo Utenza", ["Villetta", "Condominio"])
        d_ingresso = st.number_input("Durezza Acquedotto (°f)", value=35, key="p_di")
        d_mix_des = st.number_input("Durezza Mix Desiderata (°f)", value=15, key="p_dm")
    with cp2:
        if tipo_ut == "Villetta":
            pers = st.number_input("Numero Persone", value=4)
            f_gg = pers * 0.2
            p_picco = 1.2
        else:
            apps = st.number_input("Numero Appartamenti", value=10)
            f_gg = (apps * 3) * 0.2
            p_picco = round(0.2 * math.sqrt(apps * 3) + 0.8, 2)

    d_netta = max(0.1, d_ingresso - d_mix_des)
    r_id = (f_gg * 4 * d_netta) / 5
    taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
    t_p = min([t for t in taglie if t >= r_id] or [300])
    
    m3_p = (t_p * 5) / d_netta
    gg_p = m3_p / f_gg if f_gg > 0 else 0

    st.markdown(f'<div class="result-box" style="border-left: 5px solid #00AEEF;">'
                f'🎯 <b>Taglia Suggerita: {t_p} Litri</b><br>'
                f
