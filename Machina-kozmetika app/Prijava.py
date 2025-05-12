import sys
import csv
import hashlib
from PyQt5.QtWidgets import(QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import GlavniProzor

import main


class PrijavaProzor(QWidget):

    def __init__(self):
        super().__init__()
        self.status_label = QLabel()
        self.korisnicko_ime_label = QLabel("Unesi email:")
        self.korisnicko_ime_unos = QLineEdit()
        self.lozinka_label = QLabel("Lozinka:")
        self.lozinka_unos = QLineEdit()
        self.prijava_gumb = QPushButton("Prijavi se")
        self.natrag_gumb = QPushButton("Natrag")
        self.initUI()

    def initUI(self):

        #QWiddget
        self.setStyleSheet("background-color: #98FB98;")
        self.setGeometry(700, 300, 500, 500)


        #QLabel
        label_font = QFont("Arial", 20)
        self.korisnicko_ime_label.setFont(label_font)
        self.lozinka_label.setFont(label_font)

        status_font = QFont("Arial", 15)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)

        #QLineEdit
        self.lozinka_unos.setEchoMode(QLineEdit.Password)
        self.korisnicko_ime_unos.setStyleSheet("""
            QLineEdit {
                font-family: "Arial";
                font-size: 30px;
                color: #333333;
                background-color: #F0FFF0;
                border-radius: 5px;
            }
        """)
        self.lozinka_unos.setStyleSheet("""
            QLineEdit {
                font-family: "Arial";
                font-size: 30px;
                color: #333333;
                background-color: #F0FFF0;
                border-radius: 5px;
            }
        """)

        #PushButton
        gumb_font = QFont("Times New Roman", 14)
        self.prijava_gumb.setStyleSheet("background-color: #228B22; color: white; padding: 10px; border-radius: 5px;")
        self.prijava_gumb.setFont(gumb_font)
        self.natrag_gumb.setStyleSheet("background-color: #228B22; color: white; padding: 10px; border-radius: 5px;")
        self.natrag_gumb.setFont(gumb_font)
        self.prijava_gumb.clicked.connect(self.prijava_korinsika)
        self.natrag_gumb.clicked.connect(self.vrati_se)
        
        layout = QVBoxLayout()
        layout.addWidget(self.korisnicko_ime_label)
        layout.addWidget(self.korisnicko_ime_unos)
        layout.addWidget(self.lozinka_label)
        layout.addWidget(self.lozinka_unos)
        layout.addWidget(self.prijava_gumb)
        layout.addWidget(self.natrag_gumb)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def prijava_korinsika(self):
        korisnicko_ime = self.korisnicko_ime_unos.text().strip()
        lozinka_unos = self.lozinka_unos.text()

        if not korisnicko_ime:
            self.status_label.setText("Molimo unesite email.")
            return

        if not lozinka_unos:
            self.status_label.setText("Molimo unesite lozinku.")
            return

        pronaden_korisnik = None

        try:
            with open("sve_osobe.csv", 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for redak in reader:
                    if len(redak) == 6:
                        tip, ime, prezime, email, telefon, hashirana_lozinka = redak
                        if email == korisnicko_ime:
                            pronaden_korisnik = (email, hashirana_lozinka, tip, ime, prezime, telefon)
                            break
                    else:
                        pass
            if pronaden_korisnik:
                email_baza, hashirana_lozinka_baza, tip, ime, prezime, telefon = pronaden_korisnik
                hashirana_unos = hashlib.sha256(lozinka_unos.encode('utf-8')).hexdigest()
                if hashirana_unos == hashirana_lozinka_baza:
                    self.otvori_glavni_prozor(tip, ime, prezime, email, telefon)
                else:
                    self.status_label.setText("Pogrešna lozinka!")
            else:
                self.status_label.setText("Korisnik s tim emailom nije pronađen!")
        except FileNotFoundError:
            self.status_label.setText("Datoteka s korisnicima nije pronađena!")
        except Exception as e:
            self.status_label.setText(f"Došlo je do neočekivane greške: {e}")
            print(f"Došlo je do neočekivane greške: {e}")

    def otvori_glavni_prozor(self, tip, ime, prezime, email, telefon):
        self.glavni_prozor = GlavniProzor.GlavniProzor(tip,ime,prezime,email,telefon)
        self.glavni_prozor.show()
        self.close()

    def vrati_se(self):
        self.dobrodosli_prozor = main.Dobrodosli.DobrodosliProzor()
        self.dobrodosli_prozor.show()
        self.close() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = PrijavaProzor()
    prozor.show()
    sys.exit(app.exec_())