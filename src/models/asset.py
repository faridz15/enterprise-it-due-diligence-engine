from datetime import datetime

class HardwareAsset:
    def __init__(self, asset_id: str, category: str, model: str, location: str, eol_date_str: str):
        self.asset_id = asset_id
        self.category = category
        self.model = model
        self.location = location
        self.eol_date = self._parse_date(eol_date_str)
        self.is_eol = self._check_eol_status()
        self.contract_status = "Unknown"

    def _parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(str(date_str).split(' ')[0], '%Y-%m-%d')
        except ValueError:
            return datetime.today()

    def _check_eol_status(self) -> bool:
        return self.eol_date < datetime.today()

    def to_dict(self):
        return {
            "Asset ID": self.asset_id,
            "Device Category": self.category,  # Disamakan dengan dashboard
            "Model": self.model,
            "Location": self.location,
            "EOL Date": self.eol_date.strftime('%Y-%m-%d'),
            "Risk Level": "Critical" if self.is_eol else "Safe",  # Disamakan dengan Pie Chart
            "Contract Status": self.contract_status
        }