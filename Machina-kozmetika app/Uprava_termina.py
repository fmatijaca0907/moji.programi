from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QCalendarWidget, QListWidget, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
import sys
import pandas as pd

class UpravljanjeTerminimaProzor(QWidget):
    def __init__(self):
        super().__init__()
        self.termini_df = pd.DataFrame(columns=['Datum', 'Vrijeme', 'Usluga', 'Ime Korisnika', 'Tip Korisnik'])
        self.initUI()
        self.ucitaj_termine()
        self.odabrani_termin_index_lista = None # Za praćenje indeksa odabranog termina u listi

    def initUI(self):
        self.setWindowTitle("Upravljanje terminima")
        self.setGeometry(800, 400, 600, 480) # Povećajte visinu prozora zbog labela
        self.setStyleSheet("background-color: #98FB98;")
        self.init_fonts()
        self.init_widgets()
        self.init_layout()

    def init_fonts(self):
        self.naslov_font = QFont("Arial", 16, QFont.Bold)
        self.label_font = QFont("Arial",12)
        self.gumb_font = QFont("Arial", 10)

    def init_widgets(self):
        self.naslov_label = QLabel("Prikaz termina i usluga za datum")
        self.naslov_label.setFont(self.naslov_font)
        self.naslov_label.setAlignment(Qt.AlignCenter)

        self.datum_label = QLabel("Odaberi datum:")
        self.datum_label.setFont(self.label_font)

        self.usluga_label = QLabel("Usluge na taj datum:")
        self.usluga_label.setFont(self.label_font)

        self.kalendar = QCalendarWidget(self)
        self.kalendar.clicked[QDate].connect(self.prikazi_usluge)

        self.lista_usluga = QListWidget(self)
        self.lista_usluga.itemClicked.connect(self.omoguci_gumb_ukloni)

        self.ukloni_gumb = QPushButton("Ukloni")
        self.ukloni_gumb.setFont(self.gumb_font)
        self.ukloni_gumb.setStyleSheet("background-color: #f44336; color: white; padding: 5px; border-radius: 3px;")
        self.ukloni_gumb.setEnabled(False)
        self.ukloni_gumb.clicked.connect(self.ukloni_termin)

        self.studio_label = QLabel("Studio Laura")
        studio_font = QFont("Script MT Bold", 16)
        self.studio_label.setFont(studio_font)
        self.studio_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.studio_label.setStyleSheet("color: #555555;")

    def init_layout(self):
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.naslov_label, 0, 0, 1, 2)
        grid_layout.addWidget(self.datum_label, 1, 0)
        grid_layout.addWidget(self.usluga_label, 1, 1)
        grid_layout.addWidget(self.kalendar, 2, 0)
        grid_layout.addWidget(self.lista_usluga, 2, 1)

        layout.addLayout(grid_layout)
        layout.addSpacing(40)
        layout.addWidget(self.ukloni_gumb)
        layout.addWidget(self.studio_label)
        layout.addStretch(1)

        self.setLayout(layout)

    def ucitaj_termine(self):
        try:
            temp_df = pd.read_csv("termini.csv", header=None) 

            datum_format1 = pd.to_datetime(temp_df.iloc[:, 0], format='%Y-%m-%d', errors='coerce')
            datum_format2 = pd.to_datetime(temp_df.iloc[:, 0], format='%d-%m-%Y', errors='coerce')
            datum_format3 = pd.to_datetime(temp_df.iloc[:, 0], format='%d-%m-%Y', dayfirst=True, errors='coerce')
            self.termini_df['Datum'] = datum_format1.fillna(datum_format2).fillna(datum_format3)

            if temp_df.shape[1] > 1:
                self.termini_df['Vrijeme'] = temp_df.iloc[:, 1]
            if temp_df.shape[1] > 2:
                self.termini_df['Usluga'] = temp_df.iloc[:, 2]
            if temp_df.shape[1] > 3:
                self.termini_df['Ime Korisnika'] = temp_df.iloc[:, 3]
            if temp_df.shape[1] > 4:
                self.termini_df['Tip Korisnik'] = temp_df.iloc[:, 4]

            self.termini_df = self.termini_df.dropna(subset=["Datum"])
            print("Sadržaj self.termini_df NAKON učitavanja:")
            print(self.termini_df)
            print("Tip podataka stupca 'Datum' u self.termini_df:", self.termini_df['Datum'].dtype)

        except FileNotFoundError:
            print("Datoteka 'termini.csv' nije pronađena.")
        except Exception as e:
            print(f"Došlo je do pogreške pri učitavanju termina: {e}")

    def prikazi_usluge(self, datum_odabran):
        self.lista_usluga.clear()
        odabrani_datum_str = datum_odabran.toString(Qt.ISODate) # Format YYYY-MM-DD

        try:
            filtrirani_termini_df = self.termini_df[self.termini_df['Datum'].dt.strftime('%Y-%m-%d') == odabrani_datum_str]

            if not filtrirani_termini_df.empty:
                for index, redak in filtrirani_termini_df.iterrows():
                    usluga = redak.iloc[2]
                    vrijeme = redak.iloc[1]
                    ime_korisnik = redak.iloc[3]
                    self.lista_usluga.addItem(f"{usluga} ({vrijeme}), {ime_korisnik}")
            else:
                self.lista_usluga.addItem("Nema usluga \nza ovaj datum.")
            self.ukloni_gumb.setEnabled(False)
            self.odabrani_termin_index_lista = None

        except AttributeError as e:
            print(f"Greška pri filtriranju DataFrame: {e}")
            self.lista_usluga.addItem("Došlo je do problema pri prikazu usluga.")

    def omoguci_gumb_ukloni(self, item):
        self.ukloni_gumb.setEnabled(True)
        self.odabrani_termin_index_lista = self.lista_usluga.row(item)

    def ukloni_termin(self):
        if self.odabrani_termin_index_lista is not None:
            odabrani_termin_tekst = self.lista_usluga.currentItem().text()
            usluga, ostalo = odabrani_termin_tekst.split(" (", 1)
            vrijeme = ostalo.split(")")[0]
            ime_korisnik = ostalo.split(", ")[1]

            indeksi_za_brisanje = self.termini_df[
                (self.termini_df['Usluga'] == usluga) &
                (self.termini_df['Vrijeme'] == vrijeme) &
                (self.termini_df['Ime Korisnika'] == ime_korisnik)
            ].index.tolist()

            if indeksi_za_brisanje:
                odgovor = QMessageBox.question(
                    self,
                    "Potvrda brisanja",
                    f"Jeste li sigurni da želite ukloniti termin: {odabrani_termin_tekst}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if odgovor == QMessageBox.Yes:
                    self.termini_df = self.termini_df.drop(indeksi_za_brisanje[0])
                    self.termini_df.to_csv("termini.csv", index=False, header=False, encoding='windows-1250')
                    self.ucitaj_termine()
                    self.prikazi_usluge(self.kalendar.selectedDate())
                    self.odabrani_termin_index_lista = None
                    self.ukloni_gumb.setEnabled(False)
            else:
                QMessageBox.warning(self, "Greška", "Nije moguće pronaći odgovarajući termin za brisanje.")
        else:
            QMessageBox.warning(self, "Upozorenje", "Molimo odaberite termin za uklanjanje.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = UpravljanjeTerminimaProzor()
    prozor.show()
    sys.exit(app.exec_())