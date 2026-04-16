import tkinter as tk    
from FlappyBird import start_flappy_bird
from SWP_Galgenraten import Galgenraten
from TicTacToe import start_Tic
from snake import start_snake
from Gewinnt import vier_gewinnt

class GameLauncher:
    """
    Die Klasse GameLauncher repräsentiert die Hauptbenutzeroberfläche für die Minispiele. 
    """

    def __init__(self):
        """     
        Konstruktor der Klasse GameLauncher
        """ 
        self.__window = tk.Tk()
        self.__window.title("Minispiele")
        self.__window.geometry("1200x800")
        self.__window.config(bg="lightblue")

        # Bild Speichern
        self.__images = {}

        # Spiele definieren
        self.__games = [("SNAKE", "snake_picture.png", self._go_snake, 2),
                        ("Tic-Tac-Toe", "tic_picture.png", self._go_tic_tac_toe, 3), 
                        ("Galgenraten", "galgenraten_picture.png", self._go_galgenraten, 3), 
                        ("4-Gewinnt", "4-gewinnt_picture.png", self._go_4gewinnt, 3), 
                        ("Flappy Bird", "flappy_bird.png", self._go_flappy_bird, 6)]
        self.__create_buttons()
        self.__create_close_button()
    
    
    def __create_buttons(self):
        """
        Die Methode erstellt die Buttons für die Minispiele automatisch
        """
        columns = 4
        for c in range(columns):
            self.__window.columnconfigure(c, weight=1)
        for r in range((len(self.__games) // columns)+1):
            self.__window.rowconfigure(r, weight=1) 
        for i, (name, image_path, command, scale) in enumerate(self.__games):
            row = i // columns
            col = i % columns 
            image = self.__load_image(image_path, scale) if image_path else None
            button = tk.Button(self.__window, text=name, image=image, compound="top", width=170, height=200, anchor="s", pady=10, command=command, bg= "white", relief="raised", bd = 3, cursor = "hand2")
            button.grid(column=col, row=row, padx=30, pady=30)  
            button.config(font=("Arial", 12), bd=5)
        


    def __create_close_button(self):
        """
        Die Methode erstellt den Beenden-Button
        """
        button_close = tk.Button(self.__window, text= "Beenden", command= self.__window.quit)
        button_close.grid(column=3, row=10, pady= 15, padx= 15, sticky="e")
        button_close.config(bg="blue", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=5)
        
    def __load_image(self, path, scale):
        """
        Die Methode lädt ein Bild und speichert es in einem Dictionary, um zu verhindern, dass es von der Garbage Collection gelöscht wird.
        """
        if path not in self.__images:
            img = tk.PhotoImage(file=path)

            img = img.subsample(scale, scale)

            self.__images[path] = img    
        return self.__images[path]   

    def _go_snake(self):
        """
        Diese Funktion wird aufgerufen, wenn der Snake-Button gedrückt wird. Sie startet das Snake-Spiel, indem sie die Funktion start_snake() aus dem snake.py Modul aufruft. Während das Snake-Spiel läuft, wird das Hauptfenster der Benutzeroberfläche ausgeblendet, um eine bessere Spielerfahrung zu ermöglichen. Sobald das Snake-Spiel beendet ist, wird das Hauptfenster wieder angezeigt.
        """
        self.__window.withdraw() # Hauptfenster ausblenden
        start_snake() # Snake-Spiel starten
        self.__window.deiconify() # Hauptfenster wieder anzeigen, wenn Snake-Spiel beendet ist

    def _go_4gewinnt(self):
        """
        Diese Funktion wird aufgerufen, wenn der 4-Gewinnt-Button gedrückt wird. Sie startet das 4-Gewinnt-Spiel, indem sie die Funktion vier_gewinnt() aus dem Gewinnt.py Modul aufruft. Während das 4-Gewinnt-Spiel läuft, wird das Hauptfenster der Benutzeroberfläche ausgeblendet, um eine bessere Spielerfahrung zu ermöglichen. Sobald das 4-Gewinnt-Spiel beendet ist, wird das Hauptfenster wieder angezeigt.
        """
        self.__window.withdraw() # Hauptfenster ausblenden
        game_window = vier_gewinnt(self.__window) # 4-Gewinnt-Spiel starten
        self.__window.wait_window(game_window) # Warten, bis das Spiel-Fenster geschlossen wird
        self.__window.deiconify() # Hauptfenster wieder anzeigen

    def _go_flappy_bird(self):
        """
        Diese Funktion wird aufgerufen, wenn der Flappy-Bird-Button gedrückt wird. Sie startet das Flappy-Bird-Spiel, indem sie die Funktion start_flappy_bird() aus dem FlappyBird.py Modul aufruft. Während das Flappy-Bird-Spiel läuft, wird das Hauptfenster der Benutzeroberfläche ausgeblendet, um eine bessere Spielerfahrung zu ermöglichen. Sobald das Flappy-Bird-Spiel beendet ist, wird das Hauptfenster wieder angezeigt.
        """
        self.__window.withdraw() # Hauptfenster ausblenden
        game_window = start_flappy_bird(self.__window) # Flappy-Bird-Spiel starten
        self.__window.wait_window(game_window) # Warten, bis das Spiel-Fenster geschlossen wird
        self.__window.deiconify() # Hauptfenster wieder anzeigen, wenn Flappy-Bird-Spiel beendet ist

    def _go_tic_tac_toe(self):
        """                      
        Diese Funktion wird aufgerufen, wenn der Tic-Tac-Toe-Button gedrückt wird. Sie startet das Tic-Tac-Toe-Spiel, indem sie die Funktion start_Tic() aus dem TicTacToe.py Modul aufruft. Während das Tic-Tac-Toe-Spiel läuft, wird das Hauptfenster der Benutzeroberfläche ausgeblendet, um eine bessere Spielerfahrung zu ermöglichen. Sobald das Tic-Tac-Toe-Spiel beendet ist, wird das Hauptfenster wieder angezeigt.
        """
        self.__window.withdraw() # Hauptfenster ausblenden
        game_window = start_Tic(self.__window) # Tic-Tac-Toe-Spiel starten
        self.__window.wait_window(game_window) # Warten, bis das Spiel-Fenster geschlossen wird
        self.__window.deiconify() # Hauptfenster wieder anzeigen
    

    def _go_galgenraten(self):
        """
        Diese Funktion wird aufgerufen, wenn der Galgenraten-Button gedrückt wird. Sie startet das Galgenraten-Spiel, indem sie die Funktion start_galgenraten() aus dem galgenraten.py Modul aufruft. Während das Galgenraten-Spiel läuft, wird das Hauptfenster der Benutzeroberfläche ausgeblendet, um eine bessere Spielerfahrung zu ermöglichen. Sobald das Galgenraten-Spiel beendet ist, wird das Hauptfenster wieder angezeigt.
        """
        self.__window.withdraw() # Hauptfenster ausblenden
        #Galgenraten-Spiel starten
        root = tk.Toplevel(self.__window) # Neues Fenster für Galgenraten erstellen
        galgenraten = Galgenraten(root)
        
        def on_close():
            """
            Diese Funktion wird aufgerufen, wenn das Galgenraten-Fenster geschlossen wird.
            """
            root.destroy() # Galgenraten-Fenster schließen
            self.__window.deiconify() # Hauptfenster wieder anzeigen
        root.protocol("WM_DELETE_WINDOW", on_close)

    def run(self):
        """
        Diese Methode startet die Hauptschleife der Benutzeroberfläche, damit sie angezeigt wird und auf Benutzerinteraktionen reagieren kann.
        """
        self.__window.mainloop()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()