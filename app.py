Import streamlit as st
Import pandas as pd
From datetime import date

    St.set_page_config(page_title=”Gestione Spese Barca”, page_icon=”⛵”, layout=”centered”)

    St.title(“⛵ Gestione Spese Barca”)
    St.markdown(“Tieni traccia di entrate, spese condivise, voci previste e manodopera personale.”)[span_4](start_span)[span_4](end_span)

If “transazioni” not in st.session_state:
    st.session_state.transazioni = pd.DataFrame(columns=[
        “Data”, “Tipo”, “Categoria”, “Descrizione”, “Importo”, “Pagato Da”, “Coinvolti”
    ])

If “voci_fantasma” not in st.session_state:
    st.session_state.voci_fantasma = pd.DataFrame(columns=[
        “Descrizione”, “Importo Previsto”, “Categoria”, “Stato”
    ])

If “manodopera_privata” not in st.session_state:
    st.session_state.manodopera_privata = pd.DataFrame(columns=[
        “Data”, “Attività / Lavoro”, “Ore”, “Tariffa Oraria (€)”, “Totale Stimato (€)”
    ])

Soci = [“Tu”, “Socio”]

St.sidebar.header(“⚙️ Menu Operazioni”)
Scelta_menu = st.sidebar.radio(“Seleziona sezione”, [
    “Registra Operazione”,
    “Voci Fantasma / Previste”,
    “🛠️ Manodopera Personale (Privata)”
])

If scelta_menu == “Registra Operazione”:
    st.sidebar.subheader(“➕ Nuova Operazione Reale”)
    tipo = st.sidebar.selectbox(“Tipo di operazione”, [“Spesa”, “Entrata”, “Rimborso tra soci”])
    data = st.sidebar.date_input(“Data”, date.today())
    importo = st.sidebar.number_input(“Importo (€)”, min_value=0.0, step=10.0, format=”%.2f”)
    descrizione = st.sidebar.text_input(“Descrizione”)

    if tipo == “Spesa”:
        categoria = st.sidebar.selectbox(“Categoria”, [“Carburante”, “Ormeggio”, “Manutenzione Ordinaria”, “Manutenzione Straordinaria”, “Assicurazione”, “Altro”])
        pagato_da = st.sidebar.selectbox(“Pagato da chi?”, soci)
        coinvolti = st.sidebar.multiselect(“Diviso tra”, soci, default=soci)
    elif tipo == “Entrata”:
        categoria = “Entrata Comune (es. Charter)”
        pagato_da = “Cassa Comune”
        coinvolti = soci
    else:
        categoria = “Rimborso”
        pagato_da = st.sidebar.selectbox(“Chi ha fatto il bonifico/pagamento?”, soci)
        ricevuto_da = [s for s in soci if s != pagato_da][0]
        coinvolti = [ricevuto_da]
        descrizione = f”Rimborso da {pagato_da} a {ricevuto_da}”

    if st.sidebar.button(“Registra Operazione”):
        if importo > 0:
            nuova_riga = {
                “Data”: data,
                “Tipo”: tipo,
                “Categoria”: categoria,
                “Descrizione”: descrizione,
                “Importo”: importo,
                “Pagato Da”: pagato_da,
                “Coinvolti”: “, “.join(coinvolti) if isinstance(coinvolti, list) else coinvolti
            }
            Nuovo_df = pd.DataFrame([nuova_riga])
            St.session_state.transazioni = pd.concat([st.session_state.transazioni, nuovo_df], ignore_index=True)
            St.sidebar.success(“Operazione registrata!”)
            St.rerun()
        Else:
            st.sidebar.error(“Inserisci un importo maggiore di zero.”)

elif scelta_menu == “Voci Fantasma / Previste”:
    st.sidebar.subheader(“👻 Aggiungi Voce Fantasma”)
    f_desc = st.sidebar.text_input(“Nome Voce (es. Assicurazione Annuale)”, value=””)
    f_importo = st.sidebar.number_input(“Importo Previsto (€)”, min_value=0.0, step=50.0, value=0.0, format=”%.2f”)
    f_cat = st.sidebar.selectbox(“Categoria”, [“Assicurazione”, “Ormeggio Annuale”, “Manutenzione”, “Altro”])
    f_attiva = st.sidebar.checkbox(“Includi nei totali”, value=True)

    if st.sidebar.button(“Aggiungi Voce Fantasma”):
        if f_importo > 0 and f_desc.strip():
            nuova_voce = {
                “Descrizione”: f_desc.strip(),
                “Importo Previsto”: f_importo,
                “Categoria”: f_cat,
                “Stato”: “Attiva” if f_attiva else “Disattivata”
            }
            Nuovo_vdf = pd.DataFrame([nuova_voce])
            St.session_state.voci_fantasma = pd.concat([st.session_state.voci_fantasma, nuovo_vdf], ignore_index=True)
            St.sidebar.success(“Voce fantasma aggiunta!”)
            St.rerun()
        Else:
            st.sidebar.error(“Inserisci una descrizione e un importo valido.”)

else:
    st.sidebar.subheader(“🛠️ Registra Lavoro Personale”)
    st.sidebar.info(“Partecipa al calcolo dei saldi fra soci (diviso a metà), ma non appare come spesa nello storico.”)
    m_data = st.sidebar.date_input(“Data Lavoro”, date.today(), key=”m_data”)
    m_desc = st.sidebar.text_input(“Descrizione Lavoro (es. Lucidatura opera viva)”, value=””, key=”m_desc”)
    m_ore = st.sidebar.number_input(“Ore impiegate”, min_value=0.5, step=0.5, value=2.0, key=”m_ore”)
    m_tariffa = st.sidebar.number_input(“Valore / Tariffa Oraria (€/h)”, min_value=0.0, step=5.0, value=25.0, key=”m_tariffa”)

    if st.sidebar.button(“Registra Manodopera Privata”):
        if m_desc.strip() and m_ore > 0:
            tot_valore = m_ore * m_tariffa
            nuova_mano = {
                “Data”: m_data,
                “Attività / Lavoro”: m_desc.strip(),
                “Ore”: m_ore,
                “Tariffa Oraria (€)”: m_tariffa,
                “Totale Stimato (€)”: tot_valore
            }
            Nuovo_mdf = pd.DataFrame([nuova_mano])
            St.session_state.manodopera_privata = pd.concat([st.session_state.manodopera_privata, nuovo_mdf], ignore_index=True)
            St.sidebar.success(“Lavoro registrato e integrato nei calcoli di saldo!”)
            St.rerun()
        Else:
            st.sidebar.error(“Compila correttamente i campi.”)

st.subheader(“📊 Situazione Finanziaria Condivisa”)

df = st.session_state.transazioni
df_fantasma = st.session_state.voci_fantasma
df_privata = st.session_state.manodopera_privata

totale_spese_reali = df[df[“Tipo”] == “Spesa”][“Importo”].sum() if not df.empty else 0.0
totale_fantasma_attivo = df_fantasma[df_fantasma[“Stato”] == “Attiva”][“Importo Previsto”].sum() if not df_fantasma.empty else 0.0

col1, col2, col3 = st.columns(3)
col1.metric(“Spese Reali Totali”, f”{totale_spese_reali:.2f} €”)
col2.metric(“Voci Previste”, f”{totale_fantasma_attivo:.2f} €”)
col3.metric(“Totale Complessivo”, f”{totale_spese_reali + totale_fantasma_attivo:.2f} €”)

saldi = {socio: 0.0 for socio in soci}

if not df.empty:
    for _, row in df.iterrows():
        imp = float(row[“Importo”])
        paga = row[“Pagato Da”]
        if row[“Tipo”] == “Spesa”:
            if paga in saldi:
                saldi[paga] += imp
            partecipanti = row[“Coinvolti”].split(“, “) if isinstance(row[“Coinvolti”], str) else row[“Coinvolti”]
            quota_parte = imp / len(partecipanti) if len(partecipanti) > 0 else imp
            for p in partecipanti:
                if p in saldi:
                    saldi[p] -= quota_parte
        elif row[“Tipo”] == “Rimborso”:
            if paga in saldi:
                saldi[paga] += imp
            ricevente = row[“Coinvolti”] if isinstance(row[“Coinvolti”], str) else row[“Coinvolti”][0]
            if recevente in saldi:
                saldi[recevente] -= imp

if not df_privata.empty:
    for _, row in df_privata.iterrows():
        valore_lavoro = float(row[“Totale Stimato (€)”])
        saldi[“Tu”] += valore_lavoro
        quota_parte = valore_lavoro / len(soci)
        for s in soci:
            saldi[s] -= quota_parte

if not df.empty or not df_privata.empty:
    st.markdown(“---“)
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.metric(label=f”Bilancio Finale {soci[0]}”, value=f”{saldi[soci[0]]:.2f} €”)
    with s_col2:
        st.metric(label=f”Bilancio Finale {soci[1]}”, value=f”{saldi[soci[1]]:.2f} €”)

    diff = saldi[soci[0]] – saldi[soci[1]]
    if abs(diff) > 0.05:
        if diff > 0:
            st.info(f”💡 **Regolamento conti (inclusa la manodopera):** {soci[1]} deve dare **{diff / 2:.2f} €** a {soci[0]}.”)
        else:
            st.info(f”💡 **Regolamento conti (inclusa la manodopera):** {soci[0]} deve dare **{abs(diff) / 2:.2f} €** a {soci[1]}.”)

st.markdown(“---“)
st.subheader(“🔒 Area Riservata: Il Tuo Lavoro Personale”)
st.markdown(“Queste ore partecipano al calcolo dei conguagli economici, ma non appaiono come voci di spesa pubbliche nello storico.”)

if not df_privata.empty:
    st.dataframe(df_privata, use_container_width=True)
    tot_ore_lavoro = df_privata[“Ore”].sum()
    tot_valore_lavoro = df_privata[“Totale Stimato (€)”].sum()

    p_col1, p_col2 = st.columns(2)
    p_col1.metric(“Totale Ore Lavorate”, f”{tot_ore_lavoro} ore”)
    p_col2.metric(“Valore Totale Riconosciuto”, f”{tot_valore_lavoro:.2f} €”)

    if st.button(“Cancella Storico Manodopera”):
        st.session_state.manodopera_privata = pd.DataFrame(columns=[“Data”, “Attività / Lavoro”, “Ore”, “Tariffa Oraria (€)”, “Totale Stimato (€)”])
        st.rerun()
else:
    st.info(“Nessun lavoro personale registrato.”)

if not df_fantasma.empty:
    with st.expander(“👻 Visualizza Voci Fantasma / Previste”):
        st.dataframe(df_fantasma, use_container_width=True)

if not df.empty:
    with st.expander(“📜 Visualizza Storico Movimenti Reali (Spese/Entrate)”):
        st.dataframe(df, use_container_width=True)
        if st.button(“Esporta movimenti reali in CSV”):
            csv = df.to_csv(index=False).encode(“utf-8”)
            st.download_button(“Scarica CSV”, data=csv, file_name=”spese_barca.csv”, mime=”text/csv”)

