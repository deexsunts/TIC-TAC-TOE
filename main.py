
#list of imports for the project
from enum import Enum #enum has been imported to represent the names and values of specific objects in code
from random import choice# this is used for the AI choice.
from tkinter import * #tkinter imports used for buttons and game UI layout
from tkinter import ttk
from tkinter import messagebox
import os #os and sys imports are used to make teh system run more fluently. Mainly for the reset function later on shown.
import sys



gameState = None

#setting up basic stats for the game, including teh states that are already preset.
class Const(Enum):
    OFFSET = 100
    SIDE = 150
    MID = 75
    FONT = "Comic Sans MS"
    CELL_FONT_SIZE = 56
    LABEL_FONT_SIZE = 16
    WINSIZE = 650
    ROWCOL = 3
    PLAYER_CHAR = "X"
    AI_CHAR = "O"
    EMPTY_CHAR = "0"
    TURN_PLAYER = 0
    TURN_CPU = 1

#defining poinr system
class Point:
    def __init__(self, x, y, offset=0):
        self.x = x + offset
        self.y = y + offset


    def add(self, offset):
        return Point(self.x + offset, self.y + offset)


#Setting cells on board
class Cell:
    def __init__(self, canvas, i, j):
        self.canvas = canvas
        self.start = Point(i * Const.SIDE.value,
                           j * Const.SIDE.value,
                           offset=Const.OFFSET.value)
        self.mid = self.start.add(Const.MID.value)
        self.textId = "click here"
        self.marked = False
        self.marker = Const.EMPTY_CHAR.value
    
    #displaying user and ai input (X and O) on the board
    def mark(self, char):
        if self.marked:
            return False

        self.marker = char
        self.textId = self.canvas.create_text(
                           self.mid.x,
                           self.mid.y,
                           text=self.marker,
                           font=(Const.FONT.value,
                                 Const.CELL_FONT_SIZE.value))
        self.marked = True
        return True

    #defining function of user input to make an "X" on the chosen box.
    def markPlayer(self):
        return self.mark(Const.PLAYER_CHAR.value)

    #defining function of AI input to make an "o" on the chosen box.
    def markAI(self):
        return self.mark(Const.AI_CHAR.value)

    #used for deleting all presets on teh board if game has finished
    def unmark(self):
        if not self.marked:
            return False

        self.canvas.delete(self.textId)
        self.marked = False
        self.marker = Const.EMPTY_CHAR.value
        return True
    def getMarker(self):
        return self.marker



#scoring system, score card and score presets
class Score:
    #initial score are set to 0
    def __init__(self, root):
        self.playerScore = 0
        self.cpuScore = 0
        #player labels
        self.playerLabel = ttk.Label(root,
                                     font=(Const.FONT.value,
                                           Const.LABEL_FONT_SIZE.value))
        self.playerLabel.place(x=100, y=35, width=Const.SIDE.value)        
        self.cpuLabel = ttk.Label(root,
                                  font=(Const.FONT.value,
                                        Const.LABEL_FONT_SIZE.value),
                                  anchor='e')
        self.cpuLabel.place(x=400, y=35, width=Const.SIDE.value)
        self.updateScore()


    #score set on score board.
    def updateScore(self):
    
        self.playerLabel.config(text=f"username-{self.playerScore}")
        self.cpuLabel.config(text=f"Computer - {self.cpuScore}")

   

    #if player won then 1 is added to player score
    def playerWon(self):
        self.playerScore += 1
        self.updateScore()


    #if cpu won then 1 is added to cpu score
    def cpuWon(self):
        self.cpuScore += 1
        self.updateScore()

    # best of 3 for player, if player won 2 matches player wins game (displays message)
    def playergamewin(self):
     if self.playerScore==2:
      messagebox.showinfo("You won", "You won the game.")
   
    # best of 3 for AI, if AI won 2 matches AI wins game (displays message)
    def playergamewin(self):
     if self.cpuScore==2:
      messagebox.showinfo("You lost", "You lost the game.")
    






class GameState:
    #setting up game canvas
    def __init__(self, root):
        self.canvas = self.setupCanvas(root)
        self.cells = [[Cell(self.canvas, i, j) for i in range(Const.ROWCOL.value)] for j in range(Const.ROWCOL.value)]        
        self.score = Score(root)
        self.turn = Const.TURN_PLAYER.value

    #setting up grid, 3 by 3 created by 4 lines
    def setupCanvas(self, root):
        c = Canvas(root)
        c.place(x=0, y=0, height=Const.WINSIZE.value, width=Const.WINSIZE.value)
        c.create_line(250, 100, 250, 550, width=5, fill="#8B4500")
        c.create_line(400, 100, 400, 550, width=5, fill="#8B4500")
        c.create_line(100, 250, 550, 250, width=5, fill="#8B4500")
        c.create_line(100, 400, 550, 400, width=5, fill="#8B4500")
        c.bind("<Button-1>", mouseCb)
        return c

    #defining player selection , if player clicks box display "X"
    def playerSelected(self, i, j):
        valid = lambda x : 0 <= x < Const.ROWCOL.value
        if not valid(i) or not valid(j):
            return False
        return self.cells[i][j].markPlayer()

    #function used to clear the grid when it is a draw/no winner
    def clear(self, winner="none"):
        for i in range(Const.ROWCOL.value):
            for j in range(Const.ROWCOL.value):
                self.cells[i][j].unmark()

       #cases for winning possibilities, both winning and a draw
        match winner:
            case "player": self.score.playerWon()
            case "cpu": self.score.cpuWon()
            case "_": pass
        
        #determing player and AI turns during game and in between the starting of two matches
        if self.turn == Const.TURN_PLAYER.value:
            self.turn = Const.TURN_CPU.value
            self.aiTurn()
        elif self.turn == Const.TURN_CPU.value:
            self.turn = Const.TURN_PLAYER.value

    #function used for checking if a box is already taken or not
    def check(self, rowColPairs, marker):
        for (row, col) in rowColPairs:
            if (marker != self.cells[row][col].getMarker()):
                return False
        return True

   #searching for pairs in a row, (winning possibilities)
    def getColPair(self, row):
        return [(row, i) for i in range(Const.ROWCOL.value)]
        
    #searching for pairs in a column  (winning possibilities)
    def getRowPair(self, col):
        return [(i, col) for i in range(Const.ROWCOL.value)]

   #winning possibilities
    def checkWinner(self, char):
        # check for 3 in a row (horizontally)
        for row in range(Const.ROWCOL.value):
            if self.check(self.getColPair(row), char):
                return True
        # checking for 3 in a row ( vertically)
        for col in range(Const.ROWCOL.value):
            if self.check(self.getRowPair(col), char):
                return True

        # check diagonals for 3 in a row
        if self.check([(0, 0), (1, 1), (2, 2)], char):
            return True
        if self.check([(0, 2), (1, 1), (2, 0)], char):
            return True
        
        return False

    #cheking whether or not that the player positions match a winning possibility
    def checkPlayerWin(self):
        return self.checkWinner(Const.PLAYER_CHAR.value)

    #cheking whether or not that the player positions match a winning possibility
    def checkCpuWin(self):
        return self.checkWinner(Const.AI_CHAR.value)

    #caulculating remainig slots left on grid, usd to determine draw
    def getEmptySlots(self):
        slots = []
        for i in range(Const.ROWCOL.value):
            for j in range(Const.ROWCOL.value):
                if self.cells[i][j].getMarker() == Const.EMPTY_CHAR.value:
                    slots.append((i, j))
        return slots

    #if empty slots equal to 0 then the draw message will be activated
    def checkDrawn(self):
        return len(self.getEmptySlots()) == 0

    #ai turn when slots is equal to 0
    def aiTurn(self):
        slots = self.getEmptySlots()
        if len(slots) == 0:
            return
        (row, col) = choice(slots)
        self.cells[row][col].markAI()

#game selections for progress of game
def mouseCb(event):
    index = lambda x: (x - Const.OFFSET.value) // Const.SIDE.value
    j = index(event.x)
    i = index(event.y)

    if not gameState.playerSelected(i, j):
        return


    #message for if the player has won the match
    if gameState.checkPlayerWin():
        messagebox.showinfo("You won", "You won the round.")
        gameState.clear(winner="player")
        return

    gameState.aiTurn()
 #message for if the CPU has won the match
    if gameState.checkCpuWin():
        messagebox.showinfo("Cpu won", "Cpu won the round.")
        gameState.clear(winner="cpu")
        return
 #message if the game has been drawn.
    if gameState.checkDrawn():
        messagebox.showinfo("Game drawn", "The round has been drawn.")
        gameState.clear()


#restart function that closes teh application and reopens it. Tried to make one where it clears board and score.
def restart():
    os.execl(sys.executable, sys.executable, *sys.argv) #got from some guy on stack overflow


#the main UI of the game. Everything in this section is permanent on the screen and never changes.
def main():
    #setting up window characteristics.
    global gameState
    global ai
    root = Tk()
    root.title("Vishwa's Tic-tac-toe")
    root.config(bg='#F0F8FF')
    root.geometry(f"{Const.WINSIZE.value}x{Const.WINSIZE.value}+500+500")
    root.resizable(False, False)
    gameState = GameState(root)
    
    #username label on teh bottom of teh screen
    #username :)
    L1 = Label(root, text="username:")
    L1.place(x=180,y=615)
    nameinput = Entry(root, bd=4)
    nameinput.place(x=250, y=610)

    #username function used to set the user input of the entry box as the player name on score board.
    def username(root):
     username1= nameinput.get()
     label=Label(root, text= username1, font=('Comic Sans MS'))
     label.place(x=80, y=50)

    #SET USERNAME, when button is clicked it runs a function setting the username on the score board
    username_button= Button(root, text="ok",command= username )
    username_button.pack(pady=10)
    username_button.place(x=450, y=607)





    #restart button :)
    restart_button = Button(root, text="restart", command= restart)
    restart_button.pack(pady=20)
    restart_button.place(x=100, y=575)
    

    #exit button :)
    exit_button = Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=20)
    exit_button.place(x=300, y=575)
    
    
    #closing part to show that this is all prt of one main loop
    root.mainloop()



#game loop showing that all the code in this runs as one continuous program
if __name__ == "__main__":
    main()
