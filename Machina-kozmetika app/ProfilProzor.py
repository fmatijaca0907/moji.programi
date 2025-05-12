from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout,QGroupBox,QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import csv

class ProfilProzor(QWidget):
    def __init__(self, ime, prezime, email, telefon, tip):
        super().__init__()
        self.ime = ime
        self.prezime = prezime
        self.email = email
        self.telefon = telefon
        self.tip = tip
        self.setWindowTitle("Profil")
        self.setGeometry(850, 450, 500, 500)
        self.setStyleSheet("background-color: #98FB98; font-family: 'Times New Roman';")
        self.initUI()

    def initUI(self):
        self.initWidgets()
        self.initLayout()
        self.prikazi_rezervacije()

    def initWidgets(self):
        self.naslov_font = QFont("Arial", 18, QFont.Bold)
        self.label_font = QFont("Arial", 12)
        self.podatak_font = QFont("Arial", 12)
        self.rezervacija_naslov_font = QFont("Arial", 14, QFont.Bold)
        self.rezervacija_info_font = QFont("Arial", 11)
        self.prazno_font = QFont("Arial", 11,)
        self.greska_font = QFont("Arial", 11,)

        self.naslov_label = self._create_label("Profil", self.naslov_font, Qt.AlignCenter)

        self.osobni_podaci_group = self.create_osobni_podatci()
        self.rezervacije_group, self.rezervacije_layout_inner = self.create_rezervacije_group()

    def initLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.naslov_label)
        layout.addWidget(self.osobni_podaci_group)
        layout.addWidget(self.rezervacije_group)
        self.setLayout(layout)


    def _create_label(self, text, font=None, alignment=Qt.AlignLeft):
        label = QLabel(text)
        if font:
            label.setFont(font)
        label.setAlignment(alignment)
        return label

    def create_osobni_podatci(self):
        group = QGroupBox("Osobni podaci")
        layout = QGridLayout()

        layout.addWidget(self._create_label("Ime:", self.label_font), 0, 0)
        layout.addWidget(self._create_label(self.ime, self.podatak_font), 0, 1)

        layout.addWidget(self._create_label("Prezime:", self.label_font), 1, 0)
        layout.addWidget(self._create_label(self.prezime, self.podatak_font), 1, 1)

        layout.addWidget(self._create_label("Email:", self.label_font), 2, 0)
        layout.addWidget(self._create_label(self.email, self.podatak_font), 2, 1)

        layout.addWidget(self._create_label("Telefon:", self.label_font), 3, 0)
        layout.addWidget(self._create_label(self.telefon, self.podatak_font), 3, 1)

        layout.addWidget(self._create_label("Tip korisnika:", self.label_font), 4, 0)
        layout.addWidget(self._create_label(self.tip, self.podatak_font), 4, 1)

        group.setLayout(layout)
        return group

    def create_rezervacije_group(self):
        group = QGroupBox("Moje rezervacije")
        layout_inner = QVBoxLayout()
        group.setLayout(layout_inner)
        return group, layout_inner

    def prikazi_rezervacije(self):
        try:
            with open('termini.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                preskoci_zaglavlje = True
                ima_rezervacija = False
                for redak in reader:
                    if preskoci_zaglavlje:
                        preskoci_zaglavlje = False
                        continue
                    datum, vrijeme, usluga, ime_korisnik, tip_korisnik = redak
                    if ime_korisnik == self.ime:
                        rezervacija_info = f"Datum: {datum}, Vrijeme: {vrijeme}, Usluga: {usluga}"
                        label_rezervacija = self._create_label(rezervacija_info, self.rezervacija_info_font)
                        self.rezervacije_layout_inner.addWidget(label_rezervacija)
                        ima_rezervacija = True

                if not ima_rezervacija:
                    nema_rezervacija_label = self._create_label("Nemate aktivnih rezervacija.", self.prazno_font)
                    self.rezervacije_layout_inner.addWidget(nema_rezervacija_label)

            self.rezervacije_group.setLayout(self.rezervacije_layout_inner)

        except FileNotFoundError:
            nema_datoteke_label = self._create_label("Datoteka s terminima nije pronađena.", self.greska_font)
            self.rezervacije_layout_inner.addWidget(nema_datoteke_label)
            self.rezervacije_group.setLayout(self.rezervacije_layout_inner)
        except Exception as e:
            greska_label = self._create_label(f"Došlo je do pogreške pri učitavanju rezervacija: {e}", self.greska_font)
            self.rezervacije_layout_inner.addWidget(greska_label)
            self.rezervacije_group.setLayout(self.rezervacije_layout_inner)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = ProfilProzor("TestIme", "TestPrezime", "test@email.com", "0123456789", "TestTip")
    prozor.show()
    sys.exit(app.exec_())