<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>⛵ Gestione Spese Barca</title>
  <style>
    :root {
      --bg: #f4f7fb;
      --card: #ffffff;
      --primary: #0f4c81;
      --primary-light: #e6f0fa;
      --accent: #1b8a5a;
      --danger: #c0392b;
      --text: #1f2937;
      --muted: #6b7280;
      --border: #dce3ec;
    }
    * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body { margin: 0; background: var(--bg); color: var(--text); padding: 14px; }
    .container { max-width: 820px; margin: 0 auto; }
    h1 { font-size: 1.5rem; margin: 0 0 4px; color: var(--primary); }
    h2 { font-size: 1.15rem; margin: 0 0 12px; color: var(--primary); }
    p.sub { margin: 0 0 16px; color: var(--muted); font-size: 0.92rem; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
    @media (max-width: 640px) {
      .grid-3, .grid-2 { grid-template-columns: 1fr; }
    }
    .metric { background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: 12px; }
    .metric .label { font-size: 0.8rem; color: var(--muted); }
    .metric .val { font-size: 1.25rem; font-weight: 700; margin-top: 4px; }
    .banner { background: var(--primary-light); border-left: 4px solid var(--primary); padding: 12px; border-radius: 8px; margin-top: 12px; font-weight: 600; }
    .tabs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
    .tab-btn { padding: 9px 14px; border: 1px solid var(--border); background: #fff; border-radius: 8px; cursor: pointer; font-weight: 600; color: var(--text); }
    .tab-btn.active { background: var(--primary); color: #fff; border-color: var(--primary); }
    label { display: block; font-size: 0.85rem; font-weight: 600; margin: 10px 0 4px; }
    input, select { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; font-size: 0.95rem; background: #fff; }
    .checkbox-row { display: flex; gap: 14px; align-items: center; margin-top: 6px; }
    .checkbox-row label { display: flex; align-items: center; gap: 6px; margin: 0; font-weight: 500; cursor: pointer; }
    .checkbox-row input { width: auto; }
    .btn { display: inline-block; padding: 10px 16px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.95rem; margin-top: 12px; }
    .btn-primary { background: var(--primary); color: #fff; }
    .btn-accent { background: var(--accent); color: #fff; }
    .btn-outline { background: #fff; color: var(--primary); border: 1px solid var(--primary); }
    .btn-danger { background: #fdecea; color: var(--danger); padding: 5px 9px; font-size: 0.8rem; margin-top: 0; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.88rem; }
    th, td { text-align: left; padding: 8px; border-bottom: 1px solid var(--border); }
    th { background: var(--bg); color: var(--muted); font-weight: 600; }
    .table-wrap { overflow-x: auto; }
    .hidden { display: none !important; }
    .print-only { display: none; }

    @media print {
      body { background: #fff; padding: 0; }
      .no-print { display: none !important; }
      .print-only { display: block !important; }
      .card { border: 1px solid #ccc; box-shadow: none; break-inside: avoid; }
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- BLOCCO ACCESSO -->
    <div id="login-box" class="card no-print">
      <h2>🔒 Accesso Riservato</h2>
      <p class="sub">Inserisci la password per accedere alla gestione spese della barca.</p>
      <label for="pwd-input">Password</label>
      <input type="password" id="pwd-input" placeholder="Password..." onkeydown="if(event.key==='Enter') verificaLogin()" />
      <button class="btn btn-primary" onclick="verificaLogin()">Entra</button>
      <p id="login-err" style="color: var(--danger); font-size: 0.85rem; margin-top: 8px;"></p>
    </div>

    <!-- APP PRINCIPALE -->
    <div id="app-main" class="hidden">
      <div class="card">
        <h1>⛵ Gestione Spese Barca</h1>
        <p class="sub no-print">Salvataggio automatico attivo su questo dispositivo • Soci: <b>Antonio</b> e <b>Tonino</b></p>
        <p class="print-only">Report Spese Barca — Data: <span id="print-date"></span></p>

        <div class="grid-3">
          <div class="metric">
            <div class="label">Spese Reali Totali</div>
            <div class="val" id="m-spese">0.00 €</div>
          </div>
          <div class="metric">
            <div class="label">Somme Previste (Attive)</div>
            <div class="val" id="m-previste">0.00 €</div>
          </div>
          <div class="metric">
            <div class="label">Totale Complessivo</div>
            <div class="val" id="m-totale">0.00 €</div>
          </div>
        </div>

        <div class="grid-2" style="margin-top: 10px;">
          <div class="metric">
            <div class="label">Bilancio Finale Antonio</div>
            <div class="val" id="m-bal-antonio">0.00 €</div>
          </div>
          <div class="metric">
            <div class="label">Bilancio Finale Tonino</div>
            <div class="val" id="m-bal-tonino">0.00 €</div>
          </div>
        </div>

        <div id="regolamento-box" class="banner hidden"></div>
      </div>

      <!-- MODULI DI INSERIMENTO (NASCOSTI IN STAMPA) -->
      <div class="card no-print">
        <div class="tabs">
          <button class="tab-btn active" onclick="mostraTab('tab-op', this)">➕ Operazione Reale</button>
          <button class="tab-btn" onclick="mostraTab('tab-prev', this)">📌 Somme Previste</button>
          <button class="tab-btn" onclick="mostraTab('tab-note', this)">🛠️ Note Operative (Private)</button>
        </div>

        <!-- TAB 1: OPERAZIONE REALE -->
        <div id="tab-op">
          <div class="grid-2">
            <div>
              <label>Tipo operazione</label>
              <select id="op-tipo" onchange="aggiornaCampiTipo()">
                <option value="Spesa">Spesa</option>
                <option value="Entrata">Entrata</option>
                <option value="Rimborso">Rimborso tra soci</option>
              </select>
            </div>
            <div>
              <label>Data</label>
              <input type="date" id="op-data" />
            </div>
          </div>

          <div class="grid-2">
            <div>
              <label>Importo (€)</label>
              <input type="number" id="op-importo" step="0.01" min="0" placeholder="0.00" />
            </div>
            <div id="wrap-categoria">
              <label>Categoria</label>
              <select id="op-categoria">
                <option>Carburante</option>
                <option>Ormeggio</option>
                <option>Manutenzione Ordinaria</option>
                <option>Manutenzione Straordinaria</option>
                <option>Assicurazione</option>
                <option>Altro</option>
              </select>
            </div>
          </div>

          <div id="wrap-desc">
            <label>Descrizione</label>
            <input type="text" id="op-desc" placeholder="Es. Rifornimento gasolio" />
          </div>

          <div class="grid-2" id="wrap-pagato">
            <div>
              <label id="lbl-pagato">Pagato da chi?</label>
              <select id="op-pagato">
                <option value="Antonio">Antonio</option>
                <option value="Tonino">Tonino</option>
              </select>
            </div>
            <div id="wrap-coinvolti">
              <label>Diviso tra</label>
              <div class="checkbox-row">
                <label><input type="checkbox" id="chk-antonio" checked /> Antonio</label>
                <label><input type="checkbox" id="chk-tonino" checked /> Tonino</label>
              </div>
            </div>
          </div>

          <button class="btn btn-primary" onclick="aggiungiOperazione()">Registra Operazione</button>
        </div>

        <!-- TAB 2: SOMME PREVISTE -->
        <div id="tab-prev" class="hidden">
          <div class="grid-2">
            <div>
              <label>Descrizione voce</label>
              <input type="text" id="prev-desc" placeholder="Es. Assicurazione Annuale" />
            </div>
            <div>
              <label>Importo previsto (€)</label>
              <input type="number" id="prev-importo" step="0.01" min="0" placeholder="0.00" />
            </div>
          </div>
          <div class="grid-2">
            <div>
              <label>Categoria</label>
              <select id="prev-cat">
                <option>Assicurazione</option>
                <option>Ormeggio Annuale</option>
                <option>Manutenzione</option>
                <option>Altro</option>
              </select>
            </div>
            <div>
              <label>Stato</label>
              <select id="prev-stato">
                <option value="Attiva">Attiva (includi nei totali)</option>
                <option value="Disattivata">Disattivata</option>
              </select>
            </div>
          </div>
          <button class="btn btn-primary" onclick="aggiungiPrevista()">Aggiungi Somma Prevista</button>
        </div>

        <!-- TAB 3: NOTE OPERATIVE (INCLUSE NEI SALDI, NASCOSTE IN STAMPA PER TONINO) -->
        <div id="tab-note" class="hidden">
          <p class="sub">Le attività registrate qui entrano nei conguagli ma <b>non vengono stampate</b> nel report per Tonino.</p>
          <div class="grid-2">
            <div>
              <label>Data attività</label>
              <input type="date" id="att-data" />
            </div>
            <div>
              <label>Attività / Lavoro</label>
              <input type="text" id="att-desc" placeholder="Es. Lucidatura opera viva" />
            </div>
          </div>
          <div class="grid-2">
            <div>
              <label>Ore impiegate</label>
              <input type="number" id="att-ore" step="0.5" min="0.5" value="2" />
            </div>
            <div>
              <label>Tariffa oraria (€/h)</label>
              <input type="number" id="att-tariffa" step="1" min="0" value="25" />
            </div>
          </div>
          <button class="btn btn-primary" onclick="aggiungiAttivita()">Registra Attività</button>
        </div>
      </div>

      <!-- TABELLA SOMME PREVISTE -->
      <div class="card">
        <h2>📌 Somme Previste</h2>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Descrizione</th>
                <th>Categoria</th>
                <th>Stato</th>
                <th>Importo</th>
                <th class="no-print">Azioni</th>
              </tr>
            </thead>
            <tbody id="tbody-previste"></tbody>
          </table>
        </div>
      </div>

      <!-- TABELLA MOVIMENTI REALI -->
      <div class="card">
        <h2>📜 Storico Movimenti Reali</h2>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Data</th>
                <th>Tipo</th>
                <th>Categoria</th>
                <th>Descrizione</th>
                <th>Pagato Da</th>
                <th>Coinvolti</th>
                <th>Importo</th>
                <th class="no-print">Azioni</th>
              </tr>
            </thead>
            <tbody id="tbody-transazioni"></tbody>
          </table>
        </div>
      </div>

      <!-- TABELLA NOTE OPERATIVE (SEMPRE NASCOSTA IN STAMPA) -->
      <div class="card no-print">
        <h2>🛠️ Note Operative (Riservate Antonio)</h2>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Data</th>
                <th>Attività</th>
                <th>Ore</th>
                <th>Tariffa</th>
                <th>Totale</th>
                <th>Azioni</th>
              </tr>
            </thead>
            <tbody id="tbody-attivita"></tbody>
          </table>
        </div>
      </div>

      <!-- REPORT E BACKUP -->
      <div class="card no-print">
        <h2>🖨️ Report per Tonino & Backup Dati</h2>
        <p class="sub">Puoi stampare o salvare in PDF il riepilogo pulito per Tonino, oppure esportare una copia di sicurezza (.json).</p>
        <button class="btn btn-accent" onclick="stampaReport()">🖨️ Stampa / Salva PDF per Tonino</button>
        <button class="btn btn-outline" onclick="scaricaBackup()">⬇️ Scarica Backup (.json)</button>
        <label class="btn btn-outline" style="cursor:pointer;">
          ⬆️ Carica Backup (.json)
          <input type="file" accept=".json" style="display:none;" onchange="caricaBackup(event)" />
        </label>
      </div>
    </div>
  </div>

  <script>
    // Imposta una password qui (lascia "" se non vuoi richiesta password all'apertura)
    const PASSWORD_APP = "barca2026";
    const STORAGE_KEY = "spese_barca_antonio_tonino_v1";

    let stato = {
      transazioni: [],
      somme_previste: [],
      attivita_ore: []
    };

    function oggiISO() {
      return new Date().toISOString().split("T")[0];
    }

    window.onload = function () {
      document.getElementById("op-data").value = oggiISO();
      document.getElementById("att-data").value = oggiISO();
      caricaDaMemoria();

      if (!PASSWORD_APP || sessionStorage.getItem("barca_auth") === "1") {
        document.getElementById("login-box").classList.add("hidden");
        document.getElementById("app-main").classList.remove("hidden");
        aggiornaVista();
      }
    };

    function verificaLogin() {
      const val = document.getElementById("pwd-input").value;
      if (val === PASSWORD_APP) {
        sessionStorage.setItem("barca_auth", "1");
        document.getElementById("login-box").classList.add("hidden");
        document.getElementById("app-main").classList.remove("hidden");
        aggiornaVista();
      } else {
        document.getElementById("login-err").textContent = "Password non corretta.";
      }
    }

    function salvaInMemoria() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(stato));
    }

    function caricaDaMemoria() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const parsed = JSON.parse(raw);
          stato.transazioni = Array.isArray(parsed.transazioni) ? parsed.transazioni : [];
          stato.somme_previste = Array.isArray(parsed.somme_previste) ? parsed.somme_previste : [];
          stato.attivita_ore = Array.isArray(parsed.attivita_ore) ? parsed.attivita_ore : [];
        }
      } catch (e) {
        console.error("Errore caricamento memoria:", e);
      }
    }

    function mostraTab(idTab, btn) {
      ["tab-op", "tab-prev", "tab-note"].forEach(id => document.getElementById(id).classList.add("hidden"));
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.getElementById(idTab).classList.remove("hidden");
      btn.classList.add("active");
    }

    function aggiornaCampiTipo() {
      const tipo = document.getElementById("op-tipo").value;
      const wrapCat = document.getElementById("wrap-categoria");
      const wrapPagato = document.getElementById("wrap-pagato");
      const wrapCoinvolti = document.getElementById("wrap-coinvolti");
      const lblPagato = document.getElementById("lbl-pagato");

      if (tipo === "Spesa") {
        wrapCat.classList.remove("hidden");
        wrapPagato.classList.remove("hidden");
        wrapCoinvolti.classList.remove("hidden");
        lblPagato.textContent = "Pagato da chi?";
      } else if (tipo === "Entrata") {
        wrapCat.classList.add("hidden");
        wrapPagato.classList.add("hidden");
      } else {
        wrapCat.classList.add("hidden");
        wrapPagato.classList.remove("hidden");
        wrapCoinvolti.classList.add("hidden");
        lblPagato.textContent = "Chi ha fatto il rimborso?";
      }
    }

    function aggiungiOperazione() {
      const tipo = document.getElementById("op-tipo").value;
      const data = document.getElementById("op-data").value || oggiISO();
      const importo = parseFloat(document.getElementById("op-importo").value);
      let desc = document.getElementById("op-desc").value.trim();

      if (isNaN(importo) || importo <= 0) {
        alert("Inserisci un importo maggiore di zero.");
        return;
      }

      let categoria = "";
      let pagatoDa = "";
      let coinvolti = [];

      if (tipo === "Spesa") {
        categoria = document.getElementById("op-categoria").value;
        pagatoDa = document.getElementById("op-pagato").value;
        if (document.getElementById("chk-antonio").checked) coinvolti.push("Antonio");
        if (document.getElementById("chk-tonino").checked) coinvolti.push("Tonino");
        if (coinvolti.length === 0) {
          alert("Seleziona almeno un socio coinvolto nella spesa.");
          return;
        }
      } else if (tipo === "Entrata") {
        categoria = "Entrata Comune";
        pagatoDa = "Cassa Comune";
        coinvolti = ["Antonio", "Tonino"];
      } else {
        categoria = "Rimborso";
        pagatoDa = document.getElementById("op-pagato").value;
        const ricevente = pagatoDa === "Antonio" ? "Tonino" : "Antonio";
        coinvolti = [ricevente];
        if (!desc) desc = `Rimborso da ${pagatoDa} a ${ricevente}`;
      }

      stato.transazioni.push({
        Data: data,
        Tipo: tipo,
        Categoria: categoria,
        Descrizione: desc,
        Importo: importo,
        PagatoDa: pagatoDa,
        Coinvolti: coinvolti.join(", ")
      });

      document.getElementById("op-importo").value = "";
      document.getElementById("op-desc").value = "";
      salvaInMemoria();
      aggiornaVista();
    }

    function aggiungiPrevista() {
      const desc = document.getElementById("prev-desc").value.trim();
      const importo = parseFloat(document.getElementById("prev-importo").value);
      const cat = document.getElementById("prev-cat").value;
      const statoVoce = document.getElementById("prev-stato").value;

      if (!desc || isNaN(importo) || importo <= 0) {
        alert("Inserisci descrizione e importo previsto valido.");
        return;
      }

      stato.somme_previste.push({
        Descrizione: desc,
        ImportoPrevisto: importo,
        Categoria: cat,
        Stato: statoVoce
      });

      document.getElementById("prev-desc").value = "";
      document.getElementById("prev-importo").value = "";
      salvaInMemoria();
      aggiornaVista();
    }

    function aggiungiAttivita() {
      const data = document.getElementById("att-data").value || oggiISO();
      const desc = document.getElementById("att-desc").value.trim();
      const ore = parseFloat(document.getElementById("att-ore").value);
      const tariffa = parseFloat(document.getElementById("att-tariffa").value);

      if (!desc || isNaN(ore) || ore <= 0 || isNaN(tariffa) || tariffa < 0) {
        alert("Compila correttamente tutti i campi dell'attività.");
        return;
      }

      stato.attivita_ore.push({
        Data: data,
        Attivita: desc,
        Ore: ore,
        Tariffa: tariffa,
        Totale: ore * tariffa
      });

      document.getElementById("att-desc").value = "";
      salvaInMemoria();
      aggiornaVista();
    }

    function eliminaRiga(lista, index) {
      if (confirm("Vuoi eliminare questa voce?")) {
        stato[lista].splice(index, 1);
        salvaInMemoria();
        aggiornaVista();
      }
    }

    function toggleStatoPrevista(index) {
      const attuale = stato.somme_previste[index].Stato;
      stato.somme_previste[index].Stato = attuale === "Attiva" ? "Disattivata" : "Attiva";
      salvaInMemoria();
      aggiornaVista();
    }

    function aggiornaVista() {
      let totSpese = 0;
      let totPreviste = 0;
      const saldi = { Antonio: 0, Tonino: 0 };

      stato.transazioni.forEach(r => {
        const imp = Number(r.Importo) || 0;
        if (r.Tipo === "Spesa") {
          totSpese += imp;
          if (saldi[r.PagatoDa] !== undefined) saldi[r.PagatoDa] += imp;
          const part = (r.Coinvolti || "Antonio, Tonino").split(",").map(s => s.trim()).filter(Boolean);
          const quota = part.length > 0 ? imp / part.length : imp;
          part.forEach(p => {
            if (saldi[p] !== undefined) saldi[p] -= quota;
          });
        } else if (r.Tipo === "Rimborso") {
          if (saldi[r.PagatoDa] !== undefined) saldi[r.PagatoDa] += imp;
          const ric = (r.Coinvolti || "").trim();
          if (saldi[ric] !== undefined) saldi[ric] -= imp;
        }
      });

      stato.attivita_ore.forEach(a => {
        const val = Number(a.Totale) || 0;
        saldi.Antonio += val;
        saldi.Antonio -= val / 2;
        saldi.Tonino -= val / 2;
      });

      stato.somme_previste.forEach(p => {
        if (p.Stato === "Attiva") totPreviste += Number(p.ImportoPrevisto) || 0;
      });

      document.getElementById("m-spese").textContent = totSpese.toFixed(2) + " €";
      document.getElementById("m-previste").textContent = totPreviste.toFixed(2) + " €";
      document.getElementById("m-totale").textContent = (totSpese + totPreviste).toFixed(2) + " €";
      document.getElementById("m-bal-antonio").textContent = saldi.Antonio.toFixed(2) + " €";
      document.getElementById("m-bal-tonino").textContent = saldi.Tonino.toFixed(2) + " €";

      const regBox = document.getElementById("regolamento-box");
      const diff = saldi.Antonio - saldi.Tonino;
      if (Math.abs(diff) > 0.05) {
        regBox.classList.remove("hidden");
        if (diff > 0) {
          regBox.textContent = `💡 Regolamento conti: Tonino deve dare ${(diff / 2).toFixed(2)} € a Antonio.`;
        } else {
          regBox.textContent = `💡 Regolamento conti: Antonio deve dare ${(Math.abs(diff) / 2).toFixed(2)} € a Tonino.`;
        }
      } else {
        regBox.classList.add("hidden");
      }

      // Render Somme Previste
      const tbPrev = document.getElementById("tbody-previste");
      tbPrev.innerHTML = stato.somme_previste.length === 0
        ? `<tr><td colspan="5" style="color:var(--muted)">Nessuna somma prevista</td></tr>`
        : stato.somme_previste.map((p, i) => `
          <tr>
            <td>${escapeHtml(p.Descrizione)}</td>
            <td>${escapeHtml(p.Categoria)}</td>
            <td><button class="btn btn-outline" style="margin:0;padding:3px 8px;font-size:0.8rem;" onclick="toggleStatoPrevista(${i})">${escapeHtml(p.Stato)}</button></td>
            <td><b>${Number(p.ImportoPrevisto).toFixed(2)} €</b></td>
            <td class="no-print"><button class="btn btn-danger" onclick="eliminaRiga('somme_previste', ${i})">Elimina</button></td>
          </tr>
        `).join("");

      // Render Transazioni
      const tbTrans = document.getElementById("tbody-transazioni");
      tbTrans.innerHTML = stato.transazioni.length === 0
        ? `<tr><td colspan="8" style="color:var(--muted)">Nessun movimento registrato</td></tr>`
        : stato.transazioni.map((t, i) => `
          <tr>
            <td>${escapeHtml(t.Data)}</td>
            <td>${escapeHtml(t.Tipo)}</td>
            <td>${escapeHtml(t.Categoria)}</td>
            <td>${escapeHtml(t.Descrizione)}</td>
            <td>${escapeHtml(t.PagatoDa)}</td>
            <td>${escapeHtml(t.Coinvolti)}</td>
            <td><b>${Number(t.Importo).toFixed(2)} €</b></td>
            <td class="no-print"><button class="btn btn-danger" onclick="eliminaRiga('transazioni', ${i})">Elimina</button></td>
          </tr>
        `).join("");

      // Render Note Operative
      const tbAtt = document.getElementById("tbody-attivita");
      tbAtt.innerHTML = stato.attivita_ore.length === 0
        ? `<tr><td colspan="6" style="color:var(--muted)">Nessuna attività registrata</td></tr>`
        : stato.attivita_ore.map((a, i) => `
          <tr>
            <td>${escapeHtml(a.Data)}</td>
            <td>${escapeHtml(a.Attivita)}</td>
            <td>${Number(a.Ore).toFixed(1)}</td>
            <td>${Number(a.Tariffa).toFixed(2)} €</td>
            <td><b>${Number(a.Totale).toFixed(2)} €</b></td>
            <td><button class="btn btn-danger" onclick="eliminaRiga('attivita_ore', ${i})">Elimina</button></td>
          </tr>
        `).join("");
    }

    function escapeHtml(str) {
      return String(str || "").replace(/[&<>"']/g, m => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
      }[m]));
    }

    function stampaReport() {
      document.getElementById("print-date").textContent = oggiISO();
      window.print();
    }

    function scaricaBackup() {
      const blob = new Blob([JSON.stringify(stato, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `backup_spese_barca_${oggiISO()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }

    function caricaBackup(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function (e) {
        try {
          const dati = JSON.parse(e.target.result);
          stato.transazioni = Array.isArray(dati.transazioni) ? dati.transazioni : [];
          stato.somme_previste = Array.isArray(dati.somme_previste) ? dati.somme_previste : [];
          stato.attivita_ore = Array.isArray(dati.attivita_ore) ? dati.attivita_ore : [];
          salvaInMemoria();
          aggiornaVista();
          alert("Backup ripristinato con successo!");
        } catch (err) {
          alert("File di backup non valido.");
        }
      };
      reader.readAsText(file);
    }
  </script>
</body>
</html>
