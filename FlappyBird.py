from tkinter import *
import random


def start_flappy_bird(parent):
    """
    Startet das Flappy-Bird-Spiel, indem die Hauptschleife des Spiels aufgerufen wird.
    """

    #Benutzerfenster
    Form_flappy_bird = Toplevel(parent)
    Form_flappy_bird.title("Flappy Bird")
    Form_flappy_bird.geometry("1200x800")
    Form_flappy_bird.configure(bg="skyblue")
    Form_flappy_bird.resizable(False, False)

    #Spielrahmen
    canvas_width = 1000
    canvas_height = 600
    game_canvas = Canvas(Form_flappy_bird, 
                         width=canvas_width, 
                         height=canvas_height,
                         bg="skyblue", 
                         highlightthickness=0)
    game_canvas.pack(padx=20, pady=20)

    # Punktestand
    score_label = Label(Form_flappy_bird, 
                        text="Punkte: 0",
                        font=("Arial", 18), 
                        bg="skyblue")
    score_label.pack(anchor="nw", padx=30)

    # Boden
    ground = game_canvas.create_rectangle(0, 
                                          canvas_height - 50, 
                                          canvas_width, 
                                          canvas_height,
                                          fill="#8B4513")

    # Vogel
    bird_radius = 20
    bird_x = 180
    bird_y = canvas_height // 2

    bird = game_canvas.create_oval(bird_x - bird_radius, 
                                   bird_y - bird_radius,bird_x + bird_radius, 
                                   bird_y + bird_radius,
                                   fill="yellow")

    gravity = 0.8
    velocity = 0
    flap_strength = -10

    #Rohre
    pipe_speed = 5
    pipe_gap = 180
    pipe_width = 80
    pipe_distance = 300

    pipes = []
    score = 0
    game_running = True
    game_started = False
    game_over_text = None
    restart_button = None
    instruction_text = None

    def create_pipe(x):
        """
        Erstellt ein neues Rohrpaar (oben und unten) an der angegebenen x-Position.
        """
        gap_y = random.randint(150, canvas_height - 250)

        top = game_canvas.create_rectangle(x, 
                                           0, 
                                           x + pipe_width, 
                                           gap_y,fill="green")

        bottom = game_canvas.create_rectangle(x, gap_y + pipe_gap, 
                                              x + pipe_width, 
                                              canvas_height - 50, 
                                              fill="green")

        pipes.append({"top": top, "bottom": bottom, "x": x, "passed": False})

    def reset_game():
        """
        Setzt das Spiel zurück, indem alle Variablen und Grafiken auf ihre Anfangswerte zurückgesetzt werden.
        """
        nonlocal velocity, score, game_running, game_started, game_over_text, restart_button

        velocity = 0
        score = 0
        game_running = True
        game_started = False

        score_label.config(text="Punkte: 0")

        game_canvas.coords(bird, 
                           bird_x - bird_radius, 
                           canvas_height // 2 - bird_radius, 
                           bird_x + bird_radius, 
                           canvas_height // 2 + bird_radius)

        if game_over_text is not None:
            game_canvas.delete(game_over_text)
            game_over_text = None
        
        if restart_button is not None:
            restart_button.destroy()
            restart_button = None

        for pipe in pipes:
            game_canvas.delete(pipe["top"])
            game_canvas.delete(pipe["bottom"])
        pipes.clear()

        initialize_pipes()
        update_game()

    def initialize_pipes():
        """
        Erstellt die ersten Rohre zu Beginn des Spiels.
        """
        for i in range(4):
            create_pipe(canvas_width + i * pipe_distance)

    def collide(a, b):
        """
        Überprüft auf Kollision
        """
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


    def game_over():
        """
        Beendet das Spiel, zeigt eine "Game Over"-Nachricht an und bietet die Möglichkeit zum Neustart.
        """
        nonlocal game_running, game_over_text, restart_button
        game_running = False

        game_over_text = game_canvas.create_text(canvas_width // 2, 
                                canvas_height // 2,
                                text="GAME OVER",
                                fill="red",
                                font=("Arial", 36, "bold"))

        restart_button = Button(Form_flappy_bird, 
                                text="Neustart",
                                command=reset_game)
        restart_button.pack(pady=10)

    def update_game():
        """
        Aktualisiert die Positionen aller Spielobjekte, überprüft Kollisionen und verwaltet den Spielablauf.
        """
        nonlocal velocity, score

        if not game_running:
            return

        if game_started:
            velocity += gravity
            game_canvas.move(bird, 0, velocity)

        bird_coords = game_canvas.coords(bird)

        # Boden/Decke
        if bird_coords[1] <= 0 or bird_coords[3] >= canvas_height - 50:
            game_over()
            return

        if game_started:
            for pipe in list(pipes):
                game_canvas.move(pipe["top"], -pipe_speed, 0)
                game_canvas.move(pipe["bottom"], -pipe_speed, 0)
                pipe["x"] -= pipe_speed

                if not pipe["passed"] and pipe["x"] + pipe_width < bird_x:
                    pipe["passed"] = True
                    score += 1
                    score_label.config(text=f"Punkte: {score}")

                if pipe["x"] + pipe_width < 0:
                    game_canvas.delete(pipe["top"])
                    game_canvas.delete(pipe["bottom"])
                    pipes.remove(pipe)

            if pipes and pipes[-1]["x"] < canvas_width - pipe_distance:
                create_pipe(canvas_width)

            for pipe in pipes:
                if collide(bird_coords, game_canvas.coords(pipe["top"])) or \
                   collide(bird_coords, game_canvas.coords(pipe["bottom"])):
                    game_over()
                    return

        Form_flappy_bird.after(20, update_game)

    def flap(event=None):
        """
        Lässt den Vogel Fliegen und mithilfe der Bindung der Tasten durch Space und Pfeil nach oben, kann der Spieler den Vogel steuern.
        """
        nonlocal velocity, game_started, instruction_text
        if game_running:
            if not game_started:
                game_started = True
                velocity = 0
                if instruction_text is not None:
                    game_canvas.delete(instruction_text)
                    instruction_text = None
            velocity = flap_strength

    def close():
        """
        Beendet das Spiel und schließt das Fenster.
        """
        nonlocal game_running
        game_running = False
        Form_flappy_bird.destroy()

    # Steuerung
    Form_flappy_bird.bind("<space>", flap)
    Form_flappy_bird.bind("<Up>", flap)

    Form_flappy_bird.protocol("WM_DELETE_WINDOW", close)

    # Start
    initialize_pipes()
    
    instruction_text = game_canvas.create_text(canvas_width // 2, 
                                               canvas_height // 2 - 50,
                                               text="mithilfe der Leertaste oder ↑ kannst du den Vogel steuern, viel spaß :)",
                                               fill="black",
                                               font=("Arial", 20, "bold"),
                                               width=500)
    
    update_game()

    return Form_flappy_bird