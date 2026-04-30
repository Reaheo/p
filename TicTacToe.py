from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import account
import memo


def start_Tic(parent):
    """
    Methode fuer Aufruf von Spielauswahl
    """

    ## Spieler initalisieren
#    name_A = player.get_name()
    name_A = "Mini"
    player_A = account.tic(name_A)
    name_B = "Max"
    player_B = account.tic(name_B)


    ## Speicher initialisieren
    table = memo.memo()


    ## Benutzeroberflaeche
    Form = Toplevel(parent)
    Form.title("TicTacToe")
    Form.geometry("600x400")
    field_lines = 5
        

    ## Methoden
    def new_game():
        """
        Prozedur, die Spielfeld/Anzeige und Speicher zuruecksetzt
        """
        playground.delete("all")
        playground.create_line(100,0, 100, 300, width=field_lines)
        playground.create_line(200,0, 200, 300, width=field_lines)
        playground.create_line(0,100, 300, 100, width=field_lines)
        playground.create_line(0,200, 300, 200, width=field_lines)

        table.clear()
    

    def start_game():
        """
        Prozedur bei Spielstart, welcher Spieler beginnt
        """
        global current_player
        # Vorausetzung: Symbolauswahl
        if (combo_symbols.get() == "Symbol"):
            messagebox.showerror("Spielstart", "Achtung: Es muss ein Symbol ausgewählt werden!")
        else:
            # Daten loeschen
            new_game()
            # wenn bisher kein Gewinner, Zufall -> erster Spieler
            if not(player_A.get_last_loser() or player_B.get_last_loser()):
                number_A = random.randint(1,2)
                number_B = number_A%2+1
                player_A.set_number(number_A)
                player_B.set_number(number_B)
                if number_A == 1:
                    current_player = player_A
                else:
                    current_player = player_B
            # wenn A verloren hat -> beginnt
            elif player_A.get_last_loser():
                current_player = player_A
                player_A.set_number(1)
                player_B.set_number(2)
            # wenn b verloren hat -> beginnt
            elif player_B.get_last_loser():
                current_player = player_B
                player_A.set_number(2)
                player_B.set_number(1)
            # Mitteilung auf Benutzeroberflaeche               
            start_player = Label(master=Form, text=f"{current_player.get_name()} ({current_player.get_symbol()}) beginnt.")
            start_player.place(x=20, y=170, width=210)


    def change_player():
        """
        Prozedur, die aktuellen Spieler austausch (nach Spielzug)
        """
        global current_player
        if current_player == player_A:
            current_player = player_B
        else:
            current_player = player_A


    def set_field():
        """
        Prozedur, die die Felder belegt und ueberprueft
        """
        # nur Belegung eines freien Feldes moeglich
        if not(table.get_player() == 0):
            messagebox.showinfo("Error", "Dieses Feld ist bereits belegt.\nBitte wählen Sie ein anderes!")
        else:
            # Symbol zeichnen
            current_player.draw_symbol(playground, table.get_row(), table.get_col(), field_lines)
            # Daten merken und ermitteln, ob Gewinner
            if table.set_memo(current_player.get_number()):
                messagebox.showinfo("Spiel beendet", f"Spieler {current_player.get_name()} hat gewonnen!")
                # Verlierer speichern
                if current_player == player_A:
                    player_A.set_last_loser(False)
                    player_B.set_last_loser(True)
                else:
                    player_A.set_last_loser(True)
                    player_B.set_last_loser(False)
                # neues Spiel starten, Daten loeschen
                start_game()
            else:
                # wenn kein Gewinner -> Spielerwechsel
                change_player()


    def selected_field(event):
        """
        Prozedur, die analysiert, in welches Feld geklickt wurde
        """
        # aus Mauskoordinaten Reihe und Spalte speichern
        table.set_row(event.x//100)
        table.set_col(event.y//100)
        # Feldbelegung starten
        set_field()


    def selection_changed(event):
        """
        Prozedur zur Zuordnung eines Symbols zu den Spielern
        """
        selection = combo_symbols.get()
        symbol_A = 0
        # wenn egal -> Zufall
        if selection == "Zufall":
            symbol_A = random.randint(1,2) #1-Kreuz, 2-Kreis
        # wenn Kreuz
        if (selection == "Kreuz") or (symbol_A == 1):
            player_A.set_symbol("Kreuz")
            player_B.set_symbol("Kreis")
        # wenn Kreis
        elif (selection == "Kreis") or (symbol_A == 2):
            player_A.set_symbol("Kreis")
            player_B.set_symbol("Kreuz")


    #Symbolwahl
    label_symbA = Label(master=Form, text=f"{name_A}, wählen Sie ihr Symbol:")
    label_symbA.place(x=20, y=50)
    combo_symbols = ttk.Combobox(master=Form, values=["Kreuz", "Kreis", "Zufall"])
    combo_symbols.set("Symbol")
    combo_symbols.place(x=30, y=80, width=70)
    combo_symbols.bind("<<ComboboxSelected>>", selection_changed)


    # Zeichenflaeche fuer Spielfeld
    playground = Canvas(master=Form, width=300, height=300)
    playground.place(x=250, y=50, width=300, height=300)


    #Button fuer Spielstart
    button_tic = Button(master=Form, text="Spiel starten", command=start_game)
    button_tic.place(x=20, y=120, width=210)


    # Auswahl Feld
    playground.bind("<ButtonRelease-1>", selected_field)


    # Formular ausfuehren
    return Form


# Funktionsaufruf fuer Testen    
#player = classes.player("Mini", True)
#start_Tic()