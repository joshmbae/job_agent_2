# Job Application Agent

Dieses Projekt stellt einen einfachen Agenten bereit, der Stellenanzeigen anhand von Schlagwörtern filtert, Bewerbungen automatisch "einreicht" und alle Bewerbungen in einer CSV-Datei protokolliert. Die tatsächliche Übermittlung (z. B. via E-Mail oder API) ist als Erweiterung vorgesehen und kann an der zentralen Stelle im Code ergänzt werden.

## Installation

Es werden keine zusätzlichen Abhängigkeiten benötigt. Die bereitgestellten Beispiele verwenden Python 3.11.

## Vorbereitung der Daten

Die Beispiel-Quelle `data/jobs.json` enthält Einträge mit folgendem Schema:

```json
{
  "company": "TechCorp",
  "title": "Python Backend Engineer",
  "description": "Kurzbeschreibung der Aufgaben und Anforderungen",
  "url": "https://example.com/jobs/123"
}
```

Weitere Datenquellen (z. B. REST-APIs) können über eigene Implementierungen der Schnittstelle `JobSource` ergänzt werden.

## Verwendung

1. Stellenanzeigen im JSON-Format bereitstellen (siehe `data/jobs.json`).
2. Folgenden Befehl ausführen:

```bash
python main.py "python backend" --name "Max Mustermann" --email "max@example.com" --resume "/pfad/zum/lebenslauf.pdf"
```

Weitere Optionen:

- `--jobs`: Pfad zu einer JSON-Datei mit Stellenanzeigen.
- `--log`: Ziel-Datei für das Bewerbungsprotokoll (CSV).
- `--threshold`: Mindestquote der Treffer-Schlagworte (0-1).

Nach Ausführung werden passende Stellen angezeigt und Bewerbungen in der angegebenen CSV-Datei dokumentiert. Die Datei kann anschließend zur Nachverfolgung der Bewerbungen genutzt werden.
