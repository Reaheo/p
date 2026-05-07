import turtle # Modul fuer die Grafik
import random
import time
import collections # Zum Erstellen eines Input-Buffer, wo sich Eingaben gemerkt werden für ein besseres Spielgefuehl

"""
Highscore wird in "highscore_snake.txt" gespeichert. 
In der Funktion save_highscore wird der ehemalige Eintrag ueberschrieben.
(Ist auf Linie 116 zu finden)
"""

def start_snake():
    """
    Startet das Snake-Game, indem die Hauptschleife des Spiels aufgerufen wird.
    """

    # Da alles in einer Funktion, Variablen verhalten sich manchmal komisch
    state = {
        "accepting_inputs": True, 
        "resetting": False
        }

    # Geschwindigkeit
    delay = 0.1

    # Bildschirm für das Snake-Game
    window = turtle.Screen()
    window.colormode(255)
    window.bgcolor(80,230,120)
    window.setup(width=1000, height=600)
    window.tracer(0)

    def snake_background():
        """
        Gekachelten Hintergrund generieren mit vielen Rechtecken.
        Gerade Rechtecke werden dunkler. Die For-Schleife makiert 
        das Rechteck, was zu fuellen ist, indem es dieses umrandet.
        """
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

    # Punkte
    point_variables = {"count": 0,}

    # Der Text "Punkte: " wird oben links generiert.
    points = turtle.Turtle()
    points.hideturtle()
    points.penup()
    points.goto(-350, 250)
    points.color("white")
    points.write("Punkte: ", move=False, align="center", font=("Abaddon", 20, "bold"))

    # Die Punkteanzahl wird erstmal auf "0" gesetzt und oben links hinter dem Doppelpunkt platziert.
    count_display = turtle.Turtle()
    count_display.hideturtle()
    count_display.penup()
    count_display.goto(-290, 250)
    count_display.color("white")
    count_display.write("0", move=False, align="center", font=("Abaddon", 20, "bold"))

    # Die hoechste Punktzahl wird in einer Liste gespeichert, um vorherige und aktuelle Punktestaende zu vergleichen.
    highscore = collections.deque(maxlen=2)

    # "Highscore: " wird oben recht hingeschrieben.
    highscore_label = turtle.Turtle()
    highscore_label.hideturtle()
    highscore_label.penup()
    highscore_label.goto(290, 250)
    highscore_label.color("white")
    highscore_label.write("Highscore: ", move=False, align="center", font=("Abaddon", 20, "bold"))

    # Highscore wird erstmal auf "0" gesetzt.
    highscore_points = turtle.Turtle()
    highscore_points.hideturtle()
    highscore_points.penup()
    highscore_points.goto(380, 250)
    highscore_points.color("white")
    highscore_points.write("0", move=False, align="center", font=("Abaddon", 20, "bold"))

    def find_highscore(highscore, count):
        """
        Prozedur, um mit der Liste highscore und den count, also der Punkteanzahl,
        den tatsächlichen Highscore zu ermitteln. count ist der aktuelle Punktestand
        und highscore[1] der vorherige. Gibt es keinen vorherigen, dann wird nur der
        count angehangen und als Highscore festgelegt. 
        """
        highscore.append(point_variables["count"])
        if len(highscore) == 2:
            if highscore[0] < highscore[1]:
                highscore.popleft()

            else:
                highscore.pop()

    def save_highscore(highscore):
        """
        Prozedur, um den Highscore abzuspeichern, indem man diesen in eine Textdatei einschreibt.
        """
        file = open("highscore_snake.txt", "w")
        file.write(str(highscore))
        file.close()

    def give_points(point_variables):
        """
        Prozedur, um den Punktestand zu erhoehen.
        """
        point_variables["count"] += 1
        count_display.clear()
        count_display.write(point_variables["count"], move=False, align="center", font=("Abaddon", 20, "bold"))

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
    movement_label.goto(-300,150)

    tipps_movement = turtle.Turtle()
    tipps_movement.penup()
    tipps_movement.shape(movementkeys) # Abbildung, die die Tasten darstellt und ihre Richtung
    tipps_movement.goto(-300,-150)

    # Rechts: Anzeige, die einem sagt, dass man mit der "Escape"-Taste das Spiel verlassen kann

    quit_label = turtle.Turtle()
    quit_label.penup()
    quit_label.shape(quitlabel) # Ueberschrift, die "Bewegung" liest
    quit_label.goto(300,170)

    escape_button = turtle.Turtle()
    escape_button.penup()
    escape_button.shape(escape_key) # Ueberschrift, die "Bewegung" liest
    escape_button.goto(300,-150)

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

    # Die Aepfel
    apple = turtle.Turtle()
    apple.shape(appleshape)
    apple.penup()
    apple.shapesize(stretch_wid=1,stretch_len=1)
    apple.goto(0, 60)

    # Koerperteile
    bodysegments = []

    # Spiel zuruecksetzen
    def reset():
        """
        Prozedur, um das Spielbrett zurueckzusetzten.
        """
        if state["resetting"]:  # Beugt Programmfehler vor mehrmals das Spiel zurueckzusetzen.
            return
        state["resetting"] = True
        state["accepting_inputs"] = False   # Stoppt die Aufnahme weiterer Eingaben, damit die Schlange sich nicht direkt bewegt nach "Reset"
        input_buffer.clear()    # Loescht ehemalige Eingaben zur Bewegung
        head.direction = "Stop" # Stoppt die Bewegung der Schlange
        save_highscore(point_variables["count"])    # Traegt den Highscore in die Speicher-Textdatei ein

        def cleanup():
            """
            Hilfsprozedur, um das Spielbrett aufzuräumen
            """
            for segment in bodysegments:    # Koerpersegmente werden weg bewegt, damit man sie nicht mehr sieht
                segment.goto(2000, 2000)
            bodysegments.clear()    # Dictionary der Koerpersegmente wird geleert

            head.goto(0, 0)         # Schlange wird zurueck auf 0,0 gebracht
            head.shape(head_up)

            state["resetting"] = False  # Zuruecksetzen-Variable wird auf False gesetzt, um ein erneutes Zurücksetzen wieder zu erlauben
            state["accepting_inputs"] = True # Bewegungseingaben sind wieder möglich

            point_variables["count"] = 0    # Punktestand wird auf "0" gesetzt
            count_display.clear()
            count_display.write("0", move=False, align="center", font=("Abaddon", 20, "bold"))  # Anzeige der Punkte zeigt wieder "0"

            highscore_points.clear()
            highscore_points.write(highscore[0], move=False, align="center", font=("Abaddon", 20, "bold"))  # Anzeige des Highscore ggf. auf aktuellen Stand gebracht

            

        window.ontimer(cleanup, 1000)   # Friert Fenster ein für eine Sekunde

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

        # Highscore vom Spieler anzeigen
        if len(highscore) == 0: 
            with open("highscore_snake.txt", "r") as file:  # Textdatei mit Highscore oeffnen und eingetragenen Highscore anzeigen - wenn vorhanden
                highscore_player = file.read()
                highscore_points.clear()
                highscore_points.write(highscore_player, move=False, align="center", font=("Abaddon", 20, "bold"))

        # Apfel essen
        if head.distance(apple) < 20:
            give_points(point_variables)
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
            # Das erste Koerpersegment, das direkt hinter dem Kopf, wird hier bewegt.
            x = head.xcor()
            y = head.ycor()
            bodysegments[0].goto(x,y)

        # Kollision mit Rand
        if (head.xcor() == -500) or (head.xcor() == 500) or (head.ycor() == -300) or (head.ycor() == 300):
            reset()
            find_highscore(highscore, point_variables)
        move()
        
        # Kollision mit eigenen Snake-Koerper
        for segment in bodysegments[1:]:
            if segment.distance(head) < 20:
                reset()
                find_highscore(highscore, point_variables)

        # Fuer den sehr unwahrscheinlichen Fall, dass die Schlange die maximale Laenge erreicht von 49 * 29
        if len(bodysegments) >= 1421:
            reset()

            victory = turtle.Turtle()
            victory.penup()
            victory.shape(victory_label)
            victory.goto(0,100)
            window.ontimer(victory.hideturtle, 3000)
            find_highscore(highscore, point_variables)

        time.sleep(delay)

        def beenden():
            """
            Prozedur, um das Spiel und Fenster fuer Snake zu schliessen. Es setzt den Highscore wieder auf 0, damit im naesten Spielverlauf 
            sich der Highscore nicht erniedrigen kann.
            """
            file = open("highscore_snake.txt", "w")
            file.write(str(0))
            file.close()

            nonlocal running
            running = False
            window.bye()




        window.listen()
        window.onkeypress(beenden, "Escape")

        window.update()