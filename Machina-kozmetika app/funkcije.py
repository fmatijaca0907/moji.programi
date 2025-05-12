import csv

def spremi_csv(lista):
    with open("sve_osobe.csv","a") as csv_file:
        writer = csv.writer(csv_file)
        zaglavlje = ["Tip", "Ime", "Prezime", "Email", "Telefon", "Lozinka"]
        writer.writerow(zaglavlje)
        for objekt in lista:
            writer.writerow(objekt.podaci_za_csv())