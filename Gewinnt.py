from tkinter import*

def vier_gewinnt(parent):
    Form_4gewinnt = Toplevel(parent)
    canvas = Canvas(Form_4gewinnt,width=565,height=500,bg="brown")
    canvas.place(x=200,y=5)

    s=0
    Spielfeld=[[],[],[],[],[],[],[],[0,0,0,0,0,0,0]] #Felder 0-6:Spalten des Spielfeldes, Feld 7: länge der einzelnen Spalten
    loop=True
    spieler=True
    colour="orange"

    def eingabe1(): 
        """
        Dies ist das Hauptprogramm 
        """
         
        nonlocal s
        nonlocal Spielfeld
        nonlocal spieler
        nonlocal colour

        loop=True
        #1. Eingabe holen
        s=int(Eingabe_p1.get())-1 #Auslesen des Eingabe Feldes und Speicherung in s
        
        #2. Stein logisch hinzufügen
        anhängen(spieler) #Aufrufen der Prozedur anhängen
        
        #3. Stein grafisch hinzufügen
        canvas.create_oval(30+75*s,
                           36+75*(6-Spielfeld[7][s]),
                           90+75*s,96+75*(6-Spielfeld[7][s]), 
                           outline = "black", 
                           fill = colour ,
                           width = 2) # Erzeugung Speilstein
        
        #4. Prüfen ob Spieler gewonnen hat
        if prüfvertikal()==False or prüfhorizontal()==False or prüfdiagonal()==False: #Aufrufen der Prüfprozeduren und Prüfung ob 4 in einer Reihe vorliegen
            print("gewonnen")
        #5. Spielerwechsel
        spielerwechsel() #Aufrufen der Prozedur spielerwechsel 
        


    def anhängen(spieler_wert):
        """
        anhängen der ausgewählten Spalte an Spielfeld
        """
        nonlocal Spielfeld, s

        if len(Spielfeld[s])<6: #wenn die Spalte noch nicht voll ist:
            Spielfeld[s].append(spieler_wert) #Wert des Spielers wird an Spielfeld in unter Feld der ausgewählten Spalte angehängt
            Spielfeld[7][s]=Spielfeld[7][s]+1 #Länge der Spalte aktualisieren
            
        
    def spielerwechsel():
        """
        Wechseln des Wertes des Spielers
        """
        nonlocal spieler
        nonlocal colour
        if spieler==True: #Änderung des Spielers in gegensätzlichen Wert 
            spieler=False
            colour="blue"#Änderung Farbe Spielstein
        else:
            spieler=True
            colour="orange"
        print("Nächster spieler ist dran:", colour)
        

    def prüfvertikal():  
        nonlocal spieler
        nonlocal Spielfeld
        nonlocal s
        nonlocal loop
        c=0
        length=len(Spielfeld[s])
        if length>=4: #wenn die Länge größer als vier ist 
            for i in range (length, 0 ,-1): #Spalte von neuen Stein bis letzten Stein durchgehen
                
                length=length-1
                if Spielfeld[s][length]==spieler:
                    c=c+1
                else:
                    loop=True
                    return loop
    
                if c==4:
                    loop=False
                    return loop
        else:
            loop=True
            return loop
        
        """
        prüfen ob 4 gleiche Steine vertikal in einer Reihe liegen
        """
    def prüfhorizontal():
        nonlocal spieler
        nonlocal Spielfeld
        nonlocal s
        nonlocal loop
        le=Spielfeld[7][s]
        c=1
        for i in range(s-1,-1,-1): #Spalten von ausgewählten Stein zu rechten Rand durchgehen
            if le>Spielfeld[7][i]: #wenn eine darrauffolgende Spalte kleiner als die gegebene ist
                break
            if Spielfeld[i][le-1]==spieler:
                c=c+1
            else:
                break
            if c==4:
                loop=False
                return loop
            
        for i in range(s+1,7):
            if le>Spielfeld[7][i]:
                break
            if Spielfeld[i][le-1]==spieler:
                c=c+1
            else:
                break
            if c==4:
                loop=False
                return loop
        """
        prüfen ob 4 gleiche Steine horizontal in einer Reihe liegen
        """

    def prüfdiagonal():
        nonlocal spieler
        nonlocal Spielfeld
        nonlocal s
        nonlocal loop
        le=Spielfeld[7][s] 
        l=le
        c=1
        #recht nach oben
        if s<7 and le<Spielfeld[7][s+1]: #wenn neuer Stein nicht an Kante von Feld ist und der daruffolgende Stein über neuen liegt
            for b in range(s+1,7): #geht Steine von neuen Stein bis Kante durch
                l=l+1 #erhöhung Höhe des nächsten Steins
                if l<=6 and l<=Spielfeld[7][b]: #wenn neue benötigte Höhe geringer als max. Höhe und die zu betrachtende Reihe die voraus gesetzte Höhe besitzt
                    if Spielfeld[b][l-1]==spieler:
                        c=c+1
                    else:
                        break
                else:
                    break
        #rechts nach unten
        l=le
        if s<7 and le<=Spielfeld[7][s+1]+1: #wenn neuer Stein nicht an Kante von Feld ist und der darauffolgende Stein über,neben oder eins unter dem jetzigen Stein liegt
            for b in range(s+1,7): #geht von neuen Stein bis Kante durch
                l=l-1 #veringerung Höhe des nächsten Steins
                if l>=1 and l<=Spielfeld[7][b]:
                    if Spielfeld[b][l-1]==spieler:
                        c=c+1
                    else:
                        break
                else:
                    break

        #liks nach oben
        l=le
        if s>0 and le<Spielfeld[7][s-1]: #wenn neuer Stein nicht an Kante von Feld ist und der vorhergehende Stein über neuen liegt
            for b in range(s-1,0,-1): #geht Steine von neuen Stein bis Kante durch
                l=l+1 #erhöhung Höhe des nächsten Steins
                if l<=6 and l<=Spielfeld[7][b]: #wenn neue benötigte Höhe geringer als max. Höhe und die zu betrachtende Reihe die voraus gesetzte Höhe besitzt
                    if Spielfeld[b][l-1]==spieler:
                        c=c+1
                    else:
                        break
                else:
                    break
        #links nach unten
        l=le
        if s>0 and le<=Spielfeld[7][s-1]+1: #wenn neuer Stein nicht an Kante von Feld ist und der nachfolgende Stein über,neben oder eins unter dem jetzigen Stein liegt
            for b in range(s-1,0,-1): #geht von neuen Stein bis Kante durch
                l=l-1 #veringerung Höhe des nächsten Steins
                if l>=1 and l<=Spielfeld[7][b]: #wenn neue benötigte Höhe höher als minimal höhe und die zu betrachtende Reihe die voraus gesetzte Höhe besitzt 
                    if Spielfeld[b][l-1]==spieler:
                        c=c+1
                    else:
                        break
                else:
                    break

        if c>=4:
                loop=False
                return loop
        """
        prüfen ob 4 gleiche Steine horizontal in einer Reihe liegen
        """

    #Formular 
    Form_4gewinnt.title("4 Gewinnt")
    Form_4gewinnt.geometry("1000x600")
    Form_4gewinnt.option_add("*front","Arial 14")
    Form_4gewinnt.config(bg="brown")


    #Raster erstellen
    canvas.create_rectangle(10,10,565,500,outline = "black", fill = "grey",width = 2)
    for z in range(0,6):
        for i in range(0,7):
            canvas.create_oval(30+75*i,36+75*z,90+75*i,96+75*z,outline = "black", fill = "white",width = 2)
        
    #Eingabefelder   
    Eingabe_p1 = Entry(master= Form_4gewinnt)
    Eingabe_p1.place(x=10,y=100,width=100,height=30)

    #Schaltflächen 
    ButtonEingabe= Button(master=Form_4gewinnt, text="Eingabe bestätigen", command=eingabe1)
    ButtonEingabe.place(x=10,y=180, width=100, height=30)

    def close_window(event=None):
        """Beendet das Spiel und schließt das Fenster."""
        Form_4gewinnt.destroy()

    Form_4gewinnt.protocol("WM_DELETE_WINDOW", close_window)
    Form_4gewinnt.bind("<Escape>", close_window)

    canvas.pack()

    return Form_4gewinnt
