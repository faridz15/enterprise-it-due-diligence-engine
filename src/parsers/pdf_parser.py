import pdfplumber
import re
import os
from src.models.contract import VendorContract

class ContractParser:
    def __init__(self, contracts_dir: str):
        self.contracts_dir = contracts_dir

    def extract_contracts(self) -> list:
        print("[Parser] Ingesting unstructured PDF contracts into Objects...")
        contracts = []
        
        for filename in os.listdir(self.contracts_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(self.contracts_dir, filename)
                
                with pdfplumber.open(filepath) as pdf:
                    text = "".join(page.extract_text() + "\n" for page in pdf.pages)

                    vendor = re.search(r"Vendor Name:\s*(.+)", text)
                    sla = re.search(r"SLA Uptime:\s*(.+)", text)
                    validity = re.search(r"Validity Period:.*to\s*(.+)", text)

                    v_name = vendor.group(1) if vendor else "Unknown Vendor"
                    s_cov = sla.group(1) if sla else "Unknown SLA"
                    expiry = validity.group(1) if validity else "01 Jan 1970"

                    # Instansiasi Objek Contract
                    contract = VendorContract(filename, v_name, s_cov, expiry)
                    contracts.append(contract)
                    
        return contracts