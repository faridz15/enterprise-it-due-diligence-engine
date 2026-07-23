import pandas as pd
import os
import random
from datetime import datetime, timedelta
from fpdf import FPDF
from src.config import RAW_DATA_DIR, CONTRACTS_DIR

def generate_dummy_data():
    print("[System] Generating 500+ synthetic Telecom & IIoT assets...")
    
    # 1. Generate Massive Hardware Data (500 Rows)
    categories = ['5G Core Server', 'IoT Gateway (LoRaWAN)', 'mmWave Radar Node', 'Edge Compute Unit', 'Drive Test Equipment']
    models = ['PowerEdge R740', 'Catalyst IR1101', 'IWR6843', 'RAK7249', 'G-NetTrack Kit']
    manufacturers = ['Ericsson', 'Cisco', 'Texas Instruments', 'Rak Wireless', 'Dell']
    locations = ['Data Center JKT', 'Site A (Remote)', 'Site B (Field)', 'Base Station C', 'Rawa Lakbok Site']
    
    hw_data = []
    today = datetime.today()
    
    for i in range(1, 501):
        cat = random.choice(categories)
        eol_date = today + timedelta(days=random.randint(-365, 1095)) 
        
        hw_data.append({
            'Asset ID': f'HW-{1000+i}',
            'Device Category': cat,
            'Model': random.choice(models),
            'Manufacturer': random.choice(manufacturers),
            'Location': random.choice(locations),
            'EOL Date': eol_date.strftime('%Y-%m-%d')
        })
        
    df_hw = pd.DataFrame(hw_data)
    df_hw.to_csv(os.path.join(RAW_DATA_DIR, 'hardware_inventory.csv'), index=False)

    # 2. Generate Massive Software Data (50 Rows)
    sw_data = {
        'License ID': [f'LIC-{i:03d}' for i in range(1, 51)],
        'Software Name': ['MATLAB R2023a', 'G-NetTrack Pro', 'UiPath Studio', 'Cisco Packet Tracer', 'Atoll Microwave'] * 10,
        'Vendor': ['MathWorks', 'GyokovSolutions', 'UiPath', 'Cisco Systems', 'Forsk'] * 10,
        'Expiry Date': [(today + timedelta(days=random.randint(-100, 700))).strftime('%Y-%m-%d') for _ in range(50)],
        'Assigned To': ['Signal Processing Team', 'Drive Test Eng', 'RPA Dev', 'Network Architect', 'Unassigned'] * 10
    }
    df_sw = pd.DataFrame(sw_data)
    
    df_sw.loc[5, 'Expiry Date'] = 'N/A'
    df_sw.loc[12, 'Vendor'] = 'Math Works'
    df_sw.to_excel(os.path.join(RAW_DATA_DIR, 'software_licenses.xlsx'), index=False)
    
    print("[System] Massive tabular data generated successfully.\n")

def generate_dummy_contracts():
    print("[System] Generating synthetic PDF contracts...")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    content = """
    MASTER SERVICE AGREEMENT
    -------------------------------------------------
    Vendor Name: Ericsson Indonesia
    Contract Reference: CTR-2024-ER-998
    Scope of Work: Maintenance for Private 5G Core, mmWave Radar Sensors, and LoRaWAN Gateways.
    Service Level Agreement (SLA) Uptime: 99.99%
    Validity Period: 01 Jan 2024 to 31 Dec 2025
    Total Contract Value: $250,000 USD / year
    -------------------------------------------------
    CONFIDENTIAL - FOR INTERNAL DUE DILIGENCE ONLY
    """
    for line in content.split('\n'):
        pdf.cell(200, 8, txt=line.strip(), ln=True, align='L')
        
    pdf_path = os.path.join(CONTRACTS_DIR, 'Ericsson_SLA_Contract_2024.pdf')
    pdf.output(pdf_path)
    print(f"[System] Contract generated at {pdf_path}\n")