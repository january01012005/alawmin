# A-LAW-min: Local Legal Informatics Engine & Grounding Verification System

> **A-LAW-min** is a statutory legal informatics and retrieval-augmented verification engine tailored for Local Government Unit (LGU) ordinances in the Philippines, initially benchmarked on the **Code of Ordinances of Davao City 2009**.

This repository serves as the official project workspace and **Python Lo-Fi Prototype** for the thesis deliverables **C1, C2, C3, C4, and C5**, designed for team collaboration and evaluation.

---

## 🏛️ Project Overview & Deliverables Alignment

| Deliverable | Figure | Component Name | Description & Prototype Implementation |
| :--- | :--- | :--- | :--- |
| **C1** | **Figure 1** | **Proposed System Architecture** | Dual-stage pipeline linking OCR triage, hierarchical parsing, retrieval, and independent per-detail support verification. |
| **C2** | **Figure 2** | **Primary User Interface** | Citizen conversational query field supporting multi-dialect inquiries (Bisaya/Cebuano, Filipino/Tagalog, English), retrieval progress indicators, verified statutory answers, citation badges, and direct source-inspection controls. |
| **C3** | **Figure 3** | **Secondary User Interface** | Granular support-list audit per answer detail combined with an interactive split-screen/viewer that renders original PDF pages from `Davao_code-of-ordinances.pdf` with yellow highlighted bounding boxes. Enforces strict source-access error handling without silent substitution. |
| **C4** | **Figure 4** | **Main Answer-Support Flow** | Strict 6-point verification decision logic executed independently for each answer claim before release. |
| **C5** | **Figure 5** | **Document Preparation Pipeline** | End-to-end ingestion pipeline: deskewing, noise stripping, hierarchical tagging, and source page indexing. |

---

## 🚀 Quickstart: Running the Python Lo-Fi Prototype

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Clone the Repository
```bash
git clone https://github.com/january01012005/alawmin.git
cd alawmin
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Interactive Web Application
```bash
streamlit run app.py
```
The prototype will open automatically in your browser at `http://localhost:8501`.

---

## 🔍 Key Interactive Features & Scenarios

1. **Multi-Dialect Citizen Inquiries (Deliverable C2)**:
   - **Solid Waste & Anti-Littering**: *"Pila man ang multa kung magpataka og labay og basura sa Davao City?"* (Grounds against Chapter I, Article M, Section 58, Page 77).
   - **Anti-Smoking Regulations**: *"Pwede ba manigarilyo sa sulod sa PUJ o jeep diri sa Davao?"* (Grounds against Chapter I, Article N, Section 62, Page 78).
   - **Firecracker Ban Penalties**: *"Gidili ba gyud ang pagpabuto og firecrackers bisan holiday o New Year sa Davao City?"* (Grounds against Chapter III, Article C, Section 18-19, Page 64-65).
   - **Liquor Ban & Minor Sales**: *"Unsa ang balaod sa pagbaligya og ilimnong makahubog sa mga menor de edad sa Davao?"* (Grounds against Chapter III, Article A, Section 3(c), Page 56).
   - **Negative Grounding Guardrail**: Test out-of-scope queries (e.g. DFA passport renewal). Demonstrates A-LAW-min's strict policy: reporting unverified status rather than hallucinating legal advice.

2. **Synchronized Source-Inspection PDF Viewer (Deliverable C3)**:
   - Directly resolves citations to the authentic 242-page `Davao_code-of-ordinances.pdf`.
   - Uses PyMuPDF to render dynamic, high-resolution document pages with highlighted statutory clauses.
   - **Integrity Safeguard Toggle**: Simulate source file unavailability in the sidebar to observe the mandated `SEC-404-UNAVAILABLE` error state and suspended authorization.

3. **System Blueprint Showcase (C1, C4, C5)**:
   - High-resolution architecture and flowchart visual specifications accessible directly within the application.

4. **Corpus Explorer**:
   - Full-text search and page preview across all 242 pages of the Davao City Code of Ordinances.

---

## 📁 Repository Structure

```
alawmin/
├── app.py                             # Interactive Streamlit Lo-Fi Prototype
├── ordinance_engine.py                # Dataset parsing, retrieval, and PDF annotation engine
├── requirements.txt                   # Python package dependencies
├── README.md                          # Project documentation
├── .gitignore                         # Git ignore configuration
├── Davao_code-of-ordinances.pdf       # Initial dataset: Official 242-page Code of Ordinances (2009)
├── Figure 1 Proposed System Architecture.png # System Architecture specification
├── Figure 4 Flowchart.png             # Main Answer-Support Flowchart
├── Figure 5 Flowchart.png             # Document Preparation Pipeline Flowchart
├── Prior_Art_Matrix_Deliverables.docx # System Deliverables and specifications document
├── screenshot.png                     # Deliverable specifications reference
└── figures/                           # High-res SVG and exported assets
```

---

## 👥 Authors & Team
- **Thesis Research Team:** BSCS-4
- **Repository:** [january01012005/alawmin](https://github.com/january01012005/alawmin)
