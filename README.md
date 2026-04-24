# Dashboard für Studienfortschritt

Ein Dashboard zur Verwaltung eines Studiums.  
Es ermöglicht das Starten, Verwalten und Abschließen von Modulen sowie die Anzeige relevanter Kennzahlen und Fortschritt auf Basis der abgeschlossenen Module.

---

## Funktionen

- Starten und Löschen von Modulen
- Abschluss von Modulen inkl. Prüfungsleistung
- Anzeige von:
  - offenen Modulen
  - Modulen in Bearbeitung
  - abgeschlossenen Modulen
- Dashboard-Metriken:
  - Notendurchschnitt
  - Studienfortschritt (auf Basis der ECTS)
  - voraussichtliches Enddatum
  - durchschnittliche ECTS pro Semester

---
## Installation und Start

#### 1. Repository klonen
```bash
git clone https://github.com/HoffmannEduard/iu_dashboard.git
cd iu_dashboard
```

#### 2. Virtuelle Umgebung erstellen
```bash
python -m venv .venv
```

#### 3. Virtuelle Umgebung aktivieren  
Windows (cmd):  
```bash
.venv\Scripts\activate
```

Windows (PowerShell)  
```bash
.venv\Scripts\Activate.ps1
```

macOS / Linus  
```bash
source .venv\bin\activate
```

#### 4. Abhängigkeiten installieren  
```bash
pip install -r requirements.txt
```

#### 5. Anwendung starten  
```bash
streamlit run app.py
```

## Datenbank  

Die Anwendung verwendet eine **In-Memory SQLite-Datenbank**, dadurch sind Daten nur während der Laufzeit verfügbar:
```python
sqlite3.connect(":memory:", check_same_thread=False)
```

Für eine persistente Speicherung, kann `:memory:` durch `dashboard.db` ersetzt werden:
```python
sqlite3.connect("dashboard.db", check_same_thread=False)
```

## Voraussetzungen  
- Python 3
- pip