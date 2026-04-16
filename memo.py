class memo():
    def __init__(self):
        """
        Konstruktoraufruf fuer Speicher des Felds (Belegung) von TicTacToe
        """
        # dabei muss noch nichts 
        pass

    ## Getter- und Setter-Methoden
    # Tabellenbelegung
    def get_table(self) -> list:
        return self.__table
    
    def get_player(self) -> int:
        return self.__table[self.__row][self.__col]
    
    # aktuelle (Zug-) Zeile, Spalte, Feld
    def set_row(self, row:int):
        self.__row = row

    def set_col(self, col:int):
        self.__col = col

    def get_row(self) -> int:
        return self.__row

    def get_col(self) -> int:
        return self.__col

    def get_field(self) -> str:
        return str(self.__row) + str(self.__col)
    
    ## Daten loeschen, auf Anfang setzen
    def clear(self):
        """
        Prozedur, die den Speicher in seinen Anfangszustand versetzt
        """
        # 3x3-Feld zeilenweise; Belegung -> 0:keiner, 1:Spieler1, 2:Spieler2
        self.__table = [[0,0,0],[0,0,0],[0,0,0]]
        # moegliche 3er-Reihen mit Indizes von table als "ZeileSpalte"
        self.__lines = [[["00",0],["01",0],["02",0],0],
                        [["10",0],["11",0],["12",0],0],
                        [["20",0],["21",0],["22",0],0],
                        [["00",0],["10",0],["20",0],0],
                        [["01",0],["11",0],["21",0],0],
                        [["02",0],["12",0],["22",0],0],
                        [["00",0],["11",0],["22",0],0],
                        [["02",0],["11",0],["20",0],0]]
        self.__completed_lines = 0
    
    ## Spielfeldbelegung: Speichern & Pruefen
    def check_full(self, line:list,player_number:int) -> bool:
        """
        Funktion, die ueberprueft, ob vollstaendige Reihe (line) von einem einzigen Spieler belegt wird (True)
        """
        for each_field in range(3):
            if player_number != line[each_field][1]:
                return False
        return True
    
    def set_memo(self, player_number:int) -> bool:
        """
        Funktion, die Zug speichert & zurueckgibt, ob Gewinn (True)
        """
        self.__table[self.__row][self.__col] = player_number
        for line in range(len(self.__lines)-self.__completed_lines):
            for search_field in range(3):
                if self.__lines[line][search_field][0] == self.get_field():
                    self.__lines[line][search_field][1] = player_number
                    self.__lines[line][3] += 1
                    if self.__lines[line][3] == 3:
                        if self.check_full(self.__lines[line],player_number):
                            return True
                        self.__lines[line], self.__lines[len(self.__lines)-self.__completed_lines-1] = self.__lines[len(self.__lines)-self.__completed_lines-1], self.__lines[line]
                        self.__completed_lines += 1
        return False

