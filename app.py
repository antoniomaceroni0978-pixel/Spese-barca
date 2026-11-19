import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

st.set_page_config(page_title="Gestione Spese Barca", page_icon="⛵", layout="centered")

st.title("⛵ Gestione Spese Barca")
st.markdown("Tieni traccia di entrate, spese condivise, somme previste e attività.")

if "transazioni" not in st.session_state:
    st.session_state.transazioni = pd.DataFrame(columns=[
        "Data", "Tipo", "Categoria", "Descrizione", "Importo", "Pagato Da", "Coinvolti"
    ])

if "somme_previste" not in st.session_state:
    st.session_state.somme_previste = pd.DataFrame(columns=[
        "Descrizione", "Importo Previsto", "Categoria", "Stato"
    ])

if "attivita_ore" not in st.session_state:
    st.session_state.attivita_ore = pd.DataFrame(columns=[
        "Data", "Attività / Lavoro", "Ore", "Tariffa Oraria (€)", "Totale Stimato (€)"
    ])

io = "Antonio"
socio = "Tonino"
soci = [io, socio]

st.sidebar.header("⚙️ Menu Operazioni")
scelta_menu = st.sidebar.radio("Seleziona sezione", [
    "Registra Operazione",
    "Somme previste",
    "🛠️ Note operative"
])

if scelta_menu == "Registra Operazione":
    st.sidebar.subheader("➕ Nuova Operazione Reale")
    tipo = st.sidebar.selectbox("Tipo di operazione", ["Spesa", "Entrata", "Rimborso tra soci"])
    data = st.sidebar.date_input("Data", date.today())
    importo = st.sidebar.number_input("Importo (€)", min_value=0.0, step=10.0, format="%.2f")
    descrizione = st.sidebar.text_input("Descrizione", value="")

    if tipo == "Spesa":
        categoria = st.sidebar.selectbox("Categoria", ["Carburante", "Ormeggio", "Manutenzione Ordinaria", "Manutenzione Straordinaria", "Assicurazione", "Altro"])
        pagato_da = st.sidebar.selectbox("Pagato da chi?", soci)
        coinvolti = st.sidebar.multiselect("Diviso tra", soci, default=soci)
    elif tipo == "Entrata":
        categoria = "Entrata Comune (es. Charter)"
        pagato_da = "Cassa Comune"
        coinvolti = soci
    else:
        categoria = "Rimborso"
        pagato_da = st.sidebar.selectbox("Chi ha fatto il bonifico/pagamento?", soci)
        ricevuto_da = [s for s in soci if s != pagato_da][0]
        coinvolti = [ricevuto_da]
        descrizione = f"Rimborso da {pagato_da} a {ricevuto_da}"

    if st.sidebar.button("Registra Operazione"):
        if importo > 0:
            nuova_riga = {
                "Data": data,
                "Tipo": tipo,
                "Categoria": categoria,
                "Descrizione": descrizione,
                "Importo": importo,
                "Pagato Da": pagato_da,
                "Coinvolti": ", ".join(coinvolti) if isinstance(coinvolti, list) else coinvolti
            }
            nuovo_df = pd.DataFrame([nuova_riga])
            st.session_state.transazioni = pd.concat([st.session_state.transazioni, nuovo_df], ignore_index=True)
            st.sidebar.success("Operazione registrata!")
            st.rerun()
        else:
            st.sidebar.error("Inserisci un importo maggiore di zero.")

elif scelta_menu == "Somme previste":
    st.sidebar.subheader("📌 Aggiungi somma prevista")
    f_desc = st.sidebar.text_input("Nome voce (es. Assicurazione Annuale)", value="")
    f_importo = st.sidebar.number_input("Importo previsto (€)", min_value=0.0, step=50.0, value=0.0, format="%.2f")
    f_cat = st.sidebar.selectbox("Categoria", ["Assicurazione", "Ormeggio Annuale", "Manutenzione", "Altro"])
    f_attiva = st.sidebar.checkbox("Includi nei totali", value=True)

    if st.sidebar.button("Aggiungi somma prevista"):
        if f_importo > 0 and f_desc.strip():
            nuova_voce = {
                "Descrizione": f_desc.strip(),
                "Importo Previsto": f_importo,
                "Categoria": f_cat,
                "Stato": "Attiva" if f_attiva else "Disattivata"
            }
            nuovo_vdf = pd.DataFrame([nuova_voce])
            st.session_state.somme_previste = pd.concat([st.session_state.somme_previste, nuovo_vdf], ignore_index=True)
            st.sidebar.success("Somma prevista aggiunta!")
            st.rerun()
        else:
            st.sidebar.error("Inserisci una descrizione e un importo valido.")

else:
    st.sidebar.subheader("🛠️ Registra attività")
    st.sidebar.info("Le attività registrate qui vengono considerate nel riepilogo generale dei conti.")
    m_data = st.sidebar.date_input("Data attività", date.today(), key="m_data")
    m_desc = st.sidebar.text_input("Descrizione attività (es. Lucidatura opera viva)", value="", key="m_desc")
    m_ore = st.sidebar.number_input("Ore impiegate", min_value=0.5, step=0.5, value=2.0, key="m_ore")
    m_tariffa = st.sidebar.number_input("Tariffa oraria (€/h)", min_value=0.0, step=5.0, value=25.0, key="m_tariffa")

    if st.sidebar.button("Registra attività"):
        if m_desc.strip() and m_ore > 0:
            tot_valore = m_ore * m_tariffa
            nuova_mano = {
                "Data": m_data,
                "Attività / Lavoro": m_desc.strip(),
                "Ore": m_ore,
                "Tariffa Oraria (€)": m_tariffa,
                "Totale Stimato (€)": tot_valore
            }
            nuovo_mdf = pd.DataFrame([nuova_mano])
            st.session_state.attivita_ore = pd.concat([st.session_state.attivita_ore, nuovo_mdf], ignore_index=True)
            st.sidebar.success("Attività registrata!")
            st.rerun()
        else:
            st.sidebar.error("Compila correttamente i campi.")

st.subheader("📊 Situazione Finanziaria Condivisa")

df = st.session_state.transazioni
df_previste = st.session_state.somme_previste
df_attivita = st.session_state.attivita_ore

totale_spese_reali = df[df["Tipo"] == "Spesa"]["Importo"].sum() if not df.empty else 0.0
totale_previste_attivo = df_previste[df_previste["Stato"] == "Attiva"]["Importo Previsto"].sum() if not df_previste.empty else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Spese Reali Totali", f"{totale_spese_reali:.2f} €")
col2.metric("Somme previste", f"{totale_previste_attivo:.2f} €")
col3.metric("Totale Complessivo", f"{totale_spese_reali + totale_previste_attivo:.2f} €")

saldi = {io: 0.0, socio: 0.0}

if not df.empty:
    for _, row in df.iterrows():
        imp = float(row["Importo"])
        paga = row["Pagato Da"]
        if row["Tipo"] == "Spesa":
            if paga in saldi:
                saldi[paga] += imp
            partecipanti = row["Coinvolti"].split(", ") if isinstance(row["Coinvolti"], str) else row["Coinvolti"]
            quota_parte = imp / len(partecipanti) if len(partecipanti) > 0 else imp
            for p in partecipanti:
                if p in saldi:
                    saldi[p] -= quota_parte
        elif row["Tipo"] == "Rimborso":
            if paga in saldi:
                saldi[paga] += imp
            ricevente = row["Coinvolti"] if isinstance(row["Coinvolti"], str) else row["Coinvolti"][0]
            if recevente in saldi:
                saldi[recevente] -= imp

if not df_attivita.empty:
    for _, row in df_attivita.iterrows():
        valore_lavoro = float(row["Totale Stimato (€)"])
        saldi[io] += valore_lavoro
        quota_parte = valore_lavoro / len(soci)
        for s in soci:
            saldi[s] -= quota_parte

testo_regolamento = ""
if not df.empty or not df_attivita.empty:
    st.markdown("---")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.metric(label=f"Bilancio Finale {io}", value=f"{saldi[io]:.2f} €")
    with s_col2:
        st.metric(label=f"Bilancio Finale {socio}", value=f"{saldi[socio]:.2f} €")

    diff = saldi[io] - saldi[socio]
    if abs(diff) > 0.05:
        if diff > 0:
            testo_regolamento = f"{socio} deve dare {diff / 2:.2f} € a {io}."
            st.info(f"💡 **Regolamento conti:** {testo_regolamento}")
        else:
            testo_regolamento = f"{io} deve dare {abs(diff) / 2:.2f} € a {socio}."
            st.info(f"💡 **Regolamento conti:** {testo_regolamento}")

if not df_previste.empty:
    with st.expander("📌 Visualizza Somme previste"):
        st.dataframe(df_previste, use_container_width=True)

if not df.empty:
    with st.expander("📜 Visualizza Storico Movimenti Reali (Spese/Entrate)"):
        st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("🖨️ Report per Tonino (Stampa / PDF ed Excel)")
st.markdown("Esporta un riepilogo pulito con tutti i record, somme previste e conguaglio.")

buffer_excel = BytesIO()
riepilogo_dati = pd.DataFrame([
    {"Voce": "Data Report", "Valore": str(date.today())},
    {"Voce": "Spese Reali Totali (€)", "Valore": round(float(totale_spese_reali), 2)},
    {"Voce": "Somme Previste Attive (€)", "Valore": round(float(totale_previste_attivo), 2)},
    {"Voce": "Totale Complessivo (€)", "Valore": round(float(totale_spese_reali + totale_previste_attivo), 2)},
    {"Voce": f"Bilancio Finale {io} (€)", "Valore": round(float(saldi[io]), 2)},
    {"Voce": f"Bilancio Finale {socio} (€)", "Valore": round(float(saldi[socio]), 2)},
    {"Voce": "Regolamento Conti", "Valore": testo_regolamento if testo_regolamento else "Conti in pareggio"}
])

df_previste_out = df_previste.copy() if not df_previste.empty else pd.DataFrame(columns=["Descrizione", "Importo Previsto", "Categoria", "Stato"])
df_out = df.copy() if not df.empty else pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Descrizione", "Importo", "Pagato Da", "Coinvolti"])
df_spese_out = df[df["Tipo"] == "Spesa"].copy() if not df.empty else pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Descrizione", "Importo", "Pagato Da", "Coinvolti"])
