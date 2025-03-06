def lista_slova() -> list:
    """
    Function that generates a list of letters
    """
    lista_slovo = []
    slova = "ABCDEFGHIJKLMNOPQRSTUWZ"
    for slovo in slova:
        lista_slovo.append(slovo)
    return lista_slovo

def broj_znakova() -> int:
    """
    Function that asks the user to input the number of digits
    """
    broj_znamkeni = int(input("Unesi broj znamekni"))
    return broj_znamkeni

def nasumicna_lista_s() -> list:
    """
    Function that takes a list of letters and generates a random list
    """
    random_lista = []
    lista = lista_slova()
    import random
    for slovo in lista:
        slovo = random.choice(lista)
        random_lista.append(slovo)

    return random_lista

def lista_brojeva() -> list:
    """
    Function that generates a list of numbers
    """
    lista_b=[]
    brojevi = "0123456789"
    for broj in brojevi:
        lista_b.append(broj)
    return lista_b

def nasumicna_lista_b() -> list:
    """
    Function that takes a list of numbers and generates a random list
    """
    nasumicna =[]
    lista = lista_brojeva()
    import random
    for slovo in lista:
        slovo = random.choice(lista)
        nasumicna.append(slovo)

    return nasumicna

def lista_b_s() -> list:
    """
    Function that joins a list of numbers and a list of letters
    """
    lista_b = nasumicna_lista_b()
    lista_s=nasumicna_lista_s()
    lista = lista_b + lista_s
    return lista

def nasumicna_sifra() -> list:
    """
    Function that takes a list of numbers and letters and create a random list
    """
    sifra = []
    b_znakova = broj_znakova()
    lista = lista_b_s()
    import random
    for x in range(b_znakova):
        slovo = random.choice(lista)
        sifra.append(slovo)
    return sifra

def nasumicna_sifra_str() -> str:
    """
    Function that takes a random list and converts it to a string
    """
    lista = nasumicna_sifra()
    sifra = "".join(lista)
    return sifra