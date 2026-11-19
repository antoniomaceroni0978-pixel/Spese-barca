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
            "Importo (€)": round(float(r.get("Importo", 0.0)), 2),
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
            "Importo Previsto (€)": round(float(r.get("Importo Previsto", 0.0)), 2)
        })
df_previste_out = pd.DataFrame(voci_previste) if voci_previste else pd.DataFrame(
    columns=["Descrizione", "Categoria", "Stato", "Importo Previsto (€)"]
)

with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
    riepilogo_dati.to_excel(writer, sheet_name="Riepilogo", index=False)
    df_out.to_excel(writer, sheet_name="Tutti i Movimenti", index=False)
    df_spese_out.to_excel(writer, sheet_name="Solo Spese", index=False)
    df_previste_out.to_excel(writer, sheet_name="Somme Previste", index=False)
