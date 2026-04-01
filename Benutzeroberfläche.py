import tkinter as tk 
from snake import start_snake

class GameLauncher:
    """
    Die Klasse GameLauncher repräsentiert die Hauptbenutzeroberfläche für die Minispiele. 
    """

    def __init__(self):
        """
        konstruktor der Klasse GameLauncher
        """
        self.window = tk.Tk()
        self.window.title("Minispiele")
        self.window.geometry("1200x800")
        self.window.config(bg="lightblue")

        # Bild Speichern
        self.images = {}

        # Spiele definieren
        self.games = [("SNAKE", "snake_picture.png", self.go_snake, 2),("Tic-Tac-Toe", "tic_picture.png", None, 3), ("Galgenraten", "galgenraten_picture.png", None, 3), ("4-Gewinnt", "4-gewinnt_picture.png", None, 3)]
        self.create_buttons()
        self.create_close_button()

    def create_buttons(self):
        """
        Die Methode erstellt die Buttons für die Minispiele automatisch
        """
        for i, (name, image_path, command, scale) in enumerate(self.games):
            row = i // 4
            col = i % 4 
            image = self.load_image(image_path, scale) if image_path else None
            button = tk.Button(self.window, text=name, image=image, compound="top", width=170, height=200, anchor="s", pady=10, command=command)
            button.grid(column=col, row=row, padx=30, pady=30)  
            button.config(font=("Arial", 12), bd=5)

    def create_close_button(self):
        """
        Die Methode erstellt den Beenden-Button
        """
        button_close = tk.Button(self.window, text= "Beenden", command= self.window.quit)
        button_close.grid(column=4, row=10, pady= 15, padx=10)
        button_close.config(bg="blue", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=5)

    def load_image(self, path, scale):
        """
        Die Methode lädt ein Bild und speichert es in einem Dictionary, um zu verhindern, dass es von der Garbage Collection gelöscht wird.
        """
        if path not in self.images:
            self.images[path] = tk.PhotoImage(file=path)
        return self.images[path]   

        if scale: img = img.subsample(scale, scale)
        return img     

    def go_snake(self):
        """
        Diese Funktion wird aufgerufen, wenn der Snake-Button gedrückt wird. Sie startet das Snake-Spiel, indem sie die Funktion start_snake() aus dem snake.py Modul aufruft. Während das Snake-Spiel läuft, wird das Hauptfenster der Benutzeroberfläche ausgeblendet, um eine bessere Spielerfahrung zu ermöglichen. Sobald das Snake-Spiel beendet ist, wird das Hauptfenster wieder angezeigt.
        """
        self.window.withdraw() # Hauptfenster ausblenden
        start_snake() # Snake-Spiel starten
        self.window.deiconify() # Hauptfenster wieder anzeigen, wenn Snake-Spiel beendet ist

    def run(self):
        """
        Diese Methode startet die Hauptschleife der Benutzeroberfläche, damit sie angezeigt wird und auf Benutzerinteraktionen reagieren kann.
        """
        self.window.mainloop()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()