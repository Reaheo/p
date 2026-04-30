class account():
    def __init__(self, points=0):
        """
        Konstruktoraufruf fuer ein Konto eines Spielers
        """
        self.__points = points

    ## Getter- und Setter-Methoden
    def get_points(self) -> int:
        return self.__points
    
    def set_points(self, received_points:int):
        self.__points += received_points


class player():
    def __init__(self, name, new=False):
        """
        Konstruktoraufruf fuer beliebigen Spieler
        """
        self.__name = name
        if new:
            self.__account = account()

    ## Getter- und Setter-Methoden
    def get_name(self) -> str:
        return self.__name
    
    def set_name(self, new_name:str):
        self.__name = new_name
        
#        self.__accounts = []

#    def add_account(self, account:account):
#        self.__accounts.append(account)

class tic(player):
    def __init__(self, name:str, number=0, symbol=None, last_loser=False):
        """
        Konstruktoraufruf fuer Spieler im Spiel TicTacToe
        """
        self.__number = number
        self.__symbol = symbol
        self.__last_loser = last_loser
        super().__init__(name)

    ## Getter- und Setter-Methoden
    def get_number(self) -> int:
        return self.__number
    
    def set_number(self, new_number:int):
        self.__number = new_number
    
    def get_symbol(self) -> str:
        return self.__symbol
    
    def set_symbol(self, symbol:str):
        self.__symbol = symbol

    def get_last_loser(self) -> bool:
        return self.__last_loser
    
    def set_last_loser(self, last_loser:bool):
        self.__last_loser = last_loser

    # weitere Methoden
    def draw_symbol(self, canvas, row:int, col:int, thickness:int):
        """
        Prozedur, die das Symbol des derzeitigen Spielers in Playground zeichnet
        """
        if self.get_symbol() == "Kreuz":
            canvas.create_line(row*100+25,col*100+25, row*100+75,col*100+75, width=thickness)
            canvas.create_line(row*100+75,col*100+25, row*100+25,col*100+75, width=thickness)
        elif self.get_symbol() == "Kreis":
            canvas.create_oval(row*100+25,col*100+25, row*100+75,col*100+75, width=thickness)