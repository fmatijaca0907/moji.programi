import sys
import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QComboBox, QPushButton, QApplication, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont
import pandas as pd
import Dobrodosli

class IspisRacunaProzor(QWidget):
    def __init__(self, podaci_termina=None):
        super().__init__()
        self.setWindowTitle("Ispis računa")
        self.setGeometry(750, 350, 600, 400)
        self.setStyleSheet("background-color: #98FB98;")
        self.usluge_cijene = self._ucitaj_usluge_cijene()
        self.usluge = list(self.usluge_cijene.keys())
        self.putanja_racuna = "racuni.txt"
        self.podaci_termina = podaci_termina
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.usluga_label = QLabel("Odaberite uslugu:")
        font_label = QFont("Arial", 16)
        self.usluga_label.setFont(font_label)
        layout.addWidget(self.usluga_label, 0, 0)

        self.usluga_combo = QComboBox()
        font_combo = QFont("Arial", 14)
        self.usluga_combo.setFont(font_combo)
        self.usluga_combo.addItems(self.usluge)
        layout.addWidget(self.usluga_combo, 0, 1)
        self.usluga_combo.currentIndexChanged.connect(self._prikazi_racun)

        self.racun_label = QLabel("Račun:")
        font_racun_label = QFont("Arial", 16)
        self.racun_label.setFont(font_racun_label)
        layout.addWidget(self.racun_label, 1, 0)

        self.racun_text = QTextEdit()
        self.racun_text.setReadOnly(True)
        font_racun_text = QFont("Courier New", 12)
        self.racun_text.setFont(font_racun_text)
        layout.addWidget(self.racun_text, 2, 0, 1, 2)

        self.ispisi_button = QPushButton("Spremi račun")
        font_gumb = QFont("Arial", 14)
        self.ispisi_button.setFont(font_gumb)
        self.ispisi_button.setStyleSheet("""
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
        self.ispisi_button.clicked.connect(self._spremi_racun)
        layout.addWidget(self.ispisi_button, 3, 0, 1, 2)

        self.odjava_button = QPushButton("Odjava")
        font_odjava_gumb = QFont("Arial", 14)
        self.odjava_button.setFont(font_odjava_gumb)
        self.odjava_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f; /* Tamnija nijansa crvene */
            }
        """)
        self.odjava_button.clicked.connect(self.odjava)
        layout.addWidget(self.odjava_button, 4, 0, 1, 2)


        self.setLayout(layout)

    def _ucitaj_usluge_cijene(self):
        try:
            df_usluge = pd.read_csv("usluge.csv", encoding="utf-8", index_col='Usluga')['Cijena'].to_dict()
            return df_usluge
        except FileNotFoundError:
            QMessageBox.critical(self, "Greška", "Datoteka usluge.csv nije pronađena!")
            return {}
        except Exception as e:
            QMessageBox.critical(self, "Greška", f"Greška pri učitavanju usluge.csv: {e}")
            return {}

    def _prikazi_racun(self):
        if self.podaci_termina:
            datum = self.podaci_termina.get('Datum', 'N/A')
            vrijeme = self.podaci_termina.get('Vrijeme', 'N/A')
            usluga = self.podaci_termina.get('Usluga', self.usluga_combo.currentText())
        else:
            datum = datetime.date.today().strftime("%d-%m-%Y")
            vrijeme = datetime.datetime.now().strftime("%H:%M:%S")
            usluga = self.usluga_combo.currentText()

        cijena = self.usluge_cijene.get(usluga, "N/A")

        sadrzaj_racuna = f"------------------------\n"
        sadrzaj_racuna += f"Račun za termin:\n"
        sadrzaj_racuna += f"Datum: {datum}\n"
        sadrzaj_racuna += f"Vrijeme: {vrijeme}\n"
        sadrzaj_racuna += f"Usluga: {usluga}\n"
        sadrzaj_racuna += f"Cijena: {cijena}\n\n"

        self.racun_text.setText(sadrzaj_racuna)

    def _spremi_racun(self):
        if self.podaci_termina:
            datum = self.podaci_termina.get('Datum', 'N/A')
            vrijeme = self.podaci_termina.get('Vrijeme', 'N/A')
            usluga = self.podaci_termina.get('Usluga', self.usluga_combo.currentText())
        else:
            datum = datetime.date.today().strftime("%d-%m-%Y")
            vrijeme = datetime.datetime.now().strftime("%H:%M:%S")
            usluga = self.usluga_combo.currentText()

        cijena = self.usluge_cijene.get(usluga, "N/A")
        trenutni_datum_ispisa = datetime.date.today().strftime("%d-%m-%Y")
        trenutno_vrijeme_ispisa = datetime.datetime.now().strftime("%H:%M:%S")

        sadrzaj_racuna = f"------------------------\n"
        sadrzaj_racuna += f"Račun izdan:\n"
        sadrzaj_racuna += f"Datum ispisa: {trenutni_datum_ispisa}\n"
        sadrzaj_racuna += f"Vrijeme ispisa: {trenutno_vrijeme_ispisa}\n"
        sadrzaj_racuna += f"------------------------\n"
        sadrzaj_racuna += f"Detalji termina:\n"
        sadrzaj_racuna += f"Datum termina: {datum}\n"
        sadrzaj_racuna += f"Vrijeme termina: {vrijeme}\n"
        sadrzaj_racuna += f"Usluga: {usluga}\n"
        sadrzaj_racuna += f"Cijena: {cijena}\n\n"

        try:
            with open(self.putanja_racuna, 'a', encoding='utf-8') as file:
                file.write(sadrzaj_racuna)
            QMessageBox.information(self, "Račun spremljen", f"Račun je uspješno dodan u datoteku: {self.putanja_racuna}")
        except Exception as e:
            QMessageBox.critical(self, "Greška pri spremanju", f"Došlo je do pogreške prilikom dodavanja računa: {e}")

    def odjava(self):
        self.dobrodosli = Dobrodosli.DobrodosliProzor()
        self.dobrodosli.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = IspisRacunaProzor()
    prozor.show()
    sys.exit(app.exec_())