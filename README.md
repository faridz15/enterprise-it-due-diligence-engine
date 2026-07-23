# 📡 Automated IT Due Diligence & M&A Risk Assessment Platform

> An enterprise-grade, automated infrastructure audit engine designed to ingest unstructured legal contracts (PDFs) and cross-reference them against massive tabular hardware/software inventories to uncover critical operational risks and financial leaks prior to corporate mergers.

---

## 🚀 Project Overview
During M&A (Mergers & Acquisitions) technical due diligence, target companies often present unstructured data silos—ranging from messy CSV inventories to static PDF Service Level Agreements (SLAs). Manually cross-checking hundreds of network nodes against vendor maintenance contracts is error-prone and time-consuming.

This platform automates the entire pipeline: it ingests raw inventories, parses legal PDF contracts via Regex/PDFPlumber, applies strict Object-Oriented Business Rules, and renders an executive-level **Network Operations Center (NOC) Dashboard** built with Streamlit and Plotly.

---

## 🧩 Architectural Design (Domain-Driven Design)
Unlike basic script-based projects, this engine is structured using a clean, scalable **Object-Oriented Programming (OOP)** and **Separation of Concerns (SoC)** architecture:

```text
it_dd_bot/
├── data/
│   ├── contracts/        # Unstructured Vendor SLA PDFs
│   ├── raw/              # Raw Hardware Inventory & Software Licenses
│   └── processed/        # Cleaned Excel Reports & Findings
├── src/
│   ├── models/           # Domain Entities (HardwareAsset, VendorContract)
│   ├── parsers/          # Data Ingestion Layer (PDF & Tabular Parsers)
│   ├── rules/            # Business Rule Engine (SLA Compliance & EOL logic)
│   ├── services/         # Orchestration Layer (AuditOrchestrator)
│   ├── config.py         # System Paths & Configurations
│   └── generator.py      # Synthetic Data & PDF Generator Engine
├── .streamlit/           # Enterprise NOC Dark Theme Configuration
├── dashboard.py          # Executive Streamlit Web Interface
└── requirements.txt      # Project Dependencies

✨ Key Features
Automated PDF Contract Ingestion: Extracts critical metadata (Vendor Name, SLA Uptime, Validity Period) from unstructured Master Service Agreements.

Cross-Relational Risk Engine: Automatically detects "Orphaned Infrastructure"—identifying active enterprise nodes (such as 5G Core servers, LoRaWAN gateways, and Edge units) that lack valid vendor SLA protection.

Software Waste Detection: Flags unassigned, redundant, or expired software licenses to prevent financial leakage.

Enterprise NOC UI: Features a high-contrast Dark Mode layout optimized for executive command centers and technical audits.

🛠️ Tech Stack
Language: Python 3.10+

Data Engineering: Pandas, OpenPyXL

PDF Processing: PDFPlumber, FPDF

Visualization: Plotly Express

Web Framework: Streamlit (Wide NOC Layout)

Design Pattern: Domain-Driven Design (OOP)