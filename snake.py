import turtle # Modul fuer die Grafik
import random
import time
import collections # Zum Erstellen eines Input-Buffer, wo sich Eingaben gemerkt werden für ein besseres Spielgefuehl

def start_snake():
    """
    Startet das Snake-Game, indem die Hauptschleife des Spiels aufgerufen wird.
    """

    # Da alles in einer Funktion, Variablen verhalten sich manchmal komisch
    state = {"accepting_inputs": True, "resetting": False}
    running = True

    # Geschwindigkeit
    delay = 0.1

    # Bildschirm für das Snake-Game
    window = turtle.Screen()
    window.colormode(255)
    window.bgcolor(80,230,120)

    def close_snake():
        nonlocal running
        if running:
            running = False
            window.bye()

    window.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", close_snake)
    window.setup(width=1000, height=600)
    window.tracer(0)

    def snake_background():
        grid = turtle.Turtle()
        grid.hideturtle()
        grid.penup()
        grid.speed(0)
        grid.shape("square")

        color_one = (95, 195, 90)
        color_two = (108, 202, 104)

        for x in range(-510, 511, 20):
            for y in range(-310, 311, 20):
                if (x // 20 + y // 20) % 2 == 0:
                    grid.fillcolor(color_one)
                else:
                    grid.fillcolor(color_two)

                grid.goto(x, y)
                grid.begin_fill()
                for _ in range(4):
                    grid.forward(20)
                    grid.left(90)
                grid.end_fill()
        
    snake_background()

    # Bilder bzw. Formen
    appleshape = "Aepfel.gif"
    window.addshape(appleshape)

    movementlabel = "Bewegung.gif"
    window.addshape(movementlabel)

    movementkeys = "wasd.gif"
    window.addshape(movementkeys)

    quitlabel = "Verlassen.gif"
    window.addshape(quitlabel)

    escape_key = "Esc.gif"
    window.addshape(escape_key)

    victory_label = "Victory.gif"
    window.addshape(victory_label)

    # Links: Anzeige mit welchen Tasten man sich bewegt. Soll nach einer gewissen Zeit verschwinden
    movement_label = turtle.Turtle()
    movement_label.penup()
    movement_label.shape(movementlabel) # Überschrift, die "Bewegung" liest
    movement_label.goto(-300,200)

    tipps_movement = turtle.Turtle()
    tipps_movement.penup()
    tipps_movement.shape(movementkeys) # Abbildung, die die Tasten darstellt und ihre Richtung
    tipps_movement.goto(-300,-100)

    # Rechts: Anzeige, die einem sagt, dass man mit der "Escape"-Taste das Spiel verlassen kann

    quit_label = turtle.Turtle()
    quit_label.penup()
    quit_label.shape(quitlabel) # Ueberschrift, die "Bewegung" liest
    quit_label.goto(300,200)

    escape_button = turtle.Turtle()
    escape_button.penup()
    escape_button.shape(escape_key) # Ueberschrift, die "Bewegung" liest
    escape_button.goto(300,-100)

    def disable_tipps():
        # Prozedur, damit wenn eine die Schlange beginnt sich zu bewegen, die eingeblendeten Bilder verschwinden
        global deleted
        deleted = False
        if deleted == False:    
            tipps_movement.hideturtle()
            movement_label.hideturtle()
            quit_label.hideturtle()
            escape_button.hideturtle()
        deleted = True # Wiederholt die Prozedur nach Start nicht nochmal
 
    # Schlangengrafik
    head_up = "snakehead_up.gif"
    head_down = "snakehead_down.gif"
    head_left = "snakehead_left.gif"
    head_right = "snakehead_right.gif"
    body = "snakebody.gif"
    window.addshape(head_up)
    window.addshape(head_down)
    window.addshape(head_left)
    window.addshape(head_right)
    window.addshape(body)

    # Der Kopf der Schlange
    head = turtle.Turtle()
    head.color("black")
    head.shape(head_up)
    head.goto(0,0)
    head.penup()
    head.direction = "Stop"

    # Input Buffer
    input_buffer = collections.deque(maxlen=2) # Warteschlange, die maximal zwei Elemente haelt und pro Frame eins abarbeite

    # Bewegungsfunktionen
    def move():
        """
        Der Kopf bewegt sich in Richtung seiner Ausrichtung head.direction. Hier wird die Bewegung
        bei jeweiliger Ausrichtung gemacht, indem die y-Koordinate oder x-Koordinate veraendert wird.
        """
        if head.direction == "up":
            head.sety(head.ycor() + 20)
            head.shape(head_up)
        if head.direction == "down":
            head.sety(head.ycor() - 20)
            head.shape(head_down)
        if head.direction == "right":
            head.setx(head.xcor() + 20)
            head.shape(head_right)
        if head.direction == "left":
            head.setx(head.xcor() - 20)
            head.shape(head_left)

        # Ausrichtung des Kopfes
    def upward():
        if state["accepting_inputs"] == False:
            return
        input_buffer.append("up")
        disable_tipps()
    def downward():
        if state["accepting_inputs"] == False:
            return
        input_buffer.append("down")
        disable_tipps()
    def rightward():
        if state["accepting_inputs"] == False:
            return
        input_buffer.append("right")
        disable_tipps()
    def leftward():
        if state["accepting_inputs"] == False:
            return
        input_buffer.append("left")
        disable_tipps()

    # Bewegungstasten
    window.listen()
    window.onkeypress(upward, "w")
    window.onkeypress(downward, "s")
    window.onkeypress(rightward, "d")
    window.onkeypress(leftward,"a")

    def beenden():
        nonlocal running
        running = False
        window.bye()

    window.onkeypress(beenden, "Escape")

    # Die Aepfel
    apple = turtle.Turtle()
    apple.shape(appleshape)
    apple.penup()
    apple.shapesize(stretch_wid=1,stretch_len=1)
    apple.goto(0, 100)

    # Koerperteile
    bodysegments = []

    # Spiel zuruecksetzen
    def reset():
        if state["resetting"]:
            return
        state["resetting"] = True
        state["accepting_inputs"] = False
        input_buffer.clear()
        head.direction = "Stop"

        def cleanup():
            for segment in bodysegments:
                segment.goto(2000, 2000)
            bodysegments.clear()

            head.goto(0, 0)
            head.shape(head_up)

            state["resetting"] = False
            state["accepting_inputs"] = True

        window.ontimer(cleanup, 1000)

    # Haupt Spielschleife
    running = True
    while running:
        last_direction = head.direction 

        # Input Buffer
        opposites = {"up": "down", "down" : "up", "right": "left", "left": "right"}

        while input_buffer:
            next_direction = input_buffer.popleft()
            if opposites.get(next_direction) != last_direction: # opposites.get statt opposites[next_direction], weil "Stop" kein Element ist
                head.direction = next_direction
                break

        # Apfel essen
        if head.distance(apple) < 20:
            while True:
                # Wenn der Abstand vom Apfel weniger ist als ein Kaestchen, dann wird dieser gegessen
                apple.goto(random.randint(-24,24)*20,random.randint(-14,14)*20)
                if not any(apple.position() == segment.position() for segment in bodysegments):
                    apple.goto(random.randint(-24,24)*20,random.randint(-14,14)*20)
                    break

            # Die Schlange wird laenger durch das Essen eines Apfels
            new_bodysegment = turtle.Turtle()
            new_bodysegment.shape(body)
            new_bodysegment.penup()
            new_bodysegment.direction = head.direction
            new_bodysegment.speed(0)
            bodysegments.append(new_bodysegment)

        for i in range(len(bodysegments)-1, 0, -1):
            """
            Vom letzten Körperteil nach vorne wird die x- 
            und y-Koordinate auf das davor liegende gesetzt 
            und dort bewegt sich es auch hin.

            Koerperteil 4 wuerde sich auf 4 - 1 bewegen, also 3 usw.
            """ 
            x = bodysegments[i-1].xcor()
            y = bodysegments[i-1].ycor()
            bodysegments[i].goto(x,y)

        if len(bodysegments) > 0:
            # Das erste Koerpersegment, nicht gleich der Kopf, wird hier bewegt.
            x = head.xcor()
            y = head.ycor()
            bodysegments[0].goto(x,y)

        # Kollision mit Rand
        if (head.xcor() == -500) or (head.xcor() == 500) or (head.ycor() == -300) or (head.ycor() == 300):
            reset()

        move()
        
        # Kollision mit eigenen Snake-Koerper
        for segment in bodysegments:
            if segment.distance(head) < 20:
                reset()

        # Fuer den sehr unwahrscheinlichen Fall, dass die Schlange die maximale Laenge erreicht von 49 * 29
        if len(bodysegments) >= 1421:
            reset()

            victory = turtle.Turtle()
            victory.penup()
            victory.shape(victory_label)
            victory.goto(0,100)
            window.ontimer(victory.hideturtle, 3000)

        time.sleep(delay)
        window.update()