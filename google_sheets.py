import gspread

class GoogleSheets:
    def __init__(self, credenciales, documento, sheetNom):
        self.gc = gspread.service_account_from_dict(credenciales)
        self.sh = self.gc.open(documento)
        self.sheet = self.sh.worksheet(sheetNom)

    def write_data(self, range, data):
        self.sheet.update(range, data)
    
    def ultimaFilaRango(self):
        ultimaFila = len(self.sheet.get_all_values()) + 1
        # deta = self.sheet.get_values()
        # cantColumnas = len(deta[0]) if deta else 1
        rango_i = f"A{ultimaFila}"
        rango_f = f"H{ultimaFila}" #f"{chr(ord('A') + cantColumnas - 1)}{ultimaFila}"
        return f"{rango_i}:{rango_f}"