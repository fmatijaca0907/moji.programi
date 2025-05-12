import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QApplication,QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import RezervacijaProzor
import ProfilProzor
import Dobrodosli
import Uprava_termina
import Uredivanje_osoba
import PregeledRaspor
import IspisRacun

class GlavniProzor(QWidget):
    def __init__(self, tip, ime, prezime, email, telefon):
        super().__init__()
        self.tip = tip
        self.ime = ime
        self.prezime = prezime
        self.email = email
        self.telefon = telefon
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Glavni Prozor - {self.ime} ({self.tip})")
        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: #98FB98;")

        font_naslov = QFont("Arial", 24, QFont.Bold)
        font_pozdrav = QFont("Arial", 18)
        font_gumb = QFont("Arial", 14)
        font_studio = QFont("Script MT Bold", 24)

        naslov_label = QLabel("Dobrodošli!")
        naslov_label.setFont(font_naslov)
        naslov_label.setAlignment(Qt.AlignCenter)

        pozdrav_label = QLabel(f"Prijavljeni ste kao: {self.ime} ({self.tip})")
        pozdrav_label.setFont(font_pozdrav)
        pozdrav_label.setAlignment(Qt.AlignCenter)

        studio_label = QLabel("Studio Laura")
        studio_label.setFont(font_studio)
        studio_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        studio_label.setStyleSheet("color: #555555;")

        layout = QVBoxLayout()
        layout.addWidget(naslov_label)
        layout.addWidget(pozdrav_label)

        if self.tip == "Korisnik":
            layout.addSpacing(70)
            self.rezerviraj_button = QPushButton("Rezerviraj termin")
            self.rezerviraj_button.setFont(font_gumb)
            self.rezerviraj_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049; /* Tamnija nijansa zelene */
                }
            """)
            self.rezerviraj_button.clicked.connect(self.otvori_rezervacija_prozor)
            layout.addWidget(self.rezerviraj_button)

            self.profil_button = QPushButton("Prikaži profil")
            self.profil_button.setFont(font_gumb)
            self.profil_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049; /* Tamnija nijansa zelene */
                }
            """)
            self.profil_button.clicked.connect(self.otvori_profil_prozor)
            layout.addWidget(self.profil_button)

        elif self.tip == "Admin":
            layout.addSpacing(70)
            self.upravljanje_termina_button = QPushButton("Prikaz terminima")
            self.upravljanje_termina_button.setFont(font_gumb)
            self.upravljanje_termina_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049; /* Tamnija nijansa zelene */
                }
            """)
            self.upravljanje_termina_button.clicked.connect(self.otvori_upravu_termina)
            layout.addWidget(self.upravljanje_termina_button)

            self.upravljanje_korisnicima_button = QPushButton("Upravljanje osobama i administracija")
            self.upravljanje_korisnicima_button.setFont(font_gumb)
            self.upravljanje_korisnicima_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049; /* Tamnija nijansa zelene */
                }
            """)
            self.upravljanje_korisnicima_button.clicked.connect(self.otovori_uprava_korisnici)
            layout.addWidget(self.upravljanje_korisnicima_button)

        elif self.tip == "Zaposlenik":
            layout.addSpacing(70)
            self.pregled_rasporeda_button = QPushButton("Pregled rasporeda")
            self.pregled_rasporeda_button.setFont(font_gumb)
            self.pregled_rasporeda_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049; 
                }
            """)
            self.pregled_rasporeda_button.clicked.connect(self._otvori_pregled_rasporeda)
            layout.addWidget(self.pregled_rasporeda_button)

            self.evidentiranje_usluga_button = QPushButton("Ispis racuna")
            self.evidentiranje_usluga_button.setFont(font_gumb)
            self.evidentiranje_usluga_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049; 
                }
            """)
            self.evidentiranje_usluga_button.clicked.connect(self._otvori_ispis_racuna_prozor)
            layout.addWidget(self.evidentiranje_usluga_button)

        layout.addStretch(1)
        self.odjava_button = QPushButton("Odjavi se")
        self.odjava_button.setFont(font_gumb)
        self.odjava_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;}""")
        self.odjava_button.clicked.connect(self.odjava_korisnika)
        layout.addWidget(self.odjava_button)
        layout.addWidget(studio_label)

        self.setLayout(layout)

    def otvori_rezervacija_prozor(self):
        self.rezervacija_prozor = RezervacijaProzor.RezervacijaProzor(self.tip,self.ime,self.prezime,self.email,self.telefon)
        self.rezervacija_prozor.show()
        self.close()

    def otvori_profil_prozor(self):
        self.profil_prozor = ProfilProzor.ProfilProzor(self.ime,self.prezime,self.email,self.telefon,self.tip)
        self.profil_prozor.show()
        self.close()

    def odjava_korisnika(self):
        self.dobro_dosli = Dobrodosli.DobrodosliProzor()
        self.dobro_dosli.show()
        self.close()
    
    def otvori_upravu_termina(self):
        self.upravljanje = Uprava_termina.UpravljanjeTerminimaProzor()
        self.upravljanje.show()
        self.close()

    def otovori_uprava_korisnici(self):
        self.uprava_korisnici = Uredivanje_osoba.UpravljanjeKorisnicimaProzor()
        self.uprava_korisnici.show()
        self.close()

    def _otvori_pregled_rasporeda(self): 
        self.pregled_rasporeda_prozor = PregeledRaspor.PregledRasporedaProzor()
        self.pregled_rasporeda_prozor.show()
        self.close()
    def _otvori_ispis_racuna_prozor(self):
        self.ispis_racuna_prozor = IspisRacun.IspisRacunaProzor()
        self.ispis_racuna_prozor.show()
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = GlavniProzor()
    prozor.show()
    sys.exit(app.exec_())