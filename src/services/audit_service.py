import pandas as pd
import os
from datetime import datetime
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, CONTRACTS_DIR
from src.parsers.asset_parser import AssetParser
from src.parsers.pdf_parser import ContractParser
from src.rules.contract_expiry import SLAComplianceRule

class AuditOrchestrator:
    def __init__(self):
        # Menginisialisasi komponen Ingestion (Parser)
        self.asset_parser = AssetParser(RAW_DATA_DIR)
        self.contract_parser = ContractParser(CONTRACTS_DIR)

    def run_full_audit(self):
        print("[Service] Initiating Enterprise Audit Sequence (OOP Engine)...")
        
        # 1. Ingest Data: Ubah file mentah menjadi barisan Objek Python
        assets = self.asset_parser.load_hardware()
        contracts = self.contract_parser.extract_contracts()
        
        # 2. Terapkan Business Rules Engine ke setiap Objek
        sla_rule = SLAComplianceRule(contracts)
        for asset in assets:
            sla_rule.evaluate(asset)
            
        # 3. Konversi kembali Objek menjadi DataFrame untuk Laporan
        df_hw = pd.DataFrame([a.to_dict() for a in assets])
        
        # 4. Handle Software (Hybrid Approach: Menggunakan Pandas langsung untuk efisiensi)
        sw_path = os.path.join(RAW_DATA_DIR, 'software_licenses.xlsx')
        df_sw = pd.read_excel(sw_path)
        df_sw['Vendor'] = df_sw['Vendor'].str.replace(' ', '').str.strip()
        df_sw['Expiry Date'] = pd.to_datetime(df_sw['Expiry Date'], errors='coerce')
        today = datetime.today()
        df_sw['Status'] = df_sw['Expiry Date'].apply(lambda x: 'Expired' if pd.notnull(x) and x < today else 'Active')
        df_sw['Status'] = df_sw.apply(lambda row: 'Waste (Unassigned)' if row['Assigned To'] == 'Unassigned' else row['Status'], axis=1)

        # 5. Filter "Red Flags" berdasarkan properti Objek yang sudah divalidasi
        red_flags_df = df_hw[df_hw['Contract Status'] == 'UNPROTECTED (Contract Expired)'].copy()
        if not red_flags_df.empty:
            red_flags_df['Finding'] = "Operational asset lacks active SLA maintenance."

        # 6. Ekspor Laporan Akhir
        report_path = os.path.join(PROCESSED_DATA_DIR, 'Final_Audit_Report.xlsx')
        with pd.ExcelWriter(report_path) as writer:
            df_hw.to_excel(writer, sheet_name='Hardware_Cleaned', index=False)
            df_sw.to_excel(writer, sheet_name='Software_Cleaned', index=False)
            if not red_flags_df.empty:
                red_flags_df.to_excel(writer, sheet_name='RED_FLAGS', index=False)
                
        print(f"[Service] Audit Complete. Output saved to {report_path}\n")