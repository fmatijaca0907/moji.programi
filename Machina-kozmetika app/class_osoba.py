import hashlib

class Osoba:
    
    def __init__(self,ime,prezime,email,telefon,lozinka):
        self.ime = ime
        self.prezime = prezime
        self.email = self.provjeri_mail(email)
        self.telefon = telefon
        self.lozinka = self.napravi_lozinku(lozinka)
        self.tip = "Osoba"

    def provjeri_mail(self,email):
        if "@" in email and "." in email:
            return email
        else:
            raise ValueError("Email nije dobar")
        
    def napravi_lozinku(self,lozinka):
        lozinka = lozinka.encode("utf-8")
        sifra =  hashlib.sha256(lozinka)
        heksadecimalni_hash = sifra.hexdigest()
        return heksadecimalni_hash

    def podaci_za_csv(self):
        return[self.tip,self.ime,self.prezime,self.email,self.telefon,self.lozinka]

class Zaposlenik(Osoba):

    def __init__(self, ime, prezime, email, telefon,lozinka):
        super().__init__(ime, prezime, email, telefon,lozinka)
        self.tip = "Zaposlenik"

class Korisnik(Osoba):

    def __init__(self, ime, prezime, email, telefon,lozinka):
        super().__init__(ime, prezime, email, telefon,lozinka)
        self.tip = "Korisnik"

class Administrator(Osoba):

    def __init__(self, ime, prezime, email, telefon,lozinka):
        super().__init__(ime, prezime, email, telefon,lozinka)
        self.tip = "Admin"
