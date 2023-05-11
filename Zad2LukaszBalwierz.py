import sqlite3
from tabulate import tabulate

# utworzenie połączenia z bazą
db = sqlite3.connect("test")

# utworzenie obiektu kursora
kursor = db.cursor()

# # utworzenie tabeli "wyniki"
# kursor.execute('''
#
#     CREATE TABLE wyniki (
#     id integer primary key autoincrement,
#     imie string,
#     nazwisko string,
#     wynik integer,
#     ocena string)
#
# ''')

# Funkcja dodająca rekord do tabeli. Pobiera od użytkownia imie, nazwisko, oraz wynik.
# Sprawdza poprawność wprowadzonych danych i na podstawie wyniku oblicza ocenę.
def DodajRekord():
    try:
        imie = str(input("Imie: "))
        nazwisko = str(input("Nazwisko: "))
        wynik = int(input("Wynik: "))
        if wynik > 100:
            print('Wprowadzono zla wartosc!')

        wprowadzone_dane = {
            'Imie': imie,
            'Nazwisko': nazwisko,
            'Wynik': wynik
        }

        def sprawdzOcene(wynik):
            if wynik >= 90:
                return 5
            elif wynik >= 80:
                return 4
            elif wynik >= 70:
                return 3.5
            elif wynik >= 60:
                return 3
            else:
                return 2

        ocena = sprawdzOcene(wynik)
        wprowadzone_dane["Ocena"] = ocena

        kursor.execute('''

            INSERT INTO wyniki
            (id, imie, nazwisko, wynik, ocena)
            VALUES (NULL, '{}', '{}', '{}', '{}');

        '''.format(imie, nazwisko, wynik, ocena))

        print('---------------------')
        print("Pomyslnie wprowadzonono dane do tabeli.")
        print('---------------------')

        for dane in wprowadzone_dane:
            print(dane, ':', wprowadzone_dane[dane])

        print('---------------------')

    except ValueError:
        print("Wprowadzono zla wartosc!")

# Funkcja odczytująca dane z tabeli.
def OdczytajRekord():
    print("Jakie dane wyswietlic?")
    print('---------------------')
    print("Wszystkie - wpisz all")

    oceny = ['2', '3', '3,5', '4', '5']

    for ocena in oceny:
        print(f"Osoby, ktore uzyskaly ocene : {ocena}")
    r = input("INPUT: ")

    # odczytanie wszystkich danych w bazie
    if r == "all":
        print('---------------------')
        print("Wszystkie dane w bazie:")

        kursor.execute('''

                SELECT * 
                from wyniki;
        ''')

        wyswietlone_dane = kursor.fetchall()
        pierwszy_wiersz = ['id', 'imie', 'nazwisko', 'wynik', 'ocena']
        wyswietlone_dane.insert(0, pierwszy_wiersz)
        print(tabulate(wyswietlone_dane, headers='firstrow', tablefmt='fancy_grid'))

        kursor.execute('''

                SELECT count(*) 
                from wyniki;
        ''')

        ilosc_wierszy = kursor.fetchone()
        print("Ilość wierszy: ", ilosc_wierszy[0])

    # odczytanie danych po konkretnej wartosci(ocenie)
    elif r in oceny:
        print('---------------------')
        print(f"OSOBY Z OCENA {r}:")

        kursor.execute('''

                SELECT * 
                from wyniki where ocena = {};
        '''.format(r))

        wyswietlone_dane = kursor.fetchall()
        pierwszy_wiersz = ['id', 'imie', 'nazwisko', 'wynik', 'ocena']
        wyswietlone_dane.insert(0, pierwszy_wiersz)
        print(tabulate(wyswietlone_dane, headers='firstrow', tablefmt='fancy_grid'))

        kursor.execute('''

                SELECT count(*) 
                from wyniki where ocena = {};
        '''.format(r))

        ilosc_wierszy = kursor.fetchone()
        print("Ilość wierszy: ", ilosc_wierszy[0])
        print('---------------------')

    else:
        print("Wprowadzono zła wartosc. \n Sprobuj ponownie.")


def AktualizujRekord():
    print('---------------------')
    print("Wszystkie dane w bazie:")

    kursor.execute('''

            SELECT * 
            from wyniki;
    ''')

    wyswietloneDane = kursor.fetchall()
    pierwszy_wiersz = ['id', 'imie', 'nazwisko', 'wynik', 'ocena']
    wyswietloneDane.insert(0, pierwszy_wiersz)
    print(tabulate(wyswietloneDane, headers='firstrow', tablefmt='fancy_grid'))

    try:
        id_s = []
        for _ in wyswietloneDane:
            id_s = [tup[0] for tup in wyswietloneDane]

        id_s.pop(0)
        print(id_s)

        id_aktualizowanego_wiersza = int(input("Podaj id wiersza ktory chcesz aktualizowac: "))

        if id_aktualizowanego_wiersza not in id_s:
            raise ValueError(f"Brak studenta z takim id : {id_aktualizowanego_wiersza}")

        nowe_imie = str(input("Imie: "))
        nowe_nazwisko = str(input("Nazwisko: "))
        nowy_wynik = int(input("Wynik: "))
        if nowy_wynik > 100:
            print('Wprowadzono zla wartosc!')

        wprowadzone_dane_nowe = {
            'Imie': nowe_imie,
            'Nazwisko': nowe_nazwisko,
            'Wynik': nowy_wynik
        }

        def sprawdzOcene(nowy_wynik):
            if nowy_wynik >= 90:
                return 5
            elif nowy_wynik >= 80:
                return 4
            elif nowy_wynik >= 70:
                return 3.5
            elif nowy_wynik >= 60:
                return 3
            else:
                return 2

        nowaOcena = sprawdzOcene(nowy_wynik)
        wprowadzone_dane_nowe["Ocena"] = nowaOcena

        kursor.execute('''

                UPDATE wyniki SET imie = ?, nazwisko = ?, wynik = ?, ocena = ? WHERE id = ?;

        ''', (nowe_imie, nowe_nazwisko, nowy_wynik, nowaOcena, id_aktualizowanego_wiersza))

        print("Wiersz po aktualizacji:")

        kursor.execute('''

                SELECT * from wyniki
                WHERE id = {};

        '''.format(id_aktualizowanego_wiersza))

        wyswietloneDane = kursor.fetchall()
        pierwszy_wiersz = ['id', 'imie', 'nazwisko', 'wynik', 'ocena']
        wyswietloneDane.insert(0, pierwszy_wiersz)
        print(tabulate(wyswietloneDane, headers='firstrow', tablefmt='fancy_grid'))

    except ValueError:
        print('---------------------')
        print("Wprowadzono zla wartosc")
        print('---------------------')

# Funkcja usuwająca rekord z tabeli
def UsunRekord():
    print('---------------------')
    print("Wszystkie dane w bazie:")

    kursor.execute('''

            SELECT * 
            from wyniki;
            
    ''')

    wyswietlone_dane = kursor.fetchall()
    pierwszy_wiersz = ['id', 'imie', 'nazwisko', 'wynik', 'ocena']
    wyswietlone_dane.insert(0, pierwszy_wiersz)
    print(tabulate(wyswietlone_dane, headers='firstrow', tablefmt='fancy_grid'))

    try:
        id_s = []
        for _ in wyswietlone_dane:
            id_s = [tup[0] for tup in wyswietlone_dane]

        id_s.pop(0)
        print(id_s)

        id_usuwanego_wiersza = int(input("Podaj id wiersza ktory chcesz usunac: "))

        if id_usuwanego_wiersza not in id_s:
            raise ValueError(f"Brak studenta z takim id : {id_usuwanego_wiersza}")

        print("Usuwany rekord to:")

        kursor.execute('''

                SELECT * 
                from wyniki where id = {};

        '''.format(id_usuwanego_wiersza))

        wyswietlone_dane = kursor.fetchall()
        pierwszy_wiersz = ['id', 'imie', 'nazwisko', 'wynik', 'ocena']
        wyswietlone_dane.insert(0, pierwszy_wiersz)
        print(tabulate(wyswietlone_dane, headers='firstrow', tablefmt='fancy_grid'))

        kursor.execute('''

                DELETE from wyniki where id = {}

        '''.format(id_usuwanego_wiersza))

    except ValueError:
        print('---------------------')
        print("Wprowadzono zla wartosc")
        print('---------------------')


while True:
    dozwolone_znaki = ['c', 'r', 'u', 'd', 'x']

    print("Wprowadzic dane - 'c' (create) ")
    print("Wyswietlic dane - 'r' (read) ")
    print("Modyfikowac dane- 'u' (update) ")
    print("Usunac dane - 'd' (destroy) ")
    print("Wyjsc z programu - 'x' ")

    czynnosc = input("INPUT: ")
    if czynnosc not in dozwolone_znaki:
        raise ValueError("Wprowadzona wartość jest nieprawidłowa. Dozwolone wartości to: c, r, u, d, x")

    print('---------------------')
    if czynnosc == "x":
        print("Wyjscie z programu.")
        break
    elif czynnosc == "c":
        DodajRekord()
    elif czynnosc == "r":
        OdczytajRekord()
    elif czynnosc == "u":
        AktualizujRekord()
    elif czynnosc == "d":
        UsunRekord()

db.commit()
db.close()
