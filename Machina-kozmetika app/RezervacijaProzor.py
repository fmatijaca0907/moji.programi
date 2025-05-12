import sys
import csv
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QApplication, QCalendarWidget, QComboBox, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
import GlavniProzor

class RezervacijaProzor(QWidget):
    def __init__(self, tip_korisnika, ime_korisnika, prezime_korisnika, email_korisnika, telefon_korisnika):
        self.tip_korisnika = tip_korisnika
        self.ime_korisnika = ime_korisnika
        self.prezime_korisnika = prezime_korisnika
        self.email = email_korisnika
        self.telefon_korisnika = telefon_korisnika
        super().__init__()
        self.setWindowTitle("Rezervacija termina")
        self.setStyleSheet("background-color: #98FB98;")
        self.postojece_rezervacije = {} 
        self._ucitaj_rezervacije() 
        self.initUI()

    def _ucitaj_rezervacije(self):
        try:
            with open('termini.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if len(row) >= 2:
                        datum_str, vrijeme, *ostalo = row
                        try:
                            # Pokušajte parsirati datum u formatu YYYY-MM-DD
                            date_obj = QDate.fromString(datum_str, "yyyy-MM-dd")
                            formatirani_datum = date_obj.toString("dd-MM-yyyy")
                            if formatirani_datum not in self.postojece_rezervacije:
                                self.postojece_rezervacije[formatirani_datum] = []
                            self.postojece_rezervacije[formatirani_datum].append(vrijeme)
                        except:
                            try:
                                # Pokušajte parsirati datum u formatu DD-MM-YYYY (ako je datoteka tako spremljena)
                                date_obj = QDate.fromString(datum_str, "dd-MM-yyyy")
                                formatirani_datum = date_obj.toString("dd-MM-yyyy")
                                if formatirani_datum not in self.postojece_rezervacije:
                                    self.postojece_rezervacije[formatirani_datum] = []
                                self.postojece_rezervacije[formatirani_datum].append(vrijeme)
                            except Exception as e:
                                print(f"Greška pri parsiranju datuma: {e}, redak: {row}")
        except FileNotFoundError:
            self.postojece_rezervacije = {}
        except Exception as e:
            QMessageBox.critical(self, "Greška", f"Došlo je do greške pri učitavanju rezervacija: {e}")
            self.postojece_rezervacije = {}

    def initUI(self):
        self.initWidgets()
        self.initLayout()

        self.kalendar.clicked.connect(self._azuriraj_dostupna_vremena) 
        self.vrijeme_combo.currentIndexChanged.connect(self.anzuriraj_rez)
        self.usluga_combo.currentIndexChanged.connect(self.anzuriraj_rez)
        self.potvrdi_gumb.clicked.connect(self.spremi_rezervaciju)
        self.anzuriraj_rez()

    def initWidgets(self):
        font_naslov = QFont("Times New Roman", 25, QFont.Bold)
        font_label = QFont("Times New Roman", 18)
        font_info = QFont("Times New Roman", 12)

        self.naslov_label = QLabel("Odaberite datum, vrijeme i uslugu")
        self.naslov_label.setFont(font_naslov)
        self.naslov_label.setAlignment(Qt.AlignCenter)

        self.ime_korisnika_label = QLabel(f"Ime: {self.ime_korisnika}({self.tip_korisnika})")
        self.ime_korisnika_label.setFont(font_info)
        self.ime_korisnika_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.datum_label = QLabel("Izaberi datum:")
        self.datum_label.setFont(font_label)

        self.odabrano_label = QLabel("Odabrano: ")
        self.odabrano_label.setFont(font_label)
        self.odabrano_label.setAlignment(Qt.AlignCenter)

        self.kalendar = QCalendarWidget(self)
        self.kalendar.setStyleSheet("background-color: #98FB98; color: #333;")

        self.vrijeme_label = QLabel("Izaberi vrijeme:")
        self.vrijeme_label.setFont(font_label)

        self.vrijeme_combo = QComboBox(self)
        self.vrijeme_combo.setMaxVisibleItems(5)
        self.vrijeme_combo.setStyleSheet("""
            QComboBox {
                background-color: #F0FFF0;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                font-size: 20px;
            }
        """)
        self._popuni_vrijeme_combo()

        self.usluga_label = QLabel("Izaberi usluga:")
        self.usluga_label.setFont(font_label)
        self.usluga_combo = QComboBox(self)
        self.usluga_combo.addItems(["-", "Bojanje", "Manikura", "Pedikura"])
        self.usluga_combo.setStyleSheet("""
            QComboBox {
                background-color: #F0FFF0;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                font-size: 20px;
            }
        """)
        self.potvrdi_gumb = QPushButton("Potvrdi")
        self.potvrdi_gumb.setEnabled(False)
        self.potvrdi_gumb.setStyleSheet("""
            QPushButton {
                background-color: #228B22;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 20px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def initLayout(self):
        layout = QGridLayout()

        layout.addWidget(self.ime_korisnika_label, 1, 0, alignment=Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.naslov_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        layout.addWidget(self.kalendar, 2, 0)

        vrijeme_usluga_layout = QVBoxLayout()
        vrijeme_usluga_layout.addWidget(self.vrijeme_label)
        vrijeme_usluga_layout.addWidget(self.vrijeme_combo)
        vrijeme_usluga_layout.addSpacing(35)
        vrijeme_usluga_layout.addWidget(self.usluga_label)
        vrijeme_usluga_layout.addWidget(self.usluga_combo)
        layout.addLayout(vrijeme_usluga_layout, 2, 1, alignment=Qt.AlignTop)
        layout.addWidget(self.odabrano_label, 3, 0, 1, 2, alignment=Qt.AlignCenter)
        layout.addWidget(self.potvrdi_gumb, 4, 0, 1, 2)

        layout.setHorizontalSpacing(25)
        self.setLayout(layout)

    def _popuni_vrijeme_combo(self):
        self.vrijeme_combo.clear()
        self.vrijeme_combo.addItem("-")
        for i in range(13):
            sat = (i + 8)
            self.vrijeme_combo.addItem(f"{sat}:00")
            self.vrijeme_combo.addItem(f"{sat}:30")

    def _azuriraj_dostupna_vremena(self, date):
        odabrani_datum_str = date.toString("dd-MM-yyyy")
        print(f"Odabrani datum: {odabrani_datum_str}")
        print(f"Postojeće rezervacije: {self.postojece_rezervacije}")
        self._popuni_vrijeme_combo()
        if odabrani_datum_str in self.postojece_rezervacije:
            print(f"Pronađene rezervacije za {odabrani_datum_str}: {self.postojece_rezervacije[odabrani_datum_str]}")
            rezervirana_vremena = self.postojece_rezervacije[odabrani_datum_str]
            for vrijeme in rezervirana_vremena:
                print(f"Pokušavam ukloniti vrijeme: {vrijeme}")
                index_za_ukloniti = self.vrijeme_combo.findText(vrijeme)
                print(f"Indeks za ukloniti: {index_za_ukloniti}")
                if index_za_ukloniti != -1:
                    self.vrijeme_combo.removeItem(index_za_ukloniti)
                    print(f"Vrijeme {vrijeme} je uklonjeno.")
                else:
                    print(f"Vrijeme {vrijeme} nije pronađeno u combo boxu.")
        else:
            print(f"Nema rezervacija za {odabrani_datum_str}.")
        self.anzuriraj_rez()

    def anzuriraj_rez(self):
        odabrani_datum = self.kalendar.selectedDate()
        danasnji_datum = QDate.currentDate()
        vrijeme = self.vrijeme_combo.currentText()
        usluga = self.usluga_combo.currentText()

        if odabrani_datum < danasnji_datum:
            self.odabrano_label.setText("Datum ne može biti u prošlosti")
            self.potvrdi_gumb.setEnabled(False)
        elif vrijeme == "-" or usluga == "-":
            self.odabrano_label.setText("Molimo odaberite vrijeme i uslugu")
            self.potvrdi_gumb.setEnabled(False)
        else:
            datum_formatiran = odabrani_datum.toString("dd-MM-yyyy")
            self.odabrano_label.setText(f"Odabrano: {datum_formatiran}, {vrijeme}, {usluga}")
            self.potvrdi_gumb.setEnabled(True)

    def spremi_rezervaciju(self):
        odabrani_datum = self.kalendar.selectedDate().toString("dd-MM-yyyy")
        vrijeme = self.vrijeme_combo.currentText()
        usluga = self.usluga_combo.currentText()
        ime_korisnika = self.ime_korisnika
        tip_korisnika = self.tip_korisnika

        try:
            with open('termini.csv', 'a', newline='',encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([odabrani_datum, vrijeme, usluga, ime_korisnika, tip_korisnika])
            print("Datoteka zatvorena (unutar try):", csvfile.closed)
            QMessageBox.information(self, "Uspjeh", "Rezervacija je uspješno spremljena.")
            self.optvori_galvni()
        except Exception as e:
            QMessageBox.critical(self, "Greška", f"Došlo je do greške pri spremanju rezervacije: {e}")
        finally:
            print("Datoteka zatvorena (finally):", csvfile.closed if 'csvfile' in locals() else 'csvfile nije definirana')
    def optvori_galvni(self):
        self.glavni_prozor = GlavniProzor.GlavniProzor(self.tip_korisnika, self.ime_korisnika, self.prezime_korisnika, self.email, self.telefon_korisnika)
        self.glavni_prozor.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = RezervacijaProzor("Korisnik","Neto","Neki","Neki@","9834983")
    prozor.show()
    sys.exit(app.exec_())