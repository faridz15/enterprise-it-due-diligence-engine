from datetime import datetime

class VendorContract:
    def __init__(self, filename: str, vendor_name: str, sla_coverage: str, expiry_date_str: str):
        self.filename = filename
        self.vendor_name = vendor_name
        self.sla_coverage = sla_coverage
        self.expiry_date = self._parse_date(expiry_date_str)
        
    def _parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str.strip(), '%d %b %Y')
        except ValueError:
            return datetime.today()

    def is_active(self) -> bool:
        return self.expiry_date >= datetime.today()