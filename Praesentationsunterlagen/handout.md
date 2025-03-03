# DevSecOps: Systematische Integration sicherheitsrelevanter Aspekte in kontinuierliche Softwareentwicklungsprozesse

## Handout zur Präsentation

### 1. Grundlagen von DevSecOps

- **Integration von Sicherheit** in den gesamten Entwicklungszyklus
- **Erweiterung des DevOps-Ansatzes** um Security
- **Sicherheit als gemeinsame Verantwortung**
- **Frühzeitige Identifizierung** von Schwachstellen

- **Traditioneller Ansatz vs. DevSecOps**:
  - Traditionell: Sicherheit als Zusatzprüfung am Ende ("Security as Gatekeeper")
  - DevSecOps: Sicherheit als integraler Bestandteil ("Security as Enabler")
- **Wirtschaftliche Bedeutung**:
  - 60x höhere Kosten für Sicherheitsprobleme, die erst in der Produktionsphase entdeckt werden
  - Quelle: IBM Security, "Cost of a Data Breach Report", 2021

### 2. Shift-Left und Shift-Right Security

- **Shift-Left**: Sicherheit in frühen Phasen integrieren
  - **Präventiver Ansatz**: Reduziert Kosten und Zeit für Fehlerbehebung
  - **Fokus**: Planung, Entwicklung, Build
  - **Techniken**:
    - Threat Modeling: Systematische Bedrohungsanalyse
    - SAST: Statische Code-Analyse
    - SCA: Analyse von Abhängigkeiten
    - Pre-Commit Hooks: Automatisierte Prüfungen
    - IaC-Scanning: Infrastruktur-Code-Analyse
  
- **Shift-Right**: Sicherheit in späteren Phasen integrieren
  - **Reaktiver und überwachender Ansatz**: Erkennt Probleme in realen Umgebungen
  - **Fokus**: Deployment, Betrieb, Monitoring
  - **Techniken**:
    - DAST: Dynamische Anwendungstests
    - RASP: Laufzeitschutz für Anwendungen
    - Anomalieerkennung: Erkennung ungewöhnlicher Muster
    - Chaos Engineering: Gezielte Resilienz-Tests
    - Security Monitoring: Kontinuierliche Überwachung

> **Wichtig**: Beide Ansätze ergänzen sich und bilden einen vollständigen Sicherheitskreislauf über den gesamten Lebenszyklus der Anwendung.

### 3. Security in der CI/CD-Pipeline

- **Integration nach dem 'Defense in Depth'-Prinzip**
- **Automatisierte Sicherheitstests** in jeder Phase
- **Beispiel einer Pipeline-Konfiguration**:
```yaml
stages:
  - build
  - security
  - test
  - deploy

security_scan:
  stage: security
  script:
    - run-sast-scan
    - check-dependencies
    - scan-container
```

- **Wichtige Komponenten**:
  - SAST/SCA für Code und Abhängigkeiten
  - Container-Scanning für Images
  - DAST für Laufzeitverhalten
  - IaC-Scanning für Infrastruktur

### 4. Fallstudien

- **Netflix - DevSecOps in der Cloud**: 
  - Vorreiter bei Cloud-nativen DevSecOps-Praktiken
  - Open-Source-Sicherheitstools:
    - Security Monkey: Überwacht AWS-Konfigurationen
    - Repokid: Automatisiert IAM-Berechtigungen
    - Chaos Monkey: Testet Infrastruktur-Resilienz
  - Sicherheitsphilosophie:
    - "Security is Everyone's Job"
    - "Freedom and Responsibility"
    - "Context over Control"
  - Ergebnisse:
    - 90% Reduzierung der Zeit für Sicherheitsbehebungen
    - 72% reduzierte Kosten für Sicherheitsvorfälle
    - 35% höhere Entwicklerproduktivität

- **Capital One - DevSecOps nach Sicherheitsvorfall**:
  - Verstärkte DevSecOps-Praktiken nach Datenschutzvorfall 2019
  - Ursache: Server Side Request Forgery (SSRF) in WAF-Konfiguration
  - 106 Millionen betroffene Kundendatensätze
  - Implementierte Maßnahmen:
    - Cloud Custodian Framework
    - Cloud Security Posture Management
    - Infrastructure as Code mit Sicherheitsprüfungen
    - Identity & Access Management-Überarbeitung
  - Ergebnisse:
    - 70% Reduzierung der Sicherheitslücken
    - 98,5% Reduzierung kritischer Fehlkonfigurationen
    - MTTR von 7 Tagen auf 8 Stunden reduziert

### 5. Kulturelle Transformation

- **Security Champions Modell**:
  - Entwickler mit Sicherheitsexpertise
  - 10-15% ihrer Zeit für Sicherheitsthemen
  - Multiplikatoren im Team
  - Verbindung zum zentralen Sicherheitsteam

- **Kontinuierliche Lernkultur**:
  - Regelmäßige Sicherheitsschulungen
  - Capture-the-Flag-Events
  - Bug Bounty Programme
  - Lunch-and-Learn-Sessions

- **Herausforderung**: 70% der DevSecOps-Initiativen scheitern an kulturellen Herausforderungen, nicht an technischen Problemen (Quelle: Gartner)

### 6. Herausforderungen und Lösungen

- **Herausforderungen**:
  - Integration ohne Beeinträchtigung der Geschwindigkeit
    - Sicherheitstests können CI/CD-Pipelines um 30-200% verlangsamen
  - Komplexität bei Microservices-Architekturen
  - Umgang mit Legacy-Systemen
  - Kulturelle Widerstände und Skill-Gaps

- **Lösungsansätze**:
  - Schrittweise Einführung in Phasen
  - Fokus auf Quick Wins
  - Security Champions in jedem Team
  - Automatisierung maximieren
  - Kontinuierliche Schulung

- **ROI**: 180% durchschnittlicher ROI von DevSecOps-Implementierungen über drei Jahre (Quelle: Forrester Research)

### 7. Empfehlungen für erfolgreiche Implementation

- **Schrittweise Einführung**:
  1. Assessment (2-4 Wochen)
  2. Pilotprojekt (1-3 Monate)
  3. Skalierung (6-12 Monate)
  4. Optimierung (kontinuierlich)

- **Vermeiden Sie diese Fehler**:
  - Zu viel auf einmal implementieren
  - Mangelnde Entwicklerbeteiligung
  - Unklare Verantwortlichkeiten
  - Ignorieren der Unternehmenskultur

### 8. DevSecOps-Tools Übersicht

- **Shift-Left Tools**:
  - SAST: SonarQube, Checkmarx, Semgrep
  - SCA: OWASP Dependency-Check, Snyk, WhiteSource
  - Secret Detection: GitGuardian, TruffleHog
  - IaC-Scanning: Terraform-Scanner, CloudFormation-Linter, Checkov
  - Threat Modeling: STRIDE-Framework, Microsoft Threat Modeling Tool

- **Shift-Right Tools**:
  - DAST: OWASP ZAP, Burp Suite
  - RASP: Contrast Security, Signal Sciences
  - Container-Scanning: Trivy, Clair, Docker Scout
  - Security Monitoring: Splunk, ELK Stack, Datadog
  - Chaos Engineering: Netflix Chaos Monkey, Gremlin

- **CI/CD-Integration**:
  - Pipeline-Tools: GitLab CI/CD, GitHub Actions, Jenkins
  - Automatisierung: Ansible, Puppet, Chef
  - Compliance-Prüfung: Open Policy Agent, HashiCorp Sentinel

- **Cloud Security**:
  - CSPM: Cloud Custodian, AWS Config
  - IAM-Management: Repokid, AWS IAM Analyzer
  - Konfigurationsüberwachung: Security Monkey, CloudMapper

---

## Diskussionsfragen

1. Welche Herausforderungen sehen Sie bei der Implementierung von DevSecOps in Ihrem Umfeld?
2. Was ist Ihre wichtigste Erkenntnis aus dieser Präsentation?

---

## Weiterführende Ressourcen

- OWASP DevSecOps Guideline: [https://owasp.org/www-project-devsecops-guideline/](https://owasp.org/www-project-devsecops-guideline/)
- DevSecOps Community: [https://www.devsecops.org/](https://www.devsecops.org/)
- GitHub-Repository mit Beispiel-Pipelines
- Atlassian DevSecOps-Tools: [https://www.atlassian.com/de/devops/devops-tools/devsecops-tools](https://www.atlassian.com/de/devops/devops-tools/devsecops-tools)
- IBM Security Report: [https://www.ibm.com/security/data-breach](https://www.ibm.com/security/data-breach)

---

*Dieses Handout ergänzt die Präsentation "DevSecOps: Integration sicherheitsrelevanter Aspekte in Softwareentwicklungsprozesse" und dient als Referenz für die wichtigsten Konzepte und Tools.* 