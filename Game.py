import pygame
BLANK="_"
BLACK="B"
WHITE="W"
SIZE=9
class Location:
    def __init__(self, xcoord, ycoord):
        self.x=xcoord
        self.y=ycoord
    def __eq__(self, piece):
        return self.x==piece.x and self.y==piece.y
    def adj(self):
        adjs=[]
        adjs.append(Location(self.x+1, self.y))
        adjs.append(Location(self.x-1, self.y))
        adjs.append(Location(self.x, self.y+1))
        adjs.append(Location(self.x, self.y-1))
        return adjs
    def __str__(self):
        return "["+str(self.x)+", "+str(self.y)+"]"
class Piece(Location):
    def __init__(self, xcoord, ycoord, color=BLANK):
        super().__init__(xcoord, ycoord)
        self.col=color
    def location(self):
        return Location(self.x, self.y)
    def isEmpty(self):
        return self.col==BLANK
    def __str__(self):
        return self.col
class Grid:
    def __init__(self):
        self.grid=[]
        for i in range(SIZE):
            self.grid.append([])
            for j in range(SIZE):
                self.grid[i].append(Piece(i, j))
    def inGrid(self, loc):
        return loc.x>=0 and loc.x<len(self.grid) and loc.y>=0 and loc.y<len(self.grid[0])
    def change(self, loc, color):
        self.grid[loc.x][loc.y]=Piece(loc.x, loc.y, color)
    def get(self, loc):
        return self.grid[loc.x][loc.y]
    def adjacent(self, loc):
        adjacent=[]
        adjs=loc.adj()
        for i in adjs:
            if self.inGrid(i):
                adjacent.append(self.get(i))
        return adjacent
    def isValidMove(self, loc, color):
        if not self.inGrid(loc):
            return False
        if not self.get(loc).isEmpty():
            return False
        opColor=BLACK
        if color==BLACK:
            opColor=WHITE
        check=[]
        check.append(self.get(loc))
        adjs=self.adjacent(loc)
        for i in adjs:
            if i.isEmpty():
                return True
                check.append(i)
        for i in range(len(check)):
            if check[i].col!=opColor:
                adjs=self.adjacent(check[i])
                for x in adjs:
                    if x.isEmpty() and not check.__contains__(x):
                        return True
                    if not check.__contains__(x) and x.col==color:
                        check.append(x)
        return False
    def updateBoard(self, loc, color):
        adjs=self.adjacent(loc)
        opColor=BLACK
        if color==BLACK:
            opColor=WHITE
        opAdjs=[]
        for x in adjs:
            if x.col==opColor:
                opAdjs.append([x])
        for x in opAdjs:
            doBreak=False
            for i in range(len(x)):
                adjs=self.adjacent(x[i])
                for y in adjs:
                    if y.isEmpty():
                        doBreak=True
                        break
                    if y.col==opColor:
                        x.append(y)
                if doBreak:
                    break
            if not doBreak:
                for y in x:
                    self.change(y.location(), BLANK)
    def __str__(self):
        out=""
        for i in range(len(self.grid)):
            out+="  "+str(i)+" "
        out+="\n"
        for i in range(len(self.grid)):
            out+=str(i)+" "
            for j in self.grid[i]:
                out+=j.__str__()
                if j!=self.grid[i][len(self.grid[i])-1]:
                    out+=" | "
                if self.grid[i]!=self.grid[len(self.grid)-1] and j==self.grid[i][len(self.grid[i])-1]:
                    out+="\n  "+"--+-"*(len(self.grid[i])-1)+"-\n"
        return out
class Player:
    def __init__(self, inName, color):
        self.name=inName
        self.col=color
    def makeMove(self, board, loc):
        board.change(loc, self.col)
class Human(Player):
    def __init__(self, inName, color):
        super().__init__(inName, color)
        self.pas="no"
    def move(self, board):
        self.pas=input("Would you like to pass? ")
        if self.pas!="yes":
            x=int(input("X: "))
            y=int(input("Y: "))
            while not board.isValidMove(Location(x, y), self.col):
                print("Invalid move!")
                x=int(input("X: "))
                y=int((input("Y: ")))
            self.makeMove(board, Location(x, y))
            board.updateBoard(Location(x,y), self.col)
class Main:
    def playGame():
        board=Grid()
        p1=Human(input("Player 1: "), BLACK)
        p2=Human(input("Player 2: "), WHITE)
        while not (p1.pas=="yes" and p2.pas=="yes"):
            print(board)
            print(f"{p1.name}'s turn!")
            p1.move(board)
            print(board)
            if not (p1.pas=="yes" and p2.pas=="yes"):
                print(f"{p2.name}'s turn!")
                p2.move(board)
        print("Game over!")
Main.playGame()