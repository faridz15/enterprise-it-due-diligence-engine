from src.models.asset import HardwareAsset
from src.models.contract import VendorContract

class SLAComplianceRule:
    def __init__(self, active_contracts: list):
        self.active_contracts = active_contracts

    def evaluate(self, asset: HardwareAsset):
        if not self.active_contracts:
            asset.contract_status = "UNPROTECTED (No Active Contracts)"
            return

        # Logika Bisnis: Cari kontrak utama (Misal dari Ericsson)
        main_contracts = [c for c in self.active_contracts if 'Ericsson' in c.vendor_name]
        
        if not main_contracts:
            asset.contract_status = "UNPROTECTED (Vendor Mismatch)"
            return
            
        primary_contract = main_contracts[0]
        
        # Aturan Inti: Jika umur perangkat keras lebih panjang dari umur kontrak SLA = Risiko Operasional
        if asset.eol_date > primary_contract.expiry_date:
            asset.contract_status = "UNPROTECTED (Contract Expired)"
        else:
            asset.contract_status = "Covered"