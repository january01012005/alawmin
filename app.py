"""
A-LAW-min: Local Legal Informatics Engine & Grounding Verification System
Lo-Fi Interactive Python Prototype for Deliverables C2 & C3
Focusing on Davao City Code of Ordinances 2009 Ingestion, Multi-Dialect QA,
Statutory Citation Badges, and Synchronized Source-Inspection PDF Viewer.
"""

import os
import time
import streamlit as st
from PIL import Image

from ordinance_engine import (
    engine,
    PRESET_SCENARIOS,
    VERIFICATION_CHECKS,
    SourceAccessError,
    PDF_PATH
)

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="A-LAW-min | Legal Informatics Lo-Fi Prototype",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom CSS Styling (Rethink Sans & Minimalist Lo-Fi Aesthetic)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rethink+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Rethink Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

/* Header styles */
.brand-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}
.brand-subtitle {
    font-size: 0.95rem;
    color: #64748B;
    margin-bottom: 1.2rem;
}

/* Deliverable Badges */
.badge-c2 {
    background-color: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-block;
}
.badge-c3 {
    background-color: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-block;
}

/* Card Styling */
.prototype-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.citation-badge {
    background-color: #F8FAFC;
    border-left: 3px solid #2563EB;
    border: 1px solid #E2E8F0;
    border-left-width: 4px;
    border-left-color: #2563EB;
    padding: 8px 12px;
    margin-top: 6px;
    margin-bottom: 6px;
    font-size: 0.82rem;
    color: #334155;
    border-radius: 4px;
}

.audit-pass {
    background-color: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
}

.error-banner {
    background-color: #FEF2F2;
    border: 2px solid #F87171;
    border-radius: 8px;
    padding: 1.2rem;
    color: #991B1B;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.sidebar-nav-title {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Deliverable C2: Primary UI"

if "selected_scenario_key" not in st.session_state:
    st.session_state.selected_scenario_key = "littering"

if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "ceb"

if "target_pdf_page" not in st.session_state:
    st.session_state.target_pdf_page = 77

if "target_search_terms" not in st.session_state:
    st.session_state.target_search_terms = ["Section 58. Penalty"]

if "simulate_pdf_error" not in st.session_state:
    st.session_state.simulate_pdf_error = False

if "last_query_text" not in st.session_state:
    st.session_state.last_query_text = PRESET_SCENARIOS["littering"]["queries"]["ceb"]

if "retrieval_done" not in st.session_state:
    st.session_state.retrieval_done = True

# -----------------------------------------------------------------------------
# Sidebar Configuration & Prototype Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="brand-title">A-LAW-min ⚖️</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Legal Informatics Engine • Lo-Fi System Prototype</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="sidebar-nav-title">Navigation & Deliverables</div>', unsafe_allow_html=True)
    nav_options = [
        "Deliverable C2: Primary UI",
        "Deliverable C3: Secondary UI",
        "System Architecture & Flowcharts (C1, C4, C5)",
        "Corpus Explorer (Davao Code 2009)"
    ]
    st.session_state.active_nav = st.radio(
        "Select Screen View:",
        nav_options,
        index=nav_options.index(st.session_state.active_nav) if st.session_state.active_nav in nav_options else 0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-nav-title">Dialect / Language</div>', unsafe_allow_html=True)
    lang_labels = {
        "ceb": "Bisaya / Cebuano (Primary)",
        "fil": "Filipino / Tagalog",
        "en": "English (Statutory)"
    }
    st.session_state.selected_lang = st.selectbox(
        "Interface Dialect:",
        options=list(lang_labels.keys()),
        format_func=lambda k: lang_labels[k],
        index=list(lang_labels.keys()).index(st.session_state.selected_lang),
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-nav-title">Dataset Status</div>', unsafe_allow_html=True)
    if os.path.exists(PDF_PATH):
        st.success(f"Loaded: `{os.path.basename(PDF_PATH)}`\n\nTotal Pages: **{engine.get_total_pages()}**")
    else:
        st.error(f"Dataset `{PDF_PATH}` not detected in workspace!")

    st.markdown("---")
    st.markdown('<div class="sidebar-nav-title">Negative Safeguard Simulation</div>', unsafe_allow_html=True)
    st.session_state.simulate_pdf_error = st.toggle(
        "Simulate Source Access Error (C3)",
        value=st.session_state.simulate_pdf_error,
        help="Simulate source PDF unavailable/unreachable as required by Deliverable C3."
    )

# -----------------------------------------------------------------------------
# SCREEN 1: DELIVERABLE C2 — PRIMARY USER INTERFACE
# (Design Figure 2: Citizen Question, Answer, Citation, and Source-Opening Screen)
# -----------------------------------------------------------------------------
if st.session_state.active_nav == "Deliverable C2: Primary UI":
    st.markdown('<span class="badge-c2">Deliverable C2 • Design Figure 2</span>', unsafe_allow_html=True)
    st.title("Primary UI: Citizen Question, Answer & Citation Screen")
    st.caption("Per Figma Visual Specification C2: Presents citizen question input, progress indication, supported answer details, citation links, and source-inspection control.")

    st.markdown("---")

    # 1. Preset Question Selector Pills
    st.markdown("**Sample Citizen Inquiries (Click to Load):**")
    cols = st.columns([1, 1, 1, 1, 1.2])

    with cols[0]:
        if st.button("🗑️ Anti-Littering", use_container_width=True):
            st.session_state.selected_scenario_key = "littering"
            st.session_state.last_query_text = PRESET_SCENARIOS["littering"]["queries"][st.session_state.selected_lang]
            st.session_state.target_pdf_page = PRESET_SCENARIOS["littering"]["target_page"]
            st.session_state.target_search_terms = PRESET_SCENARIOS["littering"]["search_terms"]

    with cols[1]:
        if st.button("🚭 Anti-Smoking", use_container_width=True):
            st.session_state.selected_scenario_key = "smoking"
            st.session_state.last_query_text = PRESET_SCENARIOS["smoking"]["queries"][st.session_state.selected_lang]
            st.session_state.target_pdf_page = PRESET_SCENARIOS["smoking"]["target_page"]
            st.session_state.target_search_terms = PRESET_SCENARIOS["smoking"]["search_terms"]

    with cols[2]:
        if st.button("🎆 Firecrackers", use_container_width=True):
            st.session_state.selected_scenario_key = "firecrackers"
            st.session_state.last_query_text = PRESET_SCENARIOS["firecrackers"]["queries"][st.session_state.selected_lang]
            st.session_state.target_pdf_page = PRESET_SCENARIOS["firecrackers"]["target_page"]
            st.session_state.target_search_terms = PRESET_SCENARIOS["firecrackers"]["search_terms"]

    with cols[3]:
        if st.button("🍺 Liquor Ban", use_container_width=True):
            st.session_state.selected_scenario_key = "liquor"
            st.session_state.last_query_text = PRESET_SCENARIOS["liquor"]["queries"][st.session_state.selected_lang]
            st.session_state.target_pdf_page = PRESET_SCENARIOS["liquor"]["target_page"]
            st.session_state.target_search_terms = PRESET_SCENARIOS["liquor"]["search_terms"]

    with cols[4]:
        if st.button("⚠️ Out-of-Scope (Test)", use_container_width=True):
            st.session_state.selected_scenario_key = "out_of_scope"
            st.session_state.last_query_text = "Unsaon pag-apply og passport sa DFA Davao ug pila ang bayad?"

    # 2. Citizen Question Input Box
    query_input = st.text_input(
        "Citizen Question Field (Enter query in Bisaya, Tagalog, or English):",
        value=st.session_state.last_query_text,
        placeholder="e.g., Pila man ang multa kung maglabay og basura sa Davao City?"
    )

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        submit_search = st.button("🔍 Search Ordinances", type="primary", use_container_width=True)

    if submit_search:
        st.session_state.last_query_text = query_input

    # Simulated Progress Indication during retrieval
    if submit_search:
        progress_bar = st.progress(0, text="Initializing A-LAW-min retrieval pipeline...")
        time.sleep(0.15)
        progress_bar.progress(35, text="Parsing syntactic query intent across Davao City dialects...")
        time.sleep(0.15)
        progress_bar.progress(70, text="Retrieving candidate ordinance sections from Davao Code 2009...")
        time.sleep(0.15)
        progress_bar.progress(100, text="Executing per-detail Answer-Support Flow (Figure 4)...")
        time.sleep(0.1)
        progress_bar.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Decision Logic: Preset Scenarios vs Out-of-Scope vs Custom Match
    if st.session_state.selected_scenario_key == "out_of_scope" or "passport" in query_input.lower() or "dfa" in query_input.lower():
        # Negative Guardrail Display as required by C2
        st.markdown("""
        <div class="error-banner">
            <h4 style="margin: 0 0 6px 0; font-weight: 700;">⚠️ NO VERIFIED MUNICIPAL ORDINANCE RECORD FOUND</h4>
            <p style="margin: 0 0 8px 0; font-size: 0.9rem;">
                The inquiry pertains to the <strong>Department of Foreign Affairs (National Executive Agency)</strong>, 
                which falls outside the statutory jurisdiction of the <strong>Code of Ordinances of Davao City 2009</strong>.
            </p>
            <p style="margin: 0; font-size: 0.85rem; color: #7F1D1D;">
                <strong>Strict Verification Protocol (C2):</strong> When no supported municipal match is found, 
                A-LAW-min requests clarification or reports that no answer could be verified. 
                Unreviewed or ambiguous external records are strictly prevented from authorizing simulated legal answers.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Match Scenario or Fallback
        matched = engine.match_scenario(query_input)
        scenario_data = None
        if matched:
            scenario_key, scenario_data = matched
            st.session_state.selected_scenario_key = scenario_key
            st.session_state.target_pdf_page = scenario_data["target_page"]
            st.session_state.target_search_terms = scenario_data["search_terms"]
        elif st.session_state.selected_scenario_key in PRESET_SCENARIOS:
            scenario_data = PRESET_SCENARIOS[st.session_state.selected_scenario_key]

        if scenario_data:
            lang = st.session_state.selected_lang
            ans_payload = scenario_data["answers"].get(lang, scenario_data["answers"]["ceb"])

            # Main Supported Answer Container
            st.markdown(f"""
            <div class="prototype-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 700; font-size: 1.1rem; color: #0F172A;">
                        ⚖️ Supported Legal Answer ({lang_labels[lang]})
                    </span>
                    <span class="audit-pass">✓ 100% STATUTORY GROUNDED</span>
                </div>
                <p style="font-size: 0.95rem; color: #334155; margin-bottom: 1rem;">
                    {ans_payload['summary']}
                </p>
            """, unsafe_allow_html=True)

            # Detail rows with Citation Links
            for idx, item in enumerate(ans_payload["details"], 1):
                col_det, col_act = st.columns([4, 1.2])
                with col_det:
                    st.markdown(f"""
                    <div style="margin-bottom: 12px; padding: 10px 14px; background: #F8FAFC; border-radius: 6px; border: 1px solid #E2E8F0;">
                        <div style="font-weight: 600; font-size: 0.9rem; color: #1E293B;">
                            Detail {idx}: {item['claim']}
                        </div>
                        <div class="citation-badge">
                            📌 <strong>Statutory Citation:</strong> {item['citation']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_act:
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    if st.button(f"Inspect Source #{idx}", key=f"btn_src_{idx}", use_container_width=True):
                        st.session_state.active_nav = "Deliverable C3: Secondary UI"
                        st.session_state.target_pdf_page = scenario_data["target_page"]
                        st.session_state.target_search_terms = scenario_data["search_terms"]
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            # Master Source-Opening Control
            st.markdown("<br>", unsafe_allow_html=True)
            col_cta1, col_cta2 = st.columns([2, 1])
            with col_cta1:
                st.info(f"Target Ordinance Anchor: **{scenario_data['ordinance_meta']['title']}** | **{scenario_data['ordinance_meta']['article']}** | **Page {scenario_data['target_page']}**")
            with col_cta2:
                if st.button("🔍 Open Source Page & Inspection (Figure 3) ➔", type="primary", use_container_width=True):
                    st.session_state.active_nav = "Deliverable C3: Secondary UI"
                    st.rerun()

        else:
            # Custom Search Across 242 Pages
            st.info(f"Scanning 242 pages of Davao Code of Ordinances 2009 for: '{query_input}'...")
            results = engine.search_corpus(query_input, max_results=5)
            if results:
                st.success(f"Found {len(results)} candidate statutory matches in corpus:")
                for r in results:
                    st.markdown(f"""
                    <div class="prototype-card">
                        <strong>Page {r['page_num']}</strong> (Occurrences: {r['match_count']})
                        <div class="citation-badge">{r['snippet']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Inspect Page {r['page_num']} in C3", key=f"jump_{r['page_num']}"):
                        st.session_state.active_nav = "Deliverable C3: Secondary UI"
                        st.session_state.target_pdf_page = r['page_num']
                        st.session_state.target_search_terms = [query_input]
                        st.rerun()
            else:
                st.warning("No direct section matches found in the 2009 Code of Ordinances for this term. Please refine keywords.")

# -----------------------------------------------------------------------------
# SCREEN 2: DELIVERABLE C3 — SECONDARY USER INTERFACE
# (Design Figure 3: Secondary UI: Support-List and Source-Inspection Screen)
# -----------------------------------------------------------------------------
elif st.session_state.active_nav == "Deliverable C3: Secondary UI":
    st.markdown('<span class="badge-c3">Deliverable C3 • Design Figure 3</span>', unsafe_allow_html=True)
    st.title("Secondary UI: Support-List & Source-Inspection Screen")
    st.caption("Per Figma Visual Specification C3: Displays the list of support items for each answer detail and allows the citizen to inspect the linked source page with full verification audit.")

    st.markdown("---")

    col_support_list, col_pdf_viewer = st.columns([1.1, 1.4], gap="large")

    # ------------------
    # LEFT COLUMN: Support-List & Verification Audit (Figure 4)
    # ------------------
    with col_support_list:
        st.subheader("1. Answer Support Items List")
        
        scenario_key = st.session_state.selected_scenario_key
        if scenario_key in PRESET_SCENARIOS:
            scen = PRESET_SCENARIOS[scenario_key]
            lang = st.session_state.selected_lang
            details = scen["answers"].get(lang, scen["answers"]["ceb"])["details"]

            st.markdown(f"**Ordinance Metadata:** `{scen['ordinance_meta']['title']}`  \n**Article/Section:** `{scen['ordinance_meta']['article']}`, `{scen['ordinance_meta']['section']}`  \n**Archived Page:** `Page {scen['target_page']} of 242`")
            st.markdown("<br>", unsafe_allow_html=True)

            for idx, d in enumerate(details, 1):
                with st.expander(f"Support Item #{idx}: {d['claim'][:45]}...", expanded=(idx == 1)):
                    st.markdown(f"**Statement Claim:**  \n{d['claim']}")
                    st.markdown(f"**Exact Statutory Clause Extracted:**  \n> *\"{d['statutory_text']}\"*")
                    st.markdown(f"**Source Document Link:**  \n`{d['citation']}`")
                    st.markdown("---")
                    st.markdown("**Per-Detail Answer-Support Audit (Figure 4 Checklist):**")
                    
                    for chk in VERIFICATION_CHECKS:
                        c1, c2 = st.columns([3.5, 1])
                        with c1:
                            st.write(f"• **{chk['name']}**")
                            st.caption(chk['desc'])
                        with c2:
                            if st.session_state.simulate_pdf_error and chk["code"] == "CHK-05":
                                st.markdown("<span style='color: #DC2626; font-weight:700;'>FAIL ✗</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("<span class='audit-pass'>PASS ✓</span>", unsafe_allow_html=True)
        else:
            st.info("Select or submit an inquiry in Deliverable C2 to populate support items.")

    # ------------------
    # RIGHT COLUMN: Source-Inspection PDF Page Viewer
    # ------------------
    with col_pdf_viewer:
        st.subheader("2. Interactive Source-Inspection Screen")

        # Viewer Toolbar
        col_tb1, col_tb2, col_tb3 = st.columns([1.2, 1, 1.2])
        with col_tb1:
            total_pages = engine.get_total_pages()
            page_input = st.number_input(
                "Document Page:",
                min_value=1,
                max_value=total_pages,
                value=int(st.session_state.target_pdf_page),
                step=1
            )
            st.session_state.target_pdf_page = page_input

        with col_tb2:
            zoom_factor = st.selectbox("Render Zoom:", [1.0, 1.25, 1.5], index=1)

        with col_tb3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("⬅️ Return to C2", use_container_width=True):
                st.session_state.active_nav = "Deliverable C2: Primary UI"
                st.rerun()

        # Render PDF Page with Error Simulation
        try:
            rendered_img = engine.render_page(
                page_num=st.session_state.target_pdf_page,
                search_terms=st.session_state.target_search_terms,
                simulate_error=st.session_state.simulate_pdf_error,
                zoom=zoom_factor
            )

            st.caption(f"Showing official page {st.session_state.target_pdf_page} of 242 with dynamic statutory yellow highlighting.")
            st.image(rendered_img, use_container_width=True, caption=f"Davao Code of Ordinances 2009 — Page {st.session_state.target_pdf_page}")

        except SourceAccessError as err:
            # Deliverable C3 Mandate:
            # "When a source file is unavailable, the screen shows a source-access error.
            # The system does not silently substitute a different page or mark unreviewed text as verified."
            st.markdown(f"""
            <div class="error-banner">
                <h4 style="margin: 0 0 6px 0; font-weight: 700;">🚨 SOURCE-ACCESS ERROR (SEC-404-UNAVAILABLE)</h4>
                <p style="margin: 0 0 8px 0; font-size: 0.95rem;">
                    <strong>Source file or page stream cannot be accessed.</strong>
                </p>
                <p style="margin: 0 0 8px 0; font-size: 0.85rem;">
                    <em>{str(err)}</em>
                </p>
                <div style="background: #FFFFFF; padding: 10px; border-radius: 4px; border: 1px solid #FECACA; font-size: 0.82rem; color: #7F1D1D;">
                    <strong>Strict Integrity Enforcement:</strong> The system will <u>NEVER</u> silently substitute a different page, 
                    approximate coordinates, or mark unreviewed text as verified. Detail release has been suspended.
                </div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SCREEN 3: SYSTEM ARCHITECTURE & FLOWCHARTS (C1, C4, C5)
# -----------------------------------------------------------------------------
elif st.session_state.active_nav == "System Architecture & Flowcharts (C1, C4, C5)":
    st.title("System Architecture & Verification Pipeline Specifications")
    st.caption("Figma Visual Specifications C1, C4, and C5: Proposed Architecture and Detailed Process Flowcharts.")
    st.markdown("---")

    tabs = st.tabs([
        "Figure 1: Proposed System Architecture (C1)",
        "Figure 4: Main Answer-Support Flow (C4)",
        "Figure 5: Document Preparation Pipeline (C5)"
    ])

    with tabs[0]:
        st.subheader("Figure 1 — Proposed System Architecture")
        st.markdown("""
        > **C1 Architecture Specification:** Our source preparation pipeline feeds both the retrieval stage and the per-detail support checker. 
        > The answer presenter retains the supporting section and page identifiers throughout. 
        > Scanned PDFs and citizen questions yield supported answer details, missing-support notices, and source-page controls.
        """)
        if os.path.exists("Figure 1 Proposed System Architecture.png"):
            st.image("Figure 1 Proposed System Architecture.png", use_container_width=True)
        else:
            st.warning("Figure 1 Proposed System Architecture.png not found in directory.")

    with tabs[1]:
        st.subheader("Figure 4 — Main Answer-Support Flow (Per-Detail)")
        st.markdown("""
        > **C4 Verification Specification:** We run the support decision independently for each answer detail. 
        > The required checks are: readable and reviewed section text; correct ordinance, version, and section identifier; 
        > all mandatory dependencies resolved; recorded scope conditions met; source pages accessible; and no unresolved conflict.
        """)
        if os.path.exists("Figure 4 Flowchart.png"):
            st.image("Figure 4 Flowchart.png", use_container_width=True)
        else:
            st.warning("Figure 4 Flowchart.png not found in directory.")

    with tabs[2]:
        st.subheader("Figure 5 — Document Preparation, Review, Indexing & Source-Access")
        st.markdown("""
        > **C5 Pipeline Specification:** The system takes PDF pages as input and produces reviewed, searchable section records 
        > with source links as output. Records that remain pending after review are not eligible to support any verified answer detail.
        """)
        if os.path.exists("Figure 5 Flowchart.png"):
            st.image("Figure 5 Flowchart.png", use_container_width=True)
        else:
            st.warning("Figure 5 Flowchart.png not found in directory.")

# -----------------------------------------------------------------------------
# SCREEN 4: CORPUS EXPLORER (Davao Code of Ordinances 2009)
# -----------------------------------------------------------------------------
elif st.session_state.active_nav == "Corpus Explorer (Davao Code 2009)":
    st.title("Davao City Code of Ordinances 2009 — Corpus Explorer")
    st.caption("Live search and multi-page browser across all 242 pages of the municipal ordinance corpus.")
    st.markdown("---")

    kw = st.text_input("Enter search term (e.g. 'penalty', 'traffic', 'curfew', 'noise', 'liquor', 'waste'):", value="penalty")
    if kw:
        results = engine.search_corpus(kw, max_results=12)
        st.write(f"Found **{len(results)}** pages containing **'{kw}'**:")
        
        c_list, c_view = st.columns([1, 1.2])
        with c_list:
            for item in results:
                p_num = item["page_num"]
                with st.expander(f"Page {p_num} ({item['match_count']} matches)"):
                    st.write(item["snippet"])
                    if st.button(f"View Page {p_num}", key=f"v_{p_num}"):
                        st.session_state.target_pdf_page = p_num
                        st.session_state.target_search_terms = [kw]
                        st.session_state.active_nav = "Deliverable C3: Secondary UI"
                        st.rerun()

        with c_view:
            st.markdown(f"**Quick Preview of Page {st.session_state.target_pdf_page}:**")
            preview_img = engine.render_page(st.session_state.target_pdf_page, search_terms=[kw], zoom=1.1)
            st.image(preview_img, use_container_width=True)
