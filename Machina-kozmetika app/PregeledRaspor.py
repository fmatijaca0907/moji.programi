import sys
import os
import csv
import datetime
from PyQt5.QtWidgets import QWidget, QTableView, QGridLayout, QLabel, QPushButton, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
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

class PregledRasporedaProzor(QWidget):
    def __init__(self):
        super().__init__()
        self.termini_df = pd.DataFrame()
        self.tablica_view = QTableView()
        self.odabrani_redak_label = QLabel("Odabrano: ")
        self.ispisi_racun_button = QPushButton("Ispiši račun")
        self.trenutno_odabrani_indeks = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pregled rasporeda")
        self.setGeometry(850, 450, 600, 500)
        self.setStyleSheet("background-color: #98FB98;")
        self._init_layout()
        self._ucitaj_termine()
        self.tablica_view.clicked.connect(self._prikazi_odabrani_redak)
        self.ispisi_racun_button.clicked.connect(self._spremi_racun_u_datoteku)

    def _init_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.tablica_view, 0, 0)
        layout.addWidget(self.odabrani_redak_label, 1, 0)
        layout.addWidget(self.ispisi_racun_button, 2, 0)
        self.setLayout(layout)

    def _ucitaj_termine(self):
        try:
            self.termini_df = pd.read_csv("termini.csv", encoding="latin-1", header=None, names=['Datum', 'Vrijeme', 'Usluga', 'Ime', 'Tip'])
            self.termini_df['Datum_Vrijeme'] = pd.to_datetime(self.termini_df['Datum'] + ' ' + self.termini_df['Vrijeme'], format='mixed', dayfirst=True, errors='coerce')
            self.termini_df = self.termini_df.sort_values(by='Datum_Vrijeme')
            self.termini_df = self.termini_df.dropna(subset=['Datum_Vrijeme']) # Ukloni retke s nevažećim datumima

            try:
                usluge_df = pd.read_csv("usluge.csv", encoding="utf-8")
                self.termini_df = pd.merge(self.termini_df, usluge_df, on='Usluga', how='left')
            except FileNotFoundError:
                print("Datoteka usluge.csv nije pronađena. Cijene neće biti prikazane.")
                self.termini_df['Cijena'] = None
            except Exception as e:
                print(f"Greška pri učitavanju usluge.csv: {e}")
                self.termini_df['Cijena'] = None

            stupci_za_prikaz = ['Datum', 'Vrijeme', 'Usluga', 'Ime', 'Cijena']
            self.termini_df = self.termini_df[stupci_za_prikaz]
            model = PandasModel(self.termini_df)
            self.tablica_view.setModel(model)

        except FileNotFoundError:
            print("Datoteka termini.csv nije pronađena.")
            self.termini_df = pd.DataFrame()
        except Exception as e:
            print(f"Greška pri učitavanju termini.csv: {e}")

    def _prikazi_odabrani_redak(self, index: QModelIndex):
        odabrani_redak = self.termini_df.iloc[index.row()]
        prikaz_retka = ", ".join(str(value) for value in odabrani_redak.values)
        self.odabrani_redak_label.setText(f"Odabrano: {prikaz_retka}")
        self.trenutno_odabrani_indeks = index

    def _spremi_racun_u_datoteku(self):
        if self.trenutno_odabrani_indeks is not None:
            odabrani_redak = self.termini_df.iloc[self.trenutno_odabrani_indeks.row()]
            trenutni_datum = datetime.date.today().strftime("%d-%m-%Y")
            trenutno_vrijeme = datetime.datetime.now().strftime("%H:%M:%S")
            usluga = odabrani_redak['Usluga']
            ime = odabrani_redak['Ime']
            cijena = odabrani_redak.get('Cijena', 'N/A')
            sadrzaj_racuna = "---------------------\n"
            sadrzaj_racuna += f"Račun za termin:\n"
            sadrzaj_racuna += f"Datum: {trenutni_datum}\n"
            sadrzaj_racuna += f"Vrijeme: {trenutno_vrijeme}\n"
            sadrzaj_racuna += f"Usluga: {usluga}\n"
            sadrzaj_racuna += f"Ime: {ime}\n"
            sadrzaj_racuna += f"Cijena: {cijena}\n"

            putanja_racuna = "racuni.txt"
            try:
                with open(putanja_racuna, 'a', encoding='utf-8') as file:
                    file.write(sadrzaj_racuna)
                QMessageBox.information(self, "Račun spremljen", f"Račun je uspješno spremljen u datoteku: {putanja_racuna}")
                self._obradi_rijeseni_termin(odabrani_redak)
            except Exception as e:
                QMessageBox.critical(self, "Greška pri spremanju", f"Došlo je do pogreške prilikom spremanja računa: {e}")
        else:
            QMessageBox.warning(self, "Nema odabranog termina", "Molimo odaberite termin za ispis računa.")

    def _obradi_rijeseni_termin(self, termin_za_obradu):
        rijeseni_termini_file = "rijeseni_termini.csv"
        termin_postoji = False

        try:
            rijeseni_df = pd.read_csv(rijeseni_termini_file, encoding="latin-1", header=None, names=['Datum', 'Vrijeme', 'Usluga', 'Ime'])
            uvjet = (rijeseni_df['Datum'] == termin_za_obradu['Datum']) & \
                    (rijeseni_df['Vrijeme'] == termin_za_obradu['Vrijeme']) & \
                    (rijeseni_df['Usluga'] == termin_za_obradu['Usluga']) & \
                    (rijeseni_df['Ime'] == termin_za_obradu['Ime'])
            if uvjet.any():
                termin_postoji = True
        except Exception as e:
            print(f"Greška pri čitanju rijeseni_termini.csv: {e}")

        if not termin_postoji:
            try:
                with open(rijeseni_termini_file, 'a', encoding='latin-1', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([termin_za_obradu['Datum'], termin_za_obradu['Vrijeme'], termin_za_obradu['Usluga'], termin_za_obradu['Ime']])
                self._ukloni_termin(termin_za_obradu)
            except Exception as e:
                print(f"Greška pri pisanju u rijeseni_termini.csv: {e}")
                QMessageBox.critical(self, "Greška", f"Došlo je do pogreške prilikom zapisivanja riješenog termina.")
        else:
            QMessageBox.warning(self, "Termin već riješen", "Ovaj termin je već označen kao riješen.")

    def _ukloni_termin(self, termin_za_uklanjanje):
        print("Počinjem uklanjanje termina...")
        try:
            svi_termini_df = pd.read_csv("termini.csv", encoding="latin-1", header=None, names=['Datum', 'Vrijeme', 'Usluga', 'Ime', 'Tip'])
            maska = (svi_termini_df['Datum'] != termin_za_uklanjanje['Datum']) | \
                    (svi_termini_df['Vrijeme'] != termin_za_uklanjanje['Vrijeme']) | \
                    (svi_termini_df['Usluga'] != termin_za_uklanjanje['Usluga']) | \
                    (svi_termini_df['Ime'] != termin_za_uklanjanje['Ime'])
            azurirani_termini_df = svi_termini_df[maska]
            print(f"Nakon filtriranja ostalo {len(azurirani_termini_df)} redaka")
            azurirani_termini_df.to_csv("termini.csv", encoding="latin-1", header=False, index=False)
            print("termini.csv je prepisan")
            self._ucitaj_termine()
            print("Termini su ponovno učitani")
        except FileNotFoundError:
            print("Datoteka termini.csv nije pronađena prilikom pokušaja uklanjanja termina.")
            QMessageBox.critical(self, "Greška", "Datoteka termini.csv nije pronađena.")
        except Exception as e:
            print(f"Greška pri uklanjanju termina iz termini.csv: {e}")
            QMessageBox.critical(self, "Greška", f"Došlo je do pogreške prilikom uklanjanja termina: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = PregledRasporedaProzor()
    prozor.show()
    sys.exit(app.exec_())