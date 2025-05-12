from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QTableView, QLineEdit, QLabel, QMessageBox
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QAbstractTableModel
import pandas as pd

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
        return None

class ProzorSButtonima(QWidget):
    def __init__(self):
        super().__init__()
        self.uredi_korisnika_gumb = None
        self.uredi_usluge_gumb = None
        self.nazad_gumb = None
        self.tablica_view = QTableView()
        self.sve_osobe_df = pd.DataFrame()
        self.zaposlenici_df = pd.DataFrame()
        self.usluge_df = pd.DataFrame()
        self.unos_izmjene = QLineEdit()
        self.izmjeni_gumb = QPushButton("Promijeni")
        self.info_label = QLabel("")
        self.zadnje_kliknuti_indeks = None
        self.trenutno_prikazana_tablica = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Studio")
        self.setGeometry(500, 400, 800, 500)
        self._init_style()
        self._init_widgets()
        self._init_layout()
        self._ucitaj_sve_osobe()
        self._ucitaj_usluge()

    def _init_style(self):
        self.setStyleSheet("background-color: #98FB98;")

    def _init_widgets(self):
        font_gumb = QFont()
        font_gumb.setPointSize(12)
        font_gumb_promjni =QFont()
        font_gumb_promjni.setPointSize(10)
      

        self.uredi_korisnika_gumb = QPushButton("Uredi Zaposlenike")
        self.uredi_korisnika_gumb.setFont(font_gumb)
        self.uredi_korisnika_gumb.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.uredi_korisnika_gumb.clicked.connect(self._prikazi_zaposlenike)

        self.uredi_usluge_gumb = QPushButton("Uredi Usluge")
        self.uredi_usluge_gumb.setFont(font_gumb)
        self.uredi_usluge_gumb.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.uredi_usluge_gumb.clicked.connect(self._prikazi_usluge_tablica)

        self.nazad_gumb = QPushButton("Nazad")
        self.nazad_gumb.setFont(font_gumb)
        self.nazad_gumb.setStyleSheet("background-color: #DC143C ; color: white; padding: 10px; border-radius: 5px;")
        self.tablica_view.clicked.connect(self._prikazi_unos_za_izmjenu)

        self.izmjeni_gumb = QPushButton("Promijeni")
        self.izmjeni_gumb.setFont(font_gumb_promjni)
        self.izmjeni_gumb.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;") # Manji padding
        self.izmjeni_gumb.clicked.connect(self._izvrsi_izmjenu)

        self.unos_izmjene.setPlaceholderText("Unesi promjenu:")
        self.unos_izmjene.setStyleSheet("font-size: 14px;") 
        self.unos_izmjene.setVisible(False)
        self.izmjeni_gumb.setVisible(False)

        self.info_label.setStyleSheet("font-style: italic;font-size : 18px;")
    def _init_layout(self):
        grid = QGridLayout()
        grid.addWidget(self.uredi_korisnika_gumb, 0, 0)
        grid.addWidget(self.uredi_usluge_gumb, 0, 1)
        grid.addWidget(self.tablica_view, 1, 0, 1, 2)
        grid.addWidget(self.info_label, 2, 0, 1, 2)
        grid.addWidget(self.unos_izmjene, 3, 0, 1, 2)
        grid.addWidget(self.izmjeni_gumb, 4, 0, 1, 2)
        #grid.addWidget(self.nazad_gumb, 5, 0, 1, 2)
        self.setLayout(grid)

    def _ucitaj_sve_osobe(self):
        try:
            self.sve_osobe_df = pd.read_csv("sve_osobe.csv", encoding="utf-8")
        except FileNotFoundError:
            print("Datoteka sve_osobe.csv nije pronađena.")
            self.sve_osobe_df = pd.DataFrame()
        except Exception as e:
            print(f"Greška pri učitavanju sve_osobe.csv: {e}")

    def _ucitaj_usluge(self):
        try:
            self.usluge_df = pd.read_csv("usluge.csv", encoding="utf-8")
        except FileNotFoundError:
            print("Datoteka usluge.csv nije pronađena.")
            self.usluge_df = pd.DataFrame()
        except Exception as e:
            print(f"Greška pri učitavanju usluge.csv: {e}")

    def _prikazi_zaposlenike(self):
        self.zaposlenici_df = self.sve_osobe_df.loc[self.sve_osobe_df['Tip'] == 'Zaposlenik'].copy()
        model = PandasModel(self.zaposlenici_df)
        self.tablica_view.setModel(model)
        self.tablica_view.setVisible(True)
        self.unos_izmjene.setVisible(False)
        self.izmjeni_gumb.setVisible(False)
        self.info_label.setText("")
        self.zadnje_kliknuti_indeks = None
        self.trenutno_prikazana_tablica = 'zaposlenici'

    def _prikazi_usluge_tablica(self):
        model = PandasModel(self.usluge_df)
        self.tablica_view.setModel(model)
        self.tablica_view.setVisible(True)
        self.unos_izmjene.setVisible(False)
        self.izmjeni_gumb.setVisible(False)
        self.info_label.setText("")
        self.zadnje_kliknuti_indeks = None
        self.trenutno_prikazana_tablica = 'usluge'

    def _prikazi_unos_za_izmjenu(self, index):
        row = index.row()
        col = index.column()
        if self.trenutno_prikazana_tablica == 'zaposlenici':
            value = str(self.zaposlenici_df.iloc[row, col])
            header = self.zaposlenici_df.columns[col]
        elif self.trenutno_prikazana_tablica == 'usluge':
            value = str(self.usluge_df.iloc[row, col])
            header = self.usluge_df.columns[col]
        else:
            return

        self.unos_izmjene.setText("")
        self.unos_izmjene.setPlaceholderText("Unesi promjenu:")
        self.unos_izmjene.setVisible(True)
        self.izmjeni_gumb.setVisible(True)
        self.info_label.setText(f"Odabrano: {header} - {value}")
        self.zadnje_kliknuti_indeks = index

    def _izvrsi_izmjenu(self):
        if self.zadnje_kliknuti_indeks is not None:
            nova_vrijednost = self.unos_izmjene.text()
            row = self.zadnje_kliknuti_indeks.row()
            col = self.zadnje_kliknuti_indeks.column()

            try:
                if self.trenutno_prikazana_tablica == 'zaposlenici':
                    original_index = self.sve_osobe_df[self.sve_osobe_df['Tip'] == 'Zaposlenik'].index[row]
                    self.sve_osobe_df.iloc[original_index, col] = nova_vrijednost
                    self.sve_osobe_df.to_csv("sve_osobe.csv", index=False, encoding="utf-8")
                    self._prikazi_zaposlenike()
                elif self.trenutno_prikazana_tablica == 'usluge':
                    self.usluge_df.iloc[row, col] = nova_vrijednost
                    self.usluge_df.to_csv("usluge.csv", index=False, encoding="utf-8")
                    self._prikazi_usluge_tablica()

                self.unos_izmjene.setVisible(False)
                self.izmjeni_gumb.setVisible(False)
                self.info_label.setText("Promjena spremljena.")

            except Exception as e:
                QMessageBox.critical(self, "Greška", f"Došlo je do pogreške prilikom spremanja: {e}")

        else:
            self.info_label.setText("Nije odabrana ćelija za promjenu.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = ProzorSButtonima()
    prozor.show()
    sys.exit(app.exec_())