import streamlit as st
import math

# --- 1. CONFIGURAZIONE E UTILITY ---
st.set_page_config(page_title="Progetto Piscine UNI 10637", layout="wide")

def suggerisci_pvc(d_interno):
    tabella_pvc = {32:28, 40:36, 50:45, 63:57, 75:69, 90:82, 110:100, 125:114, 140:127, 160:146, 200:184}
    for esterno, interno in tabella_pvc.items():
        if interno >= d_interno: return esterno
    return "N/D"

# --- 2. INPUT DATI (LAYOUT APPROVATO) ---
with st.sidebar:
    st.header("📋 Parametri di Progetto")
    L = st.number_input("Lunghezza (m)", value=12.0)
    W = st.number_input("Larghezza (m)", value=6.0)
    h_min = st.number_input("Prof. min (m)", value=1.0)
    h_max = st.number_input("Prof. max (m)", value=1.6)
    st.divider()
    st.header("🚀 Idraulica e Filtrazione")
    v_sabbia = st.slider("Velocità Filtro Sabbia (m/h)", 20, 50, 30)
    cap_bocchetta = st.number_input("Portata singola bocchetta (m³/h)", value=6.0)
    q_max_griglia = st.number_input("Portata max griglia fondo (m³/h)", value=15.0)

# --- 3. LOGICA DI CALCOLO (PROSPETTO 3) ---
superficie_tot = L * W
q_tot = 0
passo = 0.1
for i in range(int(L/passo)):
    h_c = h_min + (i * passo * (h_max - h_min) / L)
    t = 3.0 if h_c > 1.35 else (2.5 if h_c > 0.6 else (1.0 if h_c > 0.4 else 0.5))
    q_tot += ((passo * W) * h_c) / t

# --- 4. LOCALE TECNICO (FILTRAZIONE) ---
st.header("🏗️ Locale Tecnico e Filtrazione")
tipo_f = st.radio("Scegli tecnologia di filtrazione:", ["Sabbia", "Cartuccia"], horizontal=True)

f1, f2 = st.columns(2)
with f1:
    if tipo_f == "Cartuccia":
        v_effettiva = 1.0 # NORMA: 1mc x mq
        sup_f = q_tot / v_effettiva
        st.warning(f"**Norma UNI 10637:** Velocità fissata a {v_effettiva} m/h per cartuccia.")
        st.metric("Superficie Cartuccia Necessaria", f"{sup_f:.2f} m²")
    else:
        v_effettiva = v_sabbia
        sup_f = q_tot / v_effettiva
        diam_f = math.sqrt(sup_f / math.pi) * 2000
        st.metric("Superficie Sabbia Necessaria", f"{sup_f:.2f} m²")
        st.info(f"Ø Filtro consigliato: **{diam_f:.0f} mm**")

with f2:
    st.metric("Portata di Progetto (Q)", f"{q_tot:.2f} m³/h")
    prevalenza = st.selectbox("Prevalenza stimata (m.c.a.)", [10, 12, 15, 18], index=1)
    st.write(f"Pompa: **{q_tot:.2f} m³/h @ {prevalenza} m**")

# --- 5. COMPONENTI E IDRAULICA (STACCHI E COLLETTORI) ---
st.divider()
st.subheader("🏛️ Dimensionamento Collettori e Stacchi")

# Calcolo Stacchi
q_fo = q_tot / 2
d_fo = suggerisci_pvc(math.sqrt(((q_fo/3600)/1.7)/math.pi)*2000)

n_boc = math.ceil(q_tot / cap_bocchetta)
q_boc = q_tot / n_boc
d_boc = suggerisci_pvc(math.sqrt(((q_boc/3600)/2.5)/math.pi)*2000)

# Calcolo Collettori
d_coll_asp = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.0)/math.pi)*2000)
d_coll_man = suggerisci_pvc(math.sqrt(((q_tot/3600)/1.5)/math.pi)*2000)

col_info1, col_info2 = st.columns(2)
with col_info1:
    if superficie_tot <= 100:
        n_sk = math.ceil(superficie_tot / 20)
        q_sk = q_tot / n_sk
        d_sk = suggerisci_pvc(math.sqrt(((q_sk/3600)/1.7)/math.pi)*2000)
        st.write(f"✅ **N. {n_sk} Skimmer**: stacchi Ø {d_sk}")
    else:
        st.error("⚠️ OLTRE 100 m²: OBBLIGO BORDO SFIORATORE")

    st.write(f"✅ **N. 2 Prese Fondo**: stacchi Ø {d_fo} (in parallelo)")
    if q_fo > q_max_griglia: st.error(f"Portata eccessiva per griglia: {q_fo:.1f} m³/h")

with col_info2:
    st.write(f"✅ **N. {n_boc} Bocchette**: stacchi Ø {d_boc}")
    st.write(f"✅ **Collettore Asp.**: Ø {d_coll_asp}")
    st.write(f"✅ **Collettore Man.**: Ø {d_coll_man}")

# Tabella finale
st.table({
    "Tratto": ["Collettore Asp.", "Collettore Man.", "Stacco Skimmer", "Stacco Fondo", "Stacco Bocchetta"],
    "Portata (m³/h)": [q_tot, q_tot, (q_tot/n_sk if superficie_tot<=100 else 0), q_fo, q_boc],
    "Velocità (m/s)": [1.0, 1.5, 1.7, 1.7, 2.5],
    "Diametro PVC": [f"Ø {d_coll_asp}", f"Ø {d_coll_man}", f"Ø {d_sk if superficie_tot<=100 else 'N/A'}", f"Ø {d_fo}", f"Ø {d_boc}"]
})
