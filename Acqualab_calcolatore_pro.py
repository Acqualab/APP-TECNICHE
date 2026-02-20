# --- TAB 4: PROGETTO (Versione Aggiornata) ---
with tab4:
    st.header("📐 Progettazione Nuovo Impianto")
    
    cp1, cp2 = st.columns(2)
    with cp1:
        tipo = st.selectbox("Tipo Utenza", ["Villetta / Abitazione Singola", "Condominio / Plurifamiliare"])
        dur_ingresso = st.number_input("Durezza Acqua Grezza (°f)", min_value=1, value=35)
    
    with cp2:
        dur_desiderata = st.number_input("Durezza Miscelata desiderata (°f)", min_value=0, value=15)
        if tipo == "Villetta / Abitazione Singola":
            persone = st.number_input("Numero persone totali", min_value=1, value=4)
            cons_pro = persone * 0.200 
            picco_pro = 1.20 
        else:
            app = st.number_input("Numero appartamenti", min_value=1, value=10)
            persone = app * 3 
            cons_pro = persone * 0.200
            picco_pro = round(0.20 * math.sqrt(persone) + 0.8, 2)

    # Calcolo Durezza Reale da abbattere
    dur_netta = max(0, dur_ingresso - dur_desiderata)

    st.markdown('<p class="titolo-sezione">Dati di Progetto</p>', unsafe_allow_html=True)
    res_p1, res_p2 = st.columns(2)
    res_p1.metric("Consumo giornaliero stimato", f"{cons_pro:.2f} m³/gg")
    res_p2.metric("Portata di Picco (UNI 9182)", f"{picco_pro:.2f} m³/h")

    st.markdown("---")
    
    # CALCOLO DIMENSIONAMENTO CON DUREZZA NETTA
    if dur_netta > 0:
        resina_necessaria = (cons_pro * 3 * dur_netta) / 5
        taglie = [8, 12, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300]
        taglia_scelta = min([t for t in taglie if t >= resina_necessaria] or [max(taglie)])

        st.subheader("🛠 Configurazione Impianto Suggerita")
        st.markdown(f"""
        <div class="result-box">
            <span class="nome-prodotto">Taglia Addolcitore Consigliata:</span> <span class="misura-grande" style="color:#00AEEF">{taglia_scelta}</span> <span class="unita-misura">Litri Resina</span><br>
            <p style="margin-top:10px;"><b>Analisi Tecnica:</b><br>
            • Durezza da abbattere: {dur_netta} °f<br>
            • Portata Valvola richiesta: > {picco_pro} m³/h<br>
            • Autonomia reale: {((taglia_scelta*5)/dur_netta)/cons_pro:.1f} giorni</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("La durezza desiderata è maggiore o uguale a quella in ingresso. Nessun trattamento necessario.")
