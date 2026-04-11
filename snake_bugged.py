import turtle # Modul für die Grafik
import random
import time
import collections # Zum Erstellen eines Input-Buffer, wo sich Eingaben gemerkt werden für ein besseres Spielgefühl

def start_snake():
    """
    Startet das Snake-Game, indem die Hauptschleife des Spiels aufgerufen wird.
    """
    # Geschwindigkeit
    delay = 0.05

    # Bildschirm für das Snake-Game
    window = turtle.Screen()
    window.colormode(255)
    window.bgcolor(80,230,120)
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
    quit_label.shape(quitlabel) # Überschrift, die "Bewegung" liest
    quit_label.goto(300,200)

    escape_button = turtle.Turtle()
    escape_button.penup()
    escape_button.shape(escape_key) # Überschrift, die "Bewegung" liest
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
    window.addshape(head_up)
    window.addshape(head_down)
    window.addshape(head_left)
    window.addshape(head_right)

    # Der Kopf der Schlange
    head = turtle.Turtle()
    head.color("black")
    head.shape(head_up)
    head.goto(0,0)
    head.penup()
    head.direction = "Stop"

    # Input Buffer
    input_buffer = collections.deque(maxlen=2) # Warteschlange, die maximal zwei Elemente hält und pro Frame eins abarbeitet

    def enable_inputs():
        global accepting_inputs
        accepting_inputs = True

    # Bewegungsfunktionen
    def move():
        """
        Der Kopf bewegt sich in Richtung seiner Ausrichtung head.direction. Hier wird die Bewegung
        bei jeweiliger Ausrichtung gemacht, indem die y-Koordinate oder x-Koordinate verändert wird.
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
    accepting_inputs = True
    def upward():
        if accepting_inputs == False:
            return
        input_buffer.append("up")
        disable_tipps()
    def downward():
        if accepting_inputs == False:
            return
        input_buffer.append("down")
        disable_tipps()
    def rightward():
        if accepting_inputs == False:
            return
        input_buffer.append("right")
        disable_tipps()
    def leftward():
        if accepting_inputs == False:
            return
        input_buffer.append("left")
        disable_tipps()

    # Bewegungstasten
    window.listen()
    window.onkeypress(upward, "w")
    window.onkeypress(downward, "s")
    window.onkeypress(rightward, "d")
    window.onkeypress(leftward,"a")

    # Die Äpfel
    apple = turtle.Turtle()
    apple.shape(appleshape)
    apple.penup()
    apple.shapesize(stretch_wid=1,stretch_len=1)
    apple.goto(0, 100)

    # Körperteile
    bodysegments = []

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
                # Wenn der Abstand vom Apfel weniger ist als ein Kästchen, dann wird dieser gegessen
                apple.goto(random.randint(-24,24)*20,random.randint(-14,14)*20)
                if not any(apple.position() == segment.position() for segment in bodysegments):
                    apple.goto(random.randint(-24,24)*20,random.randint(-14,14)*20)
                    break

            # Die Schlange wird länger durch das Essen eines Apfels
            new_bodysegment = turtle.Turtle()
            new_bodysegment.shape("square")
            new_bodysegment.penup()
            new_bodysegment.color("grey")
            new_bodysegment.direction = head.direction
            new_bodysegment.speed(0)
            bodysegments.append(new_bodysegment)

        for i in range(len(bodysegments)-1, 0, -1):
            """
            Vom letzten Körperteil nach vorne wird die x- 
            und y-Koordinate auf das davor liegende gesetzt 
            und dort bewegt sich es auch hin.

            Körperteil 4 würde sich auf 4 - 1 bewegen, also 3 usw.
            """ 
            x = bodysegments[i-1].xcor()
            y = bodysegments[i-1].ycor()
            bodysegments[i].goto(x,y)

        if len(bodysegments) > 0:
            # Das erste Körpersegment, nicht gleich der Kopf, wird hier bewegt.
            x = head.xcor()
            y = head.ycor()
            bodysegments[0].goto(x,y)

        # Kollision mit Rand
        if (head.xcor() == -500) or (head.xcor() == 500) or (head.ycor() == -300) or (head.ycor() == 300):
            head.direction = "Stop"
            time.sleep(1)

            for segment in bodysegments:
                    segment.goto(2000, 2000)

            bodysegments.clear()
            head.goto(0,0)

            accepting_inputs = False
            input_buffer.clear()
            window.ontimer(enable_inputs, 1000)



        move()
    
        
        # Kollision mit eigenen Snake-Körper
        for segment in bodysegments:
            if segment.distance(head) < 20:
                head.direction = "Stop"
                time.sleep(1)
            
                for segment in bodysegments:
                    segment.goto(2000, 2000)

                bodysegments.clear()
                head.goto(0,0)

                accepting_inputs = False
                input_buffer.clear()
                window.ontimer(enable_inputs, 1000)
                 
                

        # Für den sehr unwahrscheinlichen Fall, dass die Schlange die maximale Länge erreicht von 49 * 29, also das, was das Fenster halten kann.
        if len(bodysegments) >= 1421:
            head.direction = "Stop"
            time.sleep(1)
            
            for segment in bodysegments:
                segment.goto(2000, 2000)

            bodysegments.clear()
            head.goto(0,0)

            accepting_inputs = False
            input_buffer.clear()
            window.ontimer(enable_inputs, 1000)

            victory = turtle.Turtle()
            victory.penup()
            victory.shape(victory_label) # Überschrift, die "Bewegung" liest
            victory.goto(0,100)
            window.ontimer(victory.hideturtle, 3000)

        time.sleep(delay)

        def beenden():
            nonlocal running
            running = False
            window.bye()

        window.listen()
        window.onkeypress(beenden, "Escape")

        window.update()

        """
        Statt time.sleep() eine Funktion einfügen die einen Reset durchführt. Ein Hilfsfunktion, die alle Vörgänge durchführt, 
        die bisher einzel stehen wäre hilfreich

        """