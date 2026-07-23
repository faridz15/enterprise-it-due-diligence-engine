import pandas as pd
import os
from src.models.asset import HardwareAsset

class AssetParser:
    def __init__(self, raw_dir: str):
        self.raw_dir = raw_dir

    def load_hardware(self) -> list:
        print("[Parser] Loading tabular hardware inventory into Objects...")
        hw_path = os.path.join(self.raw_dir, 'hardware_inventory.csv')
        df = pd.read_csv(hw_path)
        
        assets = []
        for _, row in df.iterrows():
            asset = HardwareAsset(
                asset_id=row['Asset ID'],
                category=row['Device Category'],
                model=row['Model'],
                location=row['Location'],
                eol_date_str=row['EOL Date']
            )
            assets.append(asset)
            
        return assets