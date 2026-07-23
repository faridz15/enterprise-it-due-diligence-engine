import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Pastikan file generator.py dan config.py masih ada di folder src
from src.generator import generate_dummy_data, generate_dummy_contracts
from src.config import PROCESSED_DATA_DIR

# Import Orchestrator dari arsitektur DDD/OOP yang baru
from src.services.audit_service import AuditOrchestrator

# 1. Konfigurasi Halaman - LAYOUT WIDE (NOC Style)
st.set_page_config(page_title="IT Due Diligence | Command Center", layout="wide", page_icon="📡")

# Custom CSS untuk memperhalus UI
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #00E5FF !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Control Panel
st.sidebar.title("⚙️ NOC Control Panel")
st.sidebar.markdown("M&A Infrastructure Due Diligence Engine.")
st.sidebar.markdown("---")

if st.sidebar.button("🚀 EXECUTE FULL SCAN", use_container_width=True):
    with st.spinner("Initiating 500+ Assets Parsing & SLA Verification (OOP Engine)..."):
        # 1. Generate simulasi file mentah
        generate_dummy_data()
        generate_dummy_contracts()
        
        # 2. Panggil Orchestrator dengan arsitektur Domain-Driven Design
        orchestrator = AuditOrchestrator()
        orchestrator.run_full_audit()
        
    st.sidebar.success("✅ System Scan Complete!")

# 3. Main Header
st.title("📡 M&A Infrastructure Due Diligence Command Center")
st.markdown("*Automated Asset Discovery, SLA Verification, and Cross-Relational Risk Assessment.*")
st.markdown("---")

report_path = os.path.join(PROCESSED_DATA_DIR, 'Final_Audit_Report.xlsx')

# 4. Tampilkan Data
if os.path.exists(report_path):
    df_hw = pd.read_excel(report_path, sheet_name='Hardware_Cleaned')
    df_sw = pd.read_excel(report_path, sheet_name='Software_Cleaned')
    
    try:
        df_red = pd.read_excel(report_path, sheet_name='RED_FLAGS')
        total_red_flags = len(df_red)
    except Exception:
        df_red = pd.DataFrame()
        total_red_flags = 0

    # --- A. METRIK UTAMA (KARTU EKSEKUTIF NOC) ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Network Nodes", f"{len(df_hw)} Units", "Active Scanned")
    col2.metric("SLA Violations (Red Flags)", f"{total_red_flags} Issues", "- High Severity", delta_color="inverse")
    
    wasted_sw = len(df_sw[df_sw['Status'] == 'Waste (Unassigned)'])
    col3.metric("Idle License / Waste", f"{wasted_sw} Licenses", "- Financial Leak", delta_color="inverse")
    
    covered_hw = len(df_hw[df_hw['Contract Status'] == 'Covered'])
    col4.metric("Protected Infrastructure", f"{covered_hw} Units", "SLA Active", delta_color="normal")

    st.markdown("---")

    # --- B. BAGIAN VISUALISASI GRAFIK (PLOTLY DARK THEME) ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Hardware Risk Distribution")
        # Ganti 'Risk Status' menjadi 'Risk Level'
        fig_hw = px.pie(df_hw, names='Risk Level', hole=0.5, color='Risk Level', 
                        color_discrete_map={'Safe':'#00CC96', 'Critical':'#EF553B'})
        fig_hw.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hw, use_container_width=True)
        
    with col_chart2:
        st.subheader("Software License Analytics")
        # Mengubah jadi Bar Chart berbasis agregasi status
        status_counts = df_sw['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_sw = px.bar(status_counts, x='Status', y='Count', color='Status', text='Count',
                        color_discrete_map={'Active':'#00CC96', 'Expired':'#EF553B', 'Waste (Unassigned)':'#FFA15A'})
        fig_sw.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sw, use_container_width=True)

    # --- C. BAGIAN RED FLAGS (TABLE LEBAR) ---
    if total_red_flags > 0:
        st.markdown("### 🚨 Critical Operational Risks (SLA Unprotected)")
        st.error(f"WARNING: Detected {total_red_flags} active infrastructure assets operating without valid Vendor SLA maintenance contracts.")
        # Nama kolom telah disesuaikan dengan to_dict() di model asset.py
        st.dataframe(df_red[['Asset ID', 'Device Category', 'Model', 'Location', 'EOL Date', 'Contract Status']], use_container_width=True)

else:
    st.info("👈 Silakan jalankan 'EXECUTE FULL SCAN' dari panel kontrol NOC untuk memulai analitik.")