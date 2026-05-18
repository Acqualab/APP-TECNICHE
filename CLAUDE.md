# Contesto progetto – Acqualab APP-TECNICHE

## Repository
- **URL**: https://github.com/Acqualab/APP-TECNICHE
- **Branch principale**: `main`
- **File principale**: `portata_calcolo.html`

## Chi siamo
Acqualab – azienda italiana nel settore idraulico/impiantistico.
Il referente si chiama **Marco** (marcopagnini64@gmail.com).

## App: Calcolo Portata Istantanea – UNI 9182:2010
Applicazione HTML/CSS/JS **single-file** (nessun framework, nessuna dipendenza esterna) per il calcolo della portata istantanea di impianti idrici secondo la norma UNI 9182:2010.

### Struttura dell'app
L'app è organizzata in **3 schede (tab)**:
1. **Parametri** (`tab-parametri`) – tipo edificio, DN tubazione, n° utenti, consumo giornaliero, tempo di ritenzione
2. **Apparecchi** (`tab-apparecchi`) – tabella con 14 apparecchi sanitari, quantità e attivazione
3. **Risultati** (`tab-risultati`) – portata Qi, curva UC, grafici, dati accumulo

### Variabili e funzioni chiave
- `APPARECCHI[]` – array con tutti gli apparecchi (nome, ucAf, ucAcs, n, on)
- `CURVE{}` – curve UNI 9182:2010 Prospetto 3 (punti [ΣUC, Qi l/s]) per condizioni: `cond` (condominio), `ric` (ricircolo), `senza` (senza ricircolo)
- `calcola()` – ricalcola portata e aggiorna i risultati
- `renderTable()` – ridisegna la tabella apparecchi
- `onTipoChange()` – aggiorna i campi visibili in base al tipo edificio
- `showTab(id)` – mostra la scheda selezionata
- `resetTutto()` – azzera tutti i campi all'apertura pagina
- `salvaProgetto()` – scarica JSON con lo stato completo
- `caricaProgetto(input)` – carica JSON e ripristina lo stato

### Campi header
- `inp-cliente` – nome cliente (testo)
- `inp-data` – data (date)
- `inp-offerta` – n° offerta (testo)

### Campi scheda Parametri
- `sel-tipo` – tipo edificio: `res` / `cond` / `alb` / `osp`
- `inp-appart` – n° appartamenti (solo per tipo `cond`)
- `inp-utenti` – n° utenti
- `inp-consumo` – consumo giornaliero (l/p/g, default 150)
- `sel-dn` – diametro nominale: 12/15/20/25/32/40/50/63 mm (default 25)
- `inp-trit` – tempo di ritenzione minimo (min, default 45)
- `sel-cond` – condizioni impianto: `ric` / `senza`

### Apparecchi (14 totali, in ordine)
0. Lavabo (n:1, on:true)
1. Lavello cucina (n:1, on:true)
2. WC a cassetta (n:1, on:true)
3. WC a flussometro (n:0, on:false)
4. Vasca da bagno (n:1, on:true)
5. Doccia (n:1, on:true)
6. Bidet (n:1, on:true)
7. Lavatrice (n:1, on:true)
8. Lavastoviglie (n:1, on:true)
9. Lavatoio / lavandino (n:0, on:false)
10. Rubinetto esterno DN 15 (n:1, on:true)
11. Idrante antincendio DN 45 (n:0, on:false)
12. Abbeveratoio / stalla (n:0, on:false)
13. Fontanella (n:0, on:false)

## Stile e design
- Colori definiti in CSS variables `:root` (no hardcoded colors)
- Font: `Segoe UI`, system-ui, sans-serif
- Tema chiaro con accenti blu (`--blue:#185FA5`), verde (`--green:#3B6D11`), corallo (`--coral:#993C1D`)
- Bottoni header: classe `print-btn`
- Cards: classe `card` o `card-flush`
- Badge norma: classe `norm-badge`

## Flusso di lavoro con Claude (claude.ai chat)
1. Marco descrive la modifica da fare
2. Claude modifica il file e lo consegna come download
3. Marco fa `git push` dal terminale Git CMD:
   ```
   cd C:\Users\Ufficio\APP-TECNICHE
   git pull
   # copia il file scaricato nella cartella
   git add portata_calcolo.html
   git commit -m "descrizione modifica"
   git push
   ```

## Note importanti
- Il file si chiama `portata_calcolo.html` nel repo GitHub, ma `PORTATA-CALCOLO.html` nei download di Claude
- È un file **single-file**: tutto CSS, HTML e JS in un unico file, nessuna dipendenza esterna
- Versione attuale: include bottoni Salva/Carica progetto JSON e reset campi all'apertura
- NON usare localStorage (non supportato negli artifact Claude)
- La rete della sandbox Claude non raggiunge api.github.com, quindi il push diretto non è possibile da questa chat
