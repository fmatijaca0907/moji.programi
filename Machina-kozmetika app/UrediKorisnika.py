# UrediKorisnik.py
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

class ProzorUrediKorisnik(QWidget):
    def __init__(self):
        super().__init__()
        self.tablica_view = QTableView()
        self.sve_osobe_df = pd.DataFrame()
        self.korisnici_df = pd.DataFrame()
        self.unos_izmjene = QLineEdit()
        self.izmjeni_gumb = QPushButton("Promijeni")
        self.info_label = QLabel("")
        self.zadnje_kliknuti_indeks = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Uredi korisnika")
        self.setGeometry(500, 400, 800, 500)
        self.setStyleSheet("background-color: #98FF98;")
        self._init_widgets()
        self._init_layout()
        self._ucitaj_korisnike()

    def _init_widgets(self):
        font_promjeni = QFont()
        font_promjeni.setPointSize(10)

        self.tablica_view.clicked.connect(self._prikazi_unos_za_izmjenu)

        self.izmjeni_gumb = QPushButton("Promijeni")
        self.izmjeni_gumb.setFont(font_promjeni)
        self.izmjeni_gumb.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        self.izmjeni_gumb.clicked.connect(self._izvrsi_izmjenu)

        self.unos_izmjene.setPlaceholderText("Unesi promjenu:")
        self.unos_izmjene.setStyleSheet("font-size: 14px;")
        self.unos_izmjene.setVisible(False)
        self.izmjeni_gumb.setVisible(False)

        self.info_label.setStyleSheet("font-style: italic; font-size: 18px;")

    def _init_layout(self):
        grid = QGridLayout()
        grid.addWidget(self.tablica_view, 0, 0, 1, 2)
        grid.addWidget(self.info_label, 1, 0, 1, 2)
        grid.addWidget(self.unos_izmjene, 2, 0, 1, 2)
        grid.addWidget(self.izmjeni_gumb, 3, 0, 1, 2)
        self.setLayout(grid)

    def _ucitaj_korisnike(self):
        try:
            self.sve_osobe_df = pd.read_csv("sve_osobe.csv", encoding="utf-8")
            self.korisnici_df = self.sve_osobe_df.loc[self.sve_osobe_df['Tip'] == 'Korisnik'].copy()
            model = PandasModel(self.korisnici_df)
            self.tablica_view.setModel(model)
        except FileNotFoundError:
            print("Datoteka sve_osobe.csv nije pronađena.")
            self.sve_osobe_df = pd.DataFrame()
            self.korisnici_df = pd.DataFrame()
        except Exception as e:
            print(f"Greška pri učitavanju sve_osobe.csv: {e}")

    def _prikazi_unos_za_izmjenu(self, index):
        row = index.row()
        col = index.column()
        value = str(self.korisnici_df.iloc[row, col])
        header = self.korisnici_df.columns[col]

        self.unos_izmjene.setText("")
        self.unos_izmjene.setPlaceholderText("Unesi promjenu:")
        self.unos_izmjene.setVisible(True)
        self.izmjeni_gumb.setVisible(True)
        self.info_label.setText(f"Odabrano: {header} - {value}")
        self.zadnje_kliknuti_indeks = index

    def _izvrsi_izmjenu(self):
        if self.zadnje_kliknuti_indeks is not None:
            nova_vrijednost = self.unos_izmjene.text()
            row_in_korisnici_df = self.zadnje_kliknuti_indeks.row()
            col = self.zadnje_kliknuti_indeks.column()

            try:
                # Pronađi originalni indeks u sve_osobe_df
                original_index = self.sve_osobe_df[self.sve_osobe_df['Tip'] == 'Korisnik'].index[row_in_korisnici_df]
                self.sve_osobe_df.iloc[original_index, col] = nova_vrijednost
                self.sve_osobe_df.to_csv("sve_osobe.csv", index=False, encoding="utf-8")
                self._ucitaj_korisnike() # Ponovno učitaj da se promjene vide
                self.unos_izmjene.setVisible(False)
                self.izmjeni_gumb.setVisible(False)
                self.info_label.setText("Promjena spremljena.")
            except Exception as e:
                QMessageBox.critical(self, "Greška", f"Došlo je do pogreške prilikom spremanja: {e}")
        else:
            self.info_label.setText("Nije odabrana ćelija za promjenu.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = ProzorUrediKorisnik()
    prozor.show()
    sys.exit(app.exec_())