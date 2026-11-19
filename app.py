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

totale_spese_reali = pd.to_numeric(df[df["Tipo"] == "Spesa"]["Importo"], errors="coerce").fillna(0.0).sum() if not df.empty else 0.0
totale_previste_attivo = pd.to_numeric(df_previste[df_previste["Stato"] == "Attiva"]["Importo Previsto"], errors="coerce").fillna(0.0).sum() if not df_previste.empty else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Spese Reali Totali", f"{totale_spese_reali:.2f} €")
col2.metric("Somme previste", f"{totale_previste_attivo:.2f} €")
col3.metric("Totale Complessivo", f"{totale_spese_reali + totale_previste_attivo:.2f} €")

saldi = {io: 0.0, socio: 0.0}

if not df.empty:
    for _, row in df.iterrows():
        imp = float(pd.to_numeric(row.get("Importo", 0.0), errors="coerce") or 0.0)
        paga = row.get("Pagato Da", "")
        if row.get("Tipo") == "Spesa":
            if paga in saldi:
                saldi[paga] += imp
            coinvolti_val = row.get("Coinvolti", "")
            partecipanti = coinvolti_val.split(", ") if isinstance(coinvolti_val, str) and coinvolti_val else (coinvolti_val if isinstance(coinvolti_val, list) else soci)
            quota_parte = imp / len(partecipanti) if len(partecipanti) > 0 else imp
            for p in partecipanti:
                if p in saldi:
                    saldi[p] -= quota_parte
        elif row.get("Tipo") == "Rimborso":
            if paga in saldi:
                saldi[paga] += imp
            coinvolti_val = row.get("Coinvolti", "")
            ricevente = coinvolti_val if isinstance(coinvolti_val, str) else (coinvolti_val[0] if coinvolti_val else "")
            if ricevente in saldi:
                saldi[ricevente] -= imp

if not df_attivita.empty:
    for _, row in df_attivita.iterrows():
        valore_lavoro = float(pd.to_numeric(row.get("Totale Stimato (€)", 0.0), errors="coerce") or 0.0)
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
    with st.expander("📌 Visualizza e modifica Somme previste"):
        st.caption("Modifica i valori nelle celle o elimina righe, poi clicca su Salva modifiche.")
        prevista_mod = df_previste.copy()
        prevista_mod = st.data_editor(
            prevista_mod,
            num_rows="dynamic",
            use_container_width=True,
            key="editor_previste"
        )
        if st.button("💾 Salva modifiche Somme previste"):
            st.session_state.somme_previste = prevista_mod
            st.success("Somme previste aggiornate!")
            st.rerun()

if not df.empty:
    with st.expander("📜 Visualizza e modifica Storico Movimenti Reali (Spese/Entrate)"):
        st.caption("Clicca su una cella per correggere importo, descrizione, data o chi ha pagato.")
        movimenti_mod = df.copy()
        movimenti_mod = st.data_editor(
            movimenti_mod,
            num_rows="dynamic",
            use_container_width=True,
            key="editor_movimenti"
        )
        if st.button("💾 Salva modifiche Movimenti"):
            st.session_state.transazioni = movimenti_mod
            st.success("Movimenti reali aggiornati!")
            st.rerun()

if not df_attivita.empty:
    with st.expander("🛠️ Gestisci Note operative"):
        st.caption("Modifica ore, tariffa o attività, oppure rimuovi singole righe.")
        attivita_mod = df_attivita.copy()
        attivita_mod = st.data_editor(
            attivita_mod,
            num_rows="dynamic",
            use_container_width=True,
            key="editor_attivita"
        )
        if "Ore" in attivita_mod.columns and "Tariffa Oraria (€)" in attivita_mod.columns:
            attivita_mod["Totale Stimato (€)"] = (
                pd.to_numeric(attivita_mod["Ore"], errors="coerce").fillna(0.0)
                * pd.to_numeric(attivita_mod["Tariffa Oraria (€)"], errors="coerce").fillna(0.0)
            )
        if st.button("💾 Salva modifiche Note operative"):
            st.session_state.attivita_ore = attivita_mod
            st.success("Note operative aggiornate!")
            st.rerun()

st.markdown("---")
st.subheader("🖨️ Report per Tonino (Stampa / PDF ed Excel)")
st.markdown("Esporta un riepilogo pulito con tutte le singole voci, somme previste e conguaglio.")

buffer_excel = BytesIO()

riepilogo_righe = [
    {"Voce": "Data Report", "Valore": str(date.today())},
    {"Voce": "Spese Reali Totali (€)", "Valore": round(float(totale_spese_reali), 2)},
    {"Voce": "Somme Previste Attive (€)", "Valore": round(float(totale_previste_attivo), 2)},
    {"Voce": "Totale Complessivo (€)", "Valore": round(float(totale_spese_reali + totale_previste_attivo), 2)},
    {"Voce": f"Bilancio Finale {io} (€)", "Valore": round(float(saldi[io]), 2)},
    {"Voce": f"Bilancio Finale {socio} (€)", "Valore": round(float(saldi[socio]), 2)},
    {"Voce": "Regolamento Conti", "Valore": testo_regolamento if testo_regolamento else "Conti in pareggio"}
]
riepilogo_dati = pd.DataFrame(riepilogo_righe)

voci_movimenti = []
if not df.empty:
    for _, r in df.iterrows():
        voci_movimenti.append({
            "Data": str(r.get("Data", "")),
            "Tipo": str(r.get("Tipo", "")),
            "Categoria": str(r.get("Categoria", "")),
            "Descrizione": str(r.get("Descrizione", "")),
            "Importo (€)": round(float(pd.to_numeric(r.get("Importo", 0.0), errors="coerce") or 0.0), 2),
            "Pagato Da": str(r.get("Pagato Da", "")),
            "Coinvolti": str(r.get("Coinvolti", ""))
        })
df_out = pd.DataFrame(voci_movimenti) if voci_movimenti else pd.DataFrame(
    columns=["Data", "Tipo", "Categoria", "Descrizione", "Importo (€)", "Pagato Da", "Coinvolti"]
)

voci_spese = [v for v in voci_movimenti if v["Tipo"] == "Spesa"]
df_spese_out = pd.DataFrame(voci_spese) if voci_spese else pd.DataFrame(
    columns=["Data", "Tipo", "Categoria", "Descrizione", "Importo (€)", "Pagato Da", "Coinvolti"]
)

voci_previste = []
if not df_previste.empty:
    for _, r in df_previste.iterrows():
        voci_previste.append({
            "Descrizione": str(r.get("Descrizione", "")),
            "Categoria": str(r.get("Categoria", "")),
            "Stato": str(r.get("Stato", "")),
            "Importo Previsto (€)": round(float(pd.to_numeric(r.get("Importo Previsto", 0.0), errors="coerce") or 0.0), 2)
        })
df_previste_out = pd.DataFrame(voci_previste) if voci_previste else pd.DataFrame(
    columns=["Descrizione", "Categoria", "Stato", "Importo Previsto (€)"]
)

with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
    riepilogo_dati.to_excel(writer, sheet_name="Riepilogo", index=False)
    df_out.to_excel(writer, sheet_name="Tutti i Movimenti", index=False)
    df_spese_out.to_excel(writer, sheet_name="Solo Spese", index=False)
    df_previste_out.to_excel(writer, sheet_name="Somme Previste", index=False)

col_rep1, col_rep2 = st.columns(2)

with col_rep1:
    st.download_button(
        label="📊 Scarica Report Excel (.xlsx)",
        data=buffer_excel.getvalue(),
        file_name=f"report_spese_barca_{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_rep2:
    righe_movimenti = ""
    if not df.empty:
        for _, r in df.iterrows():
            imp_val = float(pd.to_numeric(r.get("Importo", 0.0), errors="coerce") or 0.0)
            righe_movimenti += f"<li>{r.get('Data', '')} – {r.get('Tipo', '')} ({r.get('Categoria', '')}): {r.get('Descrizione', '')} — <b>{imp_val:.2f} €</b> (Pagato da: {r.get('Pagato Da', '')})</li>"
    else:
        righe_movimenti = "<li>Nessun movimento registrato</li>"

    righe_previste = ""
    if not df_previste.empty:
        for _, r in df_previste.iterrows():
            prev_val = float(pd.to_numeric(r.get("Importo Previsto", 0.0), errors="coerce") or 0.0)
            righe_previste += f"<li>{r.get('Descrizione', '')} ({r.get('Categoria', '')}, {r.get('Stato', '')}): <b>{prev_val:.2f} €</b></li>"
    else:
        righe_previste = "<li>Nessuna somma prevista</li>"

    html_report = f"""
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: Arial, sans-serif; padding: 24px; color: #222; }}
        h1 {{ margin-bottom: 4px; }}
        .data {{ color: #666; margin-bottom: 20px; }}
        .box {{ border: 1px solid #ccc; padding: 14px; border-radius: 8px; margin-bottom: 18px; }}
        button {{ padding: 10px 16px; font-size: 15px; cursor: pointer; margin-bottom: 20px; }}
        @media print {{ button {{ display: none; }} }}
      </style>
    </head>
    <body>
      <button onclick="window.print()">🖨️ Stampa / Salva PDF</button>
      <h1>Report Spese Barca</h1>
      <div class="data">Data report: {date.today()}</div>
      <div class="box">
        <b>Riepilogo totali</b><br>
        Spese reali totali: <b>{totale_spese_reali:.2f} €</b><br>
        Somme previste: <b>{totale_previste_attivo:.2f} €</b><br>
        Totale complessivo: <b>{totale_spese_reali + totale_previste_attivo:.2f} €</b><br><br>
        Bilancio {io}: <b>{saldi[io]:.2f} €</b><br>
        Bilancio {socio}: <b>{saldi[socio]:.2f} €</b><br>
        {f"<p><b>Regolamento conti:</b> {testo_regolamento}</p>" if testo_regolamento else ""}
      </div>
      <div class="box">
        <b>Somme previste</b>
        <ul>{righe_previste}</ul>
      </div>
      <div class="box">
        <b>Movimenti reali</b>
        <ul>{righe_movimenti}</ul>
      </div>
    </body>
    </html>
    """

    st.download_button(
        label="🖨️ Scarica Report Stampa / PDF",
        data=html_report.encode("utf-8"),
        file_name=f"report_spese_barca_{date.today()}.html",
        mime="text/html"
    )
