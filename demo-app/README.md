# DevSecOps Demo App

Diese einfache Flask-Anwendung wurde für Demonstrationszwecke im Rahmen einer DevSecOps-Präsentation erstellt. Sie enthält **absichtlich Sicherheitslücken**, um die Funktionsweise von Sicherheitstools in einer DevSecOps-Pipeline zu demonstrieren.

## Warnung

**Diese Anwendung ist NICHT für den produktiven Einsatz geeignet!** Sie enthält zahlreiche Sicherheitslücken, die zu Datenverlust, unbefugtem Zugriff und anderen Sicherheitsproblemen führen können.

## Enthaltene Sicherheitslücken

Die Anwendung enthält absichtlich folgende Sicherheitslücken:

1. **SQL-Injection**: Unsichere Datenbankabfragen
2. **Hartcodierte Credentials**: Passwörter und API-Schlüssel im Quellcode
3. **Veraltete Abhängigkeiten**: Bekannte Sicherheitslücken in den verwendeten Bibliotheken
4. **Unsichere Passwort-Speicherung**: Verwendung von MD5 ohne Salting
5. **Path Traversal**: Unsichere Dateioperationen
6. **Fehlende Sitzungsverwaltung**: Keine ordnungsgemäße Authentifizierung
7. **Debug-Modus in Produktion**: Offenlegung sensibler Informationen

## Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/devsecops-demo.git
cd devsecops-demo

# Virtuelle Umgebung erstellen und aktivieren
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
python app.py
```

Die Anwendung ist dann unter http://localhost:5000 erreichbar.

## DevSecOps-Pipeline

Diese Anwendung wird in der Präsentation verwendet, um eine DevSecOps-Pipeline mit folgenden Komponenten zu demonstrieren:

1. **SAST (Static Application Security Testing)**: Semgrep
2. **SCA (Software Composition Analysis)**: Safety
3. **Container-Scanning**: Trivy
4. **Secret-Scanning**: TruffleHog

Die Pipeline-Konfiguration befindet sich in der Datei `.github/workflows/demo-pipeline.yml`.

## Behebung der Sicherheitslücken

Im Rahmen der Präsentation werden die Sicherheitslücken identifiziert und behoben. Die korrigierten Versionen der Dateien finden Sie im Branch `secure`.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die LICENSE-Datei für Details. 