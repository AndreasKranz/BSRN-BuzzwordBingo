                                    # BuzzwordBingo Werkstück A BSRN- Delos Joel Herold, Andreas Kranz, Gracjan Sekora
import curses       #Bibliothek zur grafischen Darstellung im Terminal
import random       #Bibliothek mit zufallsfunktionen
import time         #Bibliothek zum verzögern der Programmausführung





class Feld():  # Diese Klasse dient als Feld in der Bingokarte(eine Bingokarte ist mit n Feldern gefüllt)
    def __init__(self, buzzword):   # Konstruktor zum erstellen von Objekten der Klasse Feld
        self.buzzword = buzzword
        self.durchgestrichen = False
        if (buzzword == "JOKER"):  # Der Joker
            self.durchgestrichen = True



class Karte():  # Die Karte die Liste der Felder und bietet die Funktionalität zum spielen im Hintergrund
    alleWoerter = []  # Liste aller Buzzwords

    def __init__(self):  # Konstruktor zum Initialisieren der Variablen und erstellen von Objekten der Klasse Karte
        self.gewonnen = False
        self.felder = []    #Liste der Objekte Felder
        self.dimension = 0  # beschreibt die Kartengröße, da im Quadratformat nur ein wert
        self.anzahlFelder = 0  # Die Anzahl aller Wörter, Quadrat der Kratendimension


    def woerter_Einlesen(self):  # liest die buzzwords aus der Datei in die Liste 'alleWoerter'
        with open('woerter_liste', 'r') as wort:  # Wörter sind durch Zeilenumbrüche getrennt in der Datei
            self.alleWoerter = wort.read().splitlines()


    def kartenParameter_eingeben(self, eingabe):  # Übergabe der Spielfeldparameter aus der Nutzereingabe
        self.dimension = eingabe
        self.anzahlFelder = eingabe * eingabe   #Da die Bingokarte quadratisch ist ergibt sich die Anzahl aus dem Quadrat



    def erstelle_ZufallsListe(self):  # Die Liste der Wörter wird gefüllt
        tempList = random.sample(self.alleWoerter,len(self.alleWoerter)) # Liste der buzzwords mit zufälliger Reihenfolge

        for i in range(0,self.anzahlFelder):  # for-Schleife zum befüllen der Felder-Liste
            str = tempList[i]
            bingokarte.felder.append(Feld(str))  # ein Objekt von Feld mit dem gezogenen buzzword wird erstellt und der Liste hinzugefügt

        if bingokarte.dimension == 5:
            bingokarte.felder[12] = Feld("JOKER") #das zentrale Feld für 5x5 karten wird mit einem Joker ersetzt(siehe Zeile 15)
                            # Für 5x5 und 7x7 Karten wird das mittlere Feld als Joker genutzt
        if bingokarte.dimension == 7:
            bingokarte.felder[24] = Feld("JOKER")  #das zentrale Feld für 7x7 karten wird mit einem Joker ersetzt(siehe Zeile 15)


    def wortStreichen(self,index):  # dient zum streichen der Felder // wird aufgerufen wenn der Spieler auf ein Wort drückt
        tempFeld = self.felder[index]
        tempFeld.durchgestrichen = True



    def pruefeGewinn(self, index): #überprüft nach jedem gestrichenen Wort die Siegbedingung
        rest = index % self.dimension  # bestimmt die Zeile die berührt wird (Rest = 0 -> 1.Zeile, R1 -> 2.Zeile)
        quotient = int(index / self.dimension)  # bestimmt die Spalte die berührt wird(Quotient <1  -> 1.Spalte)
        counter = 0                 #zählt die gestrichenen Wörter

        # berührte Spalte wird nach kompletter Reihe durchsucht
        for i in range(quotient * self.dimension, ((quotient + 1) * self.dimension)):  # qutient ist die spalte und i ist die position in der spalte
            if bingokarte.felder[i].durchgestrichen:    #zählt für jedes gestrichene Wort hoch
                counter += 1
            else:       #wenn ein Wort in der Spalte nicht gestrichen ist kann die Überprüfung für die Spalte beendet werden
                break
        if counter == self.dimension:
            gewonnen()      #alle Wörter in der Spalte sind gestrichen das Spiel ist gewonnen
        else:
            counter = 0

        # berührte Zeile wird nach kompletter Reihe durchsucht
        for z in range(self.dimension):
            stelle = z * self.dimension + rest  # rest ist die zeile und z ist die position in der zeile
            if bingokarte.felder[stelle].durchgestrichen:
                counter += 1
            else:
                break
        if counter == self.dimension:
            gewonnen()      #alle Wörter in der Zeile sind gestrichen das Spiel ist gewonnen
        else:
            counter = 0

        # Diagonale (oben links nach unten rechts) wird nach kompletter Reihe durchsucht
        for y in range(self.dimension):
            stelle = y * self.dimension + y  # wir zählen die Stellen(Positionen) der diagonale durch(2*4+2) bei dimension =4
            if bingokarte.felder[stelle].durchgestrichen:  # y ist quasi +1 weil die diagonal werte immer die dimesion +1 sind
                counter += 1
            else:
                break
        if counter == self.dimension:
            gewonnen()      #alle Wörter in der Diagonale sind gestrichen das Spiel ist gewonnen
        else:
            counter = 0

        # Diagonale (unten links nach oben rechts) wird nach kompletter Reihe durchsucht
        for k in range(1, (self.dimension + 1)):  # wir zählen von 1-4
            stelle = k * self.dimension - k  # -k weil die diagonale immer die dimesion -1 ist
            if bingokarte.felder[stelle].durchgestrichen:
                counter += 1
            else:
                break
        if counter == self.dimension:
            gewonnen()      #alle Wörter in der Diagonale sind gestrichen das Spiel ist gewonnen
        else:
            counter = 0



    def export_BingoKarte(self):  # dient zum exportieren der BingoKarte in eine Text datei
        export = []

        for a in self.felder:  # dient zum "printen" der Buzzwords damit die exportierte Karte symetrisch ist
            whole_length = 20  # festgelegte Wortlänge von 20 Zeichen
            length = len(a.buzzword)
            diff = whole_length - length
            if diff > 0:
                for x in range(diff):  # wenn das Wort weniger als 20 Zeichen hat wird die Differenz mit Leerzeichen aufgefüllt
                    a.buzzword += " "

                export.append(a.buzzword)  # alle Wörter haben jetzt die gleiche Länge und befinden sich in einer Liste

        datei = open('export.txt', 'w')  # die ziel Datei

        for id, words in enumerate(export):  # in der for Schleife wird die Liste wie ein Feld ausgegeben. Je nach Spielfeldgröße findet ein Spaltenumbruch statt
            for b in range(1,9):
                if id == self.dimension*b:
                    datei.write("\n")

            datei.write(words)

        datei.close()
        self.felder = []



bingokarte = Karte()          #Erstellen eines Kartenobjekts mit dem Namen bingokarte
bingokarte.woerter_Einlesen()   # Bereitet das Programm vor (zieht wörter aus einer Text Datei)
input = bingokarte.felder        # Input ist eine Liste gefüllt mit Objekten der Klasse Feld


##################################################################################################################################################
#in folgendem kommt die Spieloberfläche

def print_spielfeld(stdscr, selected_row_id, enter_list):         #ausgeben des Spielfeldes
    stdscr.clear()
    spielfeld = bingokarte.dimension
    x = 0
    y = 0

    max = ""
    for a in input:          # Findet das längste Wort in der Liste, dient zur Bestimmung des Abstands zwischen den Wörtern
        if len(a.buzzword) > len(max):
            max = a.buzzword

    max += "   "

    for idx, row in enumerate(input):                                                           #gibt das Spielfeld aus

        for b in range(1,9):                                                                    #Je nach Spielfeldgröße findet ein Spaltenumbruch statt
            if idx == spielfeld * b:
                x += len(max)
                y = 0

        if idx == selected_row_id:                                                              #aktuelles Feld, in welchem der spieler sich befindet, wird makiert
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row.buzzword, )
            stdscr.attroff(curses.color_pair(1))

        elif idx in enter_list:                                                                 # Feld, welches der Spieler ausgewählt hat ist permanent grün
            stdscr.addstr(y, x, row.buzzword, curses.color_pair(2))

        else:                                                                                   # alle anderen wörter werden normal angezeigt
            stdscr.addstr(y, x, row.buzzword)

        y += 1

    stdscr.refresh()


def spielfeld_main(stdscr):                                                                     # Steuerung des Spielfeldes
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)                                 # festlegen der Farben
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    current_row_id = 0
    enter_list = []

    print_spielfeld(stdscr, current_row_id, enter_list)                                         # Spielfeld wird ausgegeben

    while 1:

        key = stdscr.getch()                                                                    #die Benutzereingabe wird gespeichert
        stdscr.clear()                                                                          #aktuelles Spielfeld wird gelöscht
        if key == curses.KEY_UP and current_row_id > 0:                                         #der Spieler bewegt sich nach oben
            current_row_id -= 1
        elif key == curses.KEY_DOWN and current_row_id < len(input) - 1:                        #der Spieler bewegt sich nach unten
            current_row_id += 1
        elif key == curses.KEY_RIGHT and current_row_id < len(input) - bingokarte.dimension:    #der Spieler bewegt sich nach rechts
            current_row_id += bingokarte.dimension
        elif key == curses.KEY_LEFT and current_row_id >= bingokarte.dimension:                 #der Spieler bewegt sich nach links
            current_row_id -= bingokarte.dimension
        elif key == curses.KEY_ENTER or key == 10 or key == 13 and current_row_id:              #der Spieler drückt Enter
            stdscr.clear()
            enter_list.append(current_row_id)                                                   #Liste mit allen ausgewählten Feldern(Grün makiert)
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(0, 0, "Sie haben {} gedrückt".format(input[current_row_id].buzzword)) #ausgabe welches Feld der Spieler gedrückt hat
            stdscr.attroff(curses.color_pair(2))
            bingokarte.wortStreichen(current_row_id)                                            #das aktuelle Wort wird "gestrichen" auf TRUE gesetzt
            bingokarte.pruefeGewinn(current_row_id) #prüfe nach jedem ENTER ob der Spieler gewonnen hat
            stdscr.refresh()
            time.sleep(0.7) #das gedrückte wort wird für 0.7 sekunden angezeigt

        print_spielfeld(stdscr, current_row_id, enter_list) #das Spielfeld inklusive der Veränderungen wird erneut ausgegeben
        stdscr.refresh()


################################################
# Ausgabe des Menüs

menu = ['Play', 'Exportieren', 'Spielanleitung', 'Exit']


def print_menu(stdscr, selected_row_id):
    stdscr.clear()
    h, w = stdscr.getmaxyx()    # maximale größe der Konsole

    for idx, row in enumerate(menu):    # berechnet die mitte der Konsole
        x = w // 2 - len(row) // 2      #len(row)//2 ist die halbe länge eines wortes in der Liste menu
        y = h // 2 - len(menu) // 2 + idx #len(menu)//2 ist die halbe länge der menu liste
        if idx == selected_row_id:  #zeigt dem Spieler die aktuelle position an
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)    #gibt die Liste menu aus
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)    #gibt alle anderen Wörter, auf welchen sich der Spieler nicht befindet aus
    stdscr.refresh()


# Steuerung des Menüs
def menu_main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #festlegen der Farben
    current_row_id = 0
    print_menu(stdscr, current_row_id) # Das men ausgeben

    while 1:            # Steuert die Bewegung im Menu
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_id > 0:
            current_row_id -= 1
        elif key == curses.KEY_DOWN and current_row_id < len(menu) - 1:
            current_row_id += 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13 and current_row_id:
            if current_row_id == 0:  # Es wird play gedrückt
                stdscr.addstr(0, 0, "Bitte geben sie die Größe der Bingo Karte zwischen 3 und 8 an. Bei großen Karten (6 oder mehr Spalten) im Vollbildmodus spielen")
                while (True):
                    try:        #Try/except, falsch die Eingabe fehlerhaft ist
                        user_input = int(stdscr.getkey())
                        break
                    except:
                        stdscr.addstr(0, 0,
                                      "Bitte geben sie die Größe der Bingo Karte zwischen 3 und 8 an. Bitte nur normale Nummerntasten")
                        continue
                bingokarte.kartenParameter_eingeben(user_input) #Übergeben der Spielfeldgröße
                bingokarte.erstelle_ZufallsListe()  #Die Bingokarte "erstellen"
                curses.wrapper(spielfeld_main)  #Das Spielfeld ausgeben
            elif current_row_id == 1:  #Es wird Exportieren gedrückt
                stdscr.addstr(0, 0, "Bitte geben sie die Größe der Bingo Karte zwischen 3 und 8 an")
                while (True): #falls die eingabe falsch ist
                    try:
                        user_input = int(stdscr.getkey())
                        break
                    except:
                        stdscr.addstr(0, 0,"Bitte geben sie die Größe der Bingo Karte zwischen 3 und 8 an. Bitte nur normale Nummerntasten")
                        continue
                bingokarte.kartenParameter_eingeben(user_input) #Übergeben der SPielfeldgröße
                bingokarte.erstelle_ZufallsListe()  #Die Bingokarte erstellen
                bingokarte.export_BingoKarte()
            elif current_row_id == 2: #Es wird Spielanleitung gedrückt
                stdscr.clear()
                stdscr.addstr(0, 0, "Nutzen sie die PFEILTASTEN um sich im Feld zu bewegen.")
                stdscr.addstr(1, 0,
                              "Mit ENTER makieren sie das aufgerufene Feld. Sobald sie eine Linie voll haben ist das Spiel vorbei.")
                stdscr.addstr(2, 0, "Viel Spaß......")
                stdscr.addstr(3, 0, "wünschen Andreas Kranz, Gracjan Sikora, Delos Joel Herold")
                stdscr.refresh()
                stdscr.getch()
            elif current_row_id == 3: #Es wird Exit gedrückt
                exit()


        print_menu(stdscr, current_row_id)#Das Menu wird ausgegeben
        stdscr.refresh()


def gewonnen():  # wird aufgerufen wenn die Gewinnbedingung erfüllt ist, zeigt die Gewinnmeldung an und beendet das Spiel
    stdscr = curses.initscr()
    stdscr.clear()
    curses.start_color()
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    h, w = stdscr.getmaxyx() #maximale Größe der Konsole
    x = w // 2 # mitte der x-Achse

    for a in range(3):  #Der Gewinn Text läuft 3 mal durch
        stdscr.clear()
        for i in range(h):  # so "hoch" wie die Konsole ist, so oft wird "Sie haben gewonnen" ausgegeben
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(i, x, "SIE HABEN GEWONNEN")
            stdscr.refresh()
            time.sleep(0.05) #0.05 Sekunden verzögerung, dadurch wird es zur Laufschrift

    time.sleep(1)   #Konsole wird noch für eine Sekunde angezeigt
    stdscr.attroff(curses.color_pair(3))
    exit()

curses.wrapper(menu_main)   # Der Wrapper ist eine Methode welche das öffnen und schließen des Fensters (stdscr) für uns übernimmt
