import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Acqualab Pool Assistant", page_icon="🏊", layout="centered")

# --- STILE CSS ---
st.markdown("""
    <style>
    .misura-grande { font-size: 36px !important; font-weight: bold; color: #FF4B4B; }
    .nome-prodotto { font-size: 18px; font-weight: 600; color: var(--text-color); }
    .unita-misura { font-size: 20px; color: #00AEEF; font-weight: bold; }
    .result-box { padding: 15px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.3); background-color: rgba(128, 128, 128, 0.05); margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏊 Acqualab Pool Assistant")

tab1, tab2 = st.tabs(["📊 Analisi e Dosaggi", "💧 Soluzione Vasca"])

with tab1:
    st.header("Calcolo Interventi Chimici")
    
    # INPUT DATI
    c1, c2 = st.columns(2)
    with c1:
        v_piscina = st.number_input("Volume Piscina (m³)", min_value=1.0, value=100.0)
        ph_ril = st.number_input("pH Rilevato", min_value=0.0, max_value=14.0, value=7.8, step=0.1)
        cl_totale = st.number_input("Cloro Totale (ppm)", min_value=0.0, value=1.5, step=0.1)
    with c2:
        cl_libero = st.number_input("Cloro Libero (ppm)", min_value=0.0, value=1.0, step=0.1)
        cya_ril = st.number_input("Acido Cianurico (ppm)", min_value=0.0, value=40.0)
        sale_ril = st.number_input("Sale Rilevato (mg/L)", min_value=0.0, value=0.0, step=100.0)
    
    cl_combinato = max(0.0, cl_totale - cl_libero)
    st.info(f"💡 Cloro Combinato (CC): **{cl_combinato:.2f} ppm**")

    if st.button("🚀 GENERA DOSAGGI", type="primary", use_container_width=True):
        st.divider()
        
        # 1. SEZIONE SALE
        st.subheader("🧂 Sale")
        sale_gl = sale_ril / 1000
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">Sale Standard (4.5 g/L):</span> <span class="misura-grande">{(v_piscina * max(0.0, 4.5 - sale_gl)):.0f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box"><span class="nome-prodotto">Bassa Salinità (1.5 g/L):</span> <span class="misura-grande">{(v_piscina * max(0.0, 1.5 - sale_gl)):.0f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

        # 2. SEZIONE PH
        st.subheader("📊 Correzione pH")
        if ph_ril > 7.2:
            diff = (ph_ril - 7.2) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">pH meno G:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">pH meno L 15%:</span> <span class="misura-grande">{(v_piscina*27*diff)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">pH meno L 40%:</span> <span class="misura-grande">{(v_piscina*9*diff)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)
        elif ph_ril < 7.2:
            diff = (7.2 - ph_ril) / 0.1
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">pH Plus G:</span> <span class="misura-grande">{(v_piscina*10*diff)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)

        # 3. SEZIONE CLORO
        st.subheader("🧪 Cloro (Target 1.5 ppm)")
        d_cl = max(0.0, 1.5 - cl_libero)
        col1, col2, col3 = st.columns(3)
        col1.markdown(f'**Chemacal 70**\n\n{(v_piscina*1.5*d_cl)/1000:.2f} kg')
        col2.markdown(f'**Power Clor 56**\n\n{(v_piscina*1.8*d_cl)/1000:.2f} kg')
        col3.markdown(f'**Chemaclor L**\n\n{(v_piscina*7*d_cl)/1000:.2f} L')

        # SHOCK
        if cl_combinato >= 0.4:
            st.warning("⚠️ TRATTAMENTO SHOCK NECESSARIO")
            ppm_shock = max(0.0, (cl_combinato * 10) - cl_libero)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">Shock Chemacal 70:</span> <span class="misura-grande">{(v_piscina*1.5*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">Shock Power Clor 56:</span> <span class="misura-grande">{(v_piscina*1.8*ppm_shock)/1000:.2f}</span> <span class="unita-misura">kg</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><span class="nome-prodotto">Shock Chemaclor L:</span> <span class="misura-grande">{(v_piscina*7*ppm_shock)/1000:.2f}</span> <span class="unita-misura">L</span></div>', unsafe_allow_html=True)

        # 4. STABILIZZANTE E ALGHICIDA
        st.subheader("🌿 Manutenzione")
        cya_reale = cya_ril / 2
        if cya_reale < 30:
            st.write(f"Acido Cianurico (Target 30): **{(v_piscina*(30-cya_reale))/1000:.2f} kg**")
        
        st.markdown(f"Algiprevent Inizio: **{(v_piscina*2)/100:.1f} L** | Urto: **{(v_piscina*5)/100:.1f} L** | Mant.: **{(v_piscina*1)/100:.1f} L**")

with tab2:
    st.header("Preparazione Soluzione Vasca")
    v_v = st.number_input("Volume Vasca Soluzione (L)", min_value=1.0, value=100.0)
    l_i = st.number_input("Litri prodotto versati (L)", value=10.0)
    p_p = st.number_input("% Prodotto Commerciale", value=15.0)
    st.success(f"### ✅ Valore in programmazione: {(l_i / v_v) * p_p if v_v > 0 else 0:.2f} %")
