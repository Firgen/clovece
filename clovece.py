from random import randint
from copy import deepcopy
import os

pole = list("        O O O O O        \n" +\
"  O O   O   O   O   O O  \n" +\
"  O O   O   O   O   O O  \n" +\
"        O   O   O        \n" +\
"O O O O O   O   O O O O O\n" +\
"O                       O\n" +\
"O O O O O       O O O O O\n" +\
"O                       O\n" +\
"O O O O O   O   O O O O O\n" +\
"        O   O   O        \n" +\
"  O O   O   O   O   O O  \n" +\
"  O O   O   O   O   O O  \n" +\
"        O O O O O        ")

# farby
RESET = "\033[0m"
farby = ["RED", "GREEN", "BLUE", "YELLOW"]
farby2 = {"RED": "\033[1;31m",
          "GREEN": "\033[1;32m",
          "BLUE": "\033[1;34m",
          "YELLOW": "\033[1;33m",
          "CYAN": "\033[1;36m"}

# všetky políčka tmavšie
for i in range(len(pole)):
    if pole[i] == "O":
        pole[i] = "\033[2mO\033[0m"

# začiatočné políčka
# 0
pole[104] = "\033[2;31mO\033[0m"
# 1
pole[16] = "\033[2;32mO\033[0m"
# 2
pole[232] = "\033[2;34mO\033[0m"
# 3
pole[320] = "\033[2;33mO\033[0m"

# domovské políčka
# 0
pole[28] = pole[30] = pole[54] = pole[56] = "\033[2;31mO\033[0m"
# 1
pole[46] = pole[48] = pole[72] = pole[74] = "\033[2;32mO\033[0m"
# 2
pole[280] = pole[282] = pole[306] = pole[308] = "\033[2;34mO\033[0m"
# 3
pole[262] = pole[264] = pole[288] = pole[290] = "\033[2;33mO\033[0m"

# cieľové políčka
# 0
pole[158] = pole[160] = pole[162] = pole[164] = "\033[2;31mO\033[0m"
# 1
pole[38] = pole[64] = pole[90] = pole[116] = "\033[2;32mO\033[0m"
# 2
pole[178] = pole[176] = pole[174] = pole[172] = "\033[2;34mO\033[0m"
# 3
pole[298] = pole[272] = pole[246] = pole[220] = "\033[2;33mO\033[0m"

novepole = deepcopy(pole)

policka = {'0': 8, '1': 10, '2': 12, '3': 14, '4': 16,
           '47': 34, '5': 42,
           '46': 60, '6': 68,
           '45': 86, '7': 94,
           '40': 104, '41': 106, '42': 108, '43': 110, '44': 112, '8': 120, '9': 122, '10': 124, '11': 126, '12': 128,
           '39': 130, '13': 154,
           '38': 156, '14': 180,
           '37': 182, '15': 206,
           '36': 208, '35': 210, '34': 212, '33': 214, '32': 216, '20': 224, '19': 226, '18': 228, '17': 230, '16': 232,
           '31': 242, '21': 250,
           '30': 268, '22': 276,
           '29': 294, '23': 302,
           '28': 320, '27': 322, '26': 324, '25': 326, '24': 328}

domov = {'100': 28, '101': 30, '102': 54, '103': 56,
         '200': 46, '201': 48, '202': 72, '203': 74,
         '300': 280, '301': 282, '302': 306, '303': 308,
         '400': 262, '401': 264, '402': 288, '403': 290}

zaciatok = {"0": 40,
            "1": 4,
            "2": 16,
            "3": 28}

ciel = {'1000': 158, '1001': 160, '1002': 162, '1003': 164,
        '2000': 38, '2001': 64, '2002': 90, '2003': 116,
        '3000': 178, '4001': 176, '4002': 174, '4003': 172,
        '4000': 298, '3001': 272, '3002': 246, '3003': 220}


class Figurka(object):
    def __init__(self, pozicia, popis):
        self.pozicia = pozicia
        self.popis = popis
        self.konci = False

    def overflow(self):
        if 60 > self.pozicia > 47:
            self.pozicia -= 48
        if self.pozicia < 0:
            self.pozicia = 48 + self.pozicia

    def tah(self, a):
        self.pozicia += a


class Hrac(object):
    def __init__(self, farba):
        self.farba = farba
        self.figurky = [Figurka(0, farba + str(i + 1) + RESET) for i in range(4)]
        self.popis = farba + "hráč" + RESET


def namiesta():
    global novepole
    global pole
    novepole = deepcopy(pole)
    for hrac in hraci:
        for figurka in hrac.figurky:
            if figurka.pozicia <= 50:
                novepole[policka[str(figurka.pozicia)]] = figurka.popis
            elif figurka.pozicia <= 500:
                novepole[domov[str(figurka.pozicia)]] = figurka.popis
            else:
                novepole[ciel[str(figurka.pozicia)]] = figurka.popis

    print(RESET)
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
    print("".join(novepole), "\n")


def cislo(prosba):
    global pokracovat
    while True:
        hodnota = input(prosba)
        if hodnota == "1" or hodnota == "2" or hodnota == "3" or hodnota == "4":
            return int(hodnota)
        else:
            pokracovat = input("\nVložiť číslo od 1 po 4 !")
            print("")


pocet = cislo("Počet hráčov: ")

# vytvorí hráčov a dá im farby
hraci = [Hrac(farby2[farby[i]]) for i in range(pocet)]

# najviac koľko figúrok je v cieli
vcieli = 0

# dá figúrkam začiatočné pozície
for i in range(len(hraci)):
    for x in range(4):
        hraci[i].figurky[x].pozicia = (i+1)*100 + x

# hráči si vyberú mená
for i in range(len(hraci)):
    hraci[i].popis = hraci[i].farba + input("\nMeno hráča " + str(i+1) + ": ") + RESET

# vyberie prvého hráča
narade = randint(0, len(hraci) - 1)

# hra
namiesta()

print("Začína " + hraci[narade].popis + ".\n")

while True:
    #hod = 6
    hod = randint(1, 6)
    pokracovat = input("Hodiť kockou")
    print("\nHodil/-a si " + farby2[farby[narade]] + str(hod) + RESET + ".\n", flush=True)
    ktora = cislo(RESET + "Posunúť figúrku: " + farby2[farby[narade]] ) - 1

    # ak figúrka končí celé kolo
    if hraci[narade].figurky[ktora].konci:
        # ak je na rade zelený
        if narade == 1:
            if hraci[narade].figurky[ktora].pozicia < 5:
                # ak ešte nedojde do cieľa
                if hraci[narade].figurky[ktora].pozicia + hod <= zaciatok[str(narade)] - 2:
                    hraci[narade].figurky[ktora].tah(hod)
                # ak už dojde do cieľa
                else:
                    # ak hodil príliš veľa
                    if hraci[narade].figurky[ktora].pozicia + hod > (zaciatok[str(narade)] + 2):
                        pokracovat = input("\nHodil/-a si príliš veľa.")
                    # ak nie
                    else:
                        # ak je políčko v cieli prázdne
                        if novepole[ciel[str(
                                (narade+1)*1000 + hraci[narade].figurky[ktora].pozicia + hod
                                - (zaciatok[str(narade)] - 1))]][7] == "O":
                            hraci[narade].figurky[ktora].pozicia = (narade+1)*1000 + hraci[narade].figurky[ktora].pozicia +\
                                                               hod - (zaciatok[str(narade)] - 1)
                            hraci[narade].figurky[ktora].konci = False

                            # zistí, koľko figúrok je v cieli
                            vcieli = 0
                            for f in hraci[narade].figurky:
                                if f.pozicia > 900:
                                    vcieli += 1
                        # ak je obsadené
                        else:
                            pokracovat = input("\nPolíčko je obsadené.")
            elif hraci[narade].figurky[ktora].pozicia + hod > 40:
                # ak dojde do cieľa
                if hraci[narade].figurky[ktora].pozicia + hod >= 51:
                    # ak je políčko v cieli prázdne
                    if novepole[ciel[str(
                            (narade+1)*1000 + hraci[narade].figurky[ktora].pozicia + hod
                            - (zaciatok[str(narade)] - 1) - 48)]][7] == "O":
                        hraci[narade].figurky[ktora].pozicia = (narade+1)*1000 + hraci[narade].figurky[ktora].pozicia +\
                                                           hod - (zaciatok[str(narade)] - 1) - 48
                        hraci[narade].figurky[ktora].konci = False

                        # zistí, koľko figúrok je v cieli
                        vcieli = 0
                        for f in hraci[narade].figurky:
                            if f.pozicia > 900:
                                vcieli += 1
                    # ak je obsadené
                    else:
                        pokracovat = input("\nPolíčko je obsadené.")
                # ak nedojde do cieľa
                else:
                    hraci[narade].figurky[ktora].tah(hod)
                    hraci[narade].figurky[ktora].overflow()
        # ak nie je na rade zelený
        else:
            # ak ešte nedojde do cieľa
            if hraci[narade].figurky[ktora].pozicia + hod <= zaciatok[str(narade)] - 2:
                hraci[narade].figurky[ktora].tah(hod)
            # ak už dojde do cieľa
            else:
                # ak hodil príliš veľa
                if hraci[narade].figurky[ktora].pozicia + hod > (zaciatok[str(narade)] + 2):
                    pokracovat = input("\nHodil/-a si príliš veľa.")
                # ak nie
                else:
                    # ak je políčko v cieli prázdne
                    if novepole[ciel[str(
                            (narade+1)*1000 + hraci[narade].figurky[ktora].pozicia + hod
                            - (zaciatok[str(narade)] - 1))]][7] == "O":
                        hraci[narade].figurky[ktora].pozicia = (narade+1)*1000 + hraci[narade].figurky[ktora].pozicia +\
                                                           hod - (zaciatok[str(narade)] - 1)
                        hraci[narade].figurky[ktora].konci = False

                        # zistí, koľko figúrok je v cieli
                        vcieli = 0
                        for f in hraci[narade].figurky:
                            if f.pozicia > 900:
                                vcieli += 1
                    # ak je obsadené
                    else:
                        pokracovat = input("\nPolíčko je obsadené.")

    # ak nekončí
    else:
        # ak je v poli
        if hraci[narade].figurky[ktora].pozicia < 50:
            hraci[narade].figurky[ktora].tah(hod)
            hraci[narade].figurky[ktora].overflow()
        # ak je doma
        elif hraci[narade].figurky[ktora].pozicia < 500:
            if hod == 6:
                # vyhadzovanie
                # ak je prázdne políčko
                if novepole[policka[str(zaciatok[str(narade)])]][7] == "O":
                    hraci[narade].figurky[ktora].pozicia = zaciatok[str(narade)]
                # ak je to figúrka
                else:
                    for h in hraci:
                        # ak je to figúrka rovnakého hráča
                        if h == hraci[narade]:
                            for f in h.figurky:
                                if f.pozicia == zaciatok[str(narade)]:
                                    pokracovat = input("\nŠtartovacie políčko je obsadené.")
                                    break
                            else:
                                continue
                            break
                        # ak je to figúrka iného hráča
                        else:
                            for f in h.figurky:
                                if f.pozicia == zaciatok[str(narade)]:
                                    for i in range((hraci.index(h)+1)*100, (hraci.index(h)+1)*100 + 4):
                                        if novepole[domov[str(i)]][7] == "O":
                                            f.pozicia = i
                                            f.konci = False
                            hraci[narade].figurky[ktora].pozicia = zaciatok[str(narade)]
                # ak je to figúrka iného hráča
            else:
                pokracovat = input("\nMusíš hodiť 6.")
        # ak je v cieli
        else:
            pokracovat = input("\nFigúrka je v cieli.")

    # vyhadzovanie figúrok
    if hraci[narade].figurky[ktora].pozicia < 50:
        if novepole[policka[str(hraci[narade].figurky[ktora].pozicia)]] != "\033[2mO\033[0m":
            for h in hraci:
                for f in h.figurky:
                    # ak je to figúrka práve na ťahu
                    if f == hraci[narade].figurky[ktora]:
                        continue
                    elif f.pozicia == hraci[narade].figurky[ktora].pozicia:
                        # ak je to figúrka rovnakého hráča
                        if h == hraci[narade]:
                            pokracovat = input("Políčko je obsadené.")
                            hraci[narade].figurky[ktora].pozicia -= hod
                            hraci[narade].figurky[ktora].overflow()
                            break
                        # ak je to figúrka iného hráča
                        else:
                            for i in range((hraci.index(h)+1)*100, (hraci.index(h)+1)*100 + 4):
                                if novepole[domov[str(i)]][7] == "O":
                                    f.pozicia = i
                                    f.konci = False

    namiesta()

    # zistí, či figúrka už ubehla kolo
    if zaciatok[str(narade)] - 8 < hraci[narade].figurky[ktora].pozicia < zaciatok[str(narade)]:
        hraci[narade].figurky[ktora].konci = True
    if narade == 1:
        if 44 < hraci[narade].figurky[ktora].pozicia < 50 or hraci[narade].figurky[ktora].pozicia < 4:
            hraci[narade].figurky[ktora].konci = True

    # ďalší je narade alebo niekto vyhral
    if vcieli == 4:
        print("Vyhral " + hraci[narade].popis + ".\n")
        break
    if narade == len(hraci) - 1:
        narade = 0
    else:
        narade += 1
    print("Na rade je " + hraci[narade].popis + ".\n")
