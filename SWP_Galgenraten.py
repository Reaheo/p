from tkinter import *
import random



class Galgenraten:
    def __init__(self, root):
        self.__root = root
        self.__root.title("Galgenraten")
        self.__root.geometry("1000x500")
        self.__root.config(bg="aquamarine")
        self.__root.option_add("*Font", "Arial 12")


        self.__filename = "Woerter.txt"
        self.__guess_word = ""
        self.__interim_status = []
        self.__wrong = 0
        self.__right = 0
        self.__wrong_letters = ""
        self.__wins = 0
        self.__defeats = 0

        self.__create_gui()
        self.__new_word()

    """
    Erstelung der Objekte der Klassen
    """    
    # folgende Methoden


    def __create_gui(self):
        self.__canvas = Canvas(self.__root, width=500, height=400, bg="aquamarine", highlightbackground="aquamarine")
        self.__canvas.place(x=250, y=90)

        self.__label_A = Label(self.__root, text="Zu erratendes Wort:", bg="aquamarine")
        self.__label_A.place(x=10, y=12)

        self.__label_B = Label(self.__root, text="Buchstabe raten:", bg="aquamarine")
        self.__label_B.place(x=10, y=48)

        self.__label_C = Label(self.__root, text="Wort:", bg="aquamarine")
        self.__label_C.place(x=10, y=243)

        self.__label_word = Label(self.__root, font=("Arial", 14), bg="aquamarine")
        self.__label_word.place(x=165, y=10)

        self.__label_status = Label(self.__root, text="Spiel läuft", bg="aquamarine")
        self.__label_status.place(x=790, y=10)

        self.__label_mistakes = Label(self.__root, text="Fehler: 0", bg="aquamarine")
        self.__label_mistakes.place(x=790, y=50)

        self.__label_statistics = Label(self.__root, text="Siege: 0 | Niederlagen: 0", bg="aquamarine")
        self.__label_statistics.place(x=790, y=130)

        self.__label_right = Label(self.__root, text=f"0 von {len(self.__guess_word)} richtig", bg="aquamarine")
        self.__label_right.place(x=790, y=90)

        self.__label_wrong = Label(self.__root, text=f"0 von {len(self.__guess_word)} richtig", bg="aquamarine")
        self.__label_wrong.place(x=180, y=48)

        self.__Entry_Word = Entry(self.__root)
        self.__Entry_Word.place(x=135, y=50, width=30)

        self.__button_guess = Button(self.__root, text="Raten", command=self.__guess)
        self.__button_guess.place(x=10, y=80, width=145, height=30)

        self.__button_new = Button(self.__root, text="Neues Spiel", command=self.__reset)
        self.__button_new.place(x=10, y=120, width=145, height=30)

        self.__Entry_next = Entry(self.__root)
        self.__Entry_next.place(x=55, y=240, width=150, height=30)

        self.__button_next = Button(self.__root, text="mit Wort starten", command=self.__naechstes_wort)
        self.__button_next.place(x=10, y=200, width=145, height=30)

        self.__root.bind("<Insert>", lambda e: self.__naechstes_wort())
        self.__root.bind("<Escape>", lambda e: self.__root.destroy())

    """
    Erstellung der Buttons, Eingbefelder, Labels, Canvas in der GUI sowie die Einbundung von Tatsten 
    """


    def __set_colour(self,neueFarbe):
        self.__root.config(bg=neueFarbe) 
        self.__canvas.config(bg=neueFarbe, highlightbackground=neueFarbe)

        for widget in self.__root.winfo_children():
            if isinstance(widget, Label):
                widget.config(bg=neueFarbe)   

    """
    Umfärben aller Objekte außer Buttons und Eingabefelder    
    """            


    def __new_word(self):
        with open(self.__filename, "r", encoding="utf-8") as file:
            words = [word.strip().upper() for word in file if word.strip()]

        self.__guess_word = random.choice(words)
        self.__game_reset()

    """
    zufälliges Wort aus Wörter.txt Datei
    Methodenaufruf: __spiel_reset
    """


    def __naechstes_wort(self):
        word = self.__Entry_next.get().upper()
        self.__Entry_next.delete(0, END)

        if not word:
            return

        with open(self.__filename, "r", encoding="utf-8") as file:
            words = [worte.strip().upper() for worte in file]

        if word not in words:
            with open(self.__filename, "a", encoding="utf-8") as file:
                file.write("\n" + word)

        self.__guess_word = word
        self.__game_reset()

    """
    nächstes Wort mit Eingabefeld eingeben und in Woerter.txt Datei einfügen, falls nicht schon vorhanden
    Methodenaufruf: __game_reset
    """


    def __reset(self):
        self.__wins = 0
        self.__defeats = 0
        self.__new_word()

    """
    zurücksetzen von Spielständen
    Methodenaufruf: __new_game
    """    


    def __game_reset(self):
        self.__interim_status = ["_ "] * len(self.__guess_word)
        self.__wrong = 0
        self.__right = 0
        self.__wrong_letters = ""

        self.__canvas.delete("all")
        self.__draw(0)

        self.__label_status.config(text="Spiel läuft")
        self.__button_guess.config(text="Raten", command=self.__guess)

        self.__update_dispay()
        self.__root.bind("<Return>", lambda e: self.__guess())
        self.__set_colour("aquamarine")

    """
    zurücksetzen der falschen/richtigen Buchstaben, Button, Label zurücksetzen
    Methodenaufruf: __draw(0) -> für Beginn
                    __set_colour("aquamarine") -> ausgewählte Farbe  
                    __update_anzeige      
    """


    def __guess(self):
        letter = self.__Entry_Word.get().upper()
        self.__Entry_Word.delete(0, END)

        if not letter:
            return

        treffer = False

        for i, l in enumerate(self.__guess_word):
            if l == letter and self.__interim_status[i] == "_ ":
                self.__interim_status[i] = letter
                self.__right += 1
                treffer = True
            elif l == letter and self.__interim_status[i] == letter:
                treffer = True

        if not treffer:
            self.__wrong += 1
            if letter not in self.__wrong_letters:
                self.__wrong_letters += letter
        self.__draw(self.__wrong)

        self.__update_dispay()

        if self.__right == len(self.__guess_word):
            self.__won()
        elif self.__wrong >= 9:
            self.__lost()

    """
    Auslesen des geratenen Buchstaben, Test ob Buchstabe richtig geraten -> Anpassen der Statistiken sowie Information für Spieler (falsche Buchstaben, Wort mit strichen und Buchstaben) danach
    Methodenaufruf: __draw(self.__falsch) -> Anzahl falscher Buchstaben
                    __update_display
                    __won -> falls alle Buchstaben gefunden
                    __lost -> falls zu viele Fehlversuche
    """


    def __update_dispay(self):
        self.__label_word.config(text="".join(self.__interim_status))
        self.__label_mistakes.config(text=f"Fehler: {self.__wrong}")
        self.__label_statistics.config(text=f"Siege: {self.__wins} | Niederlagen: {self.__defeats}")
        self.__label_right.config(text=f"{self.__right} von {len(self.__guess_word)} richtig")
        self.__label_wrong.config(text=f"falsche Buchstaben: {self.__wrong_letters}")

    """
    Anpassen der Statistischen Labels mit neuen Werten
    """


    def __won(self):
        self.__label_status.config(text="Spiel gewonnen!")
        self.__wins += 1
        self.__update_dispay()
        self.__button_guess.config(text="Neues Wort", command= lambda: self.__new_word())
        self.__root.bind("<Return>", lambda e: self.__new_word())
        self.__draw_win()

    """
    Änderung der Labels zur Information zum sieg sowie Anzahl Siege erhöhen, Button/Taste Anpassen
    Methodenaufruf: __update_display
                    __draw_win
    """    


    def __draw_win(self):
        self.__canvas.delete("all")
        self.__canvas.create_line(50,350, 450,350, fill="dark green", width = 5)
        self.__canvas.create_line(100,360, 100,30, fill="black", width=10)
        self.__canvas.create_line(50,50, 450,50, fill="black", width=10)
        self.__canvas.create_line(120,50, 100,70, fill="black", width=10)
        self.__canvas.create_line(400,50, 400,100, fill="black", width=10)
        self.__canvas.create_oval(375,200, 425,250, outline="black", width = 3)
        self.__canvas.create_line(400,250, 400,300, fill="black", width=4)
        self.__canvas.create_line(400,275, 375,250, fill="black", width=3)
        self.__canvas.create_line(400,275, 425,250, fill="black", width=3)
        self.__canvas.create_line(400,300, 375,350, fill="black", width=3)
        self.__canvas.create_line(400,300, 425,350, fill="black", width=3)
        self.__set_colour("green")

    """
    Zeichnung für den Sieg im Canvas
    Methodenaufruf: __set_colour("green") -> ausgewählte Farbe bei Sieg
    """


    def __lost(self):
        self.__label_status.config(text="Spiel verloren!")
        self.__defeats += 1
        self.__label_word.config(text=self.__guess_word)
        self.__update_dispay()
        self.__button_guess.config(text="Aufdecken", command = lambda: self.__reveal())
        self.__root.bind("<Return>", lambda e: self.__reveal())
        self.__set_colour("maroon")
        
    """
    Änderung der Labels zur Information der Niederlage sowie Anzahl Niederlagen erhöhen, Button/Taste Anpassen
    Methodenaufruf: __update_display
                    __set_colour("maroon") -> ausgewählte Farbe bei Niederlage

    """


    def __draw(self, nummer):
        if nummer == 0:
            self.__canvas.create_line(50,350, 450,350, fill="dark green", width = 5)
        if nummer == 1:
            self.__canvas.create_line(100,360, 100,30, fill="black", width=10)
        if nummer == 2:
            self.__canvas.create_line(50,50, 450,50, fill="black", width=10)
            self.__canvas.create_line(120,50, 100,70, fill="black", width=10)
        if nummer == 3:
            self.__canvas.create_line(400,50, 400,100, fill="black", width=10)
        if nummer == 4:
            self.__canvas.create_oval(375,100, 425,150, outline="black", width = 3)
        if nummer == 5:
            self.__canvas.create_line(400,150, 400,200, fill="black", width=4)
        if nummer == 6:
            self.__canvas.create_line(400,175, 375,150, fill="black", width=3)
        if nummer == 7:
            self.__canvas.create_line(400,175, 425,150, fill="black", width=3)
        if nummer == 8:
            self.__canvas.create_line(400,200, 375,250, fill="black", width=3)
        if nummer == 9:
            self.__canvas.create_line(400,200, 425,250, fill="black", width=3)

    """
    Zeichnen des nächsten Schrittes je nach Fehleranzahl
    """
    
    
    def __reveal(self):
        self.__button_guess.config(text="Neuer Versuch", command = lambda: self.__new_word())
        self.__label_word.config(text=self.__guess_word)
        self.__root.bind("<Return>", lambda e: self.__new_word())

    """
    Aufdecken des Gesuchten Wortes, Einstellung des Buttons(sowie der Taste) für neues Wort
    """


"""
Funktion des GUI/tkinter starten
"""