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

with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
    riepilogo_dati.to_excel(writer, sheet_name="Riepilogo", index=False)
    df_out.to_excel(writer, sheet_name="Tutti i Movimenti", index=False)
    df_spese_out.to_excel(writer, sheet_name="Solo Spese", index=False)
    df_previste_out.to_excel(writer, sheet_name="Somme Previste", index=False)
