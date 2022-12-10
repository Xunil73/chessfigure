#!/usr/bin/env python3


###############################################################################

# Anmerkung zum weiteren Programm

# ab rev7 haben Objekte Kenntnis von den anderen Objekten und leiten daraus
# mögliche Züge ab. Es fehlt noch die Implementation die Figur nicht zu bewegen
# falls dadurch der König bedroht werden würde. 

###############################################################################

###############################################################################
# Änderung in rev13:
# Queen von Knight und Rook kopiert und umgeändert
# noch nicht getestet
# Code frisiert, alle überflüssigen __variablen aus den privaten Methoden
# entfernt. 
###############################################################################

class Figure() :
    
    # Konstruktor
    def __init__(self, color, fld, isActive = True) -> str :
        self.__isActive = isActive
        pos = Figure.fieldToPosition(fld)
        self.__color = color
        self.__col = pos[0]
        self.__row = pos[1]

    @property
    def getPos(self) :
        return [self.__col, self.__row]

    @property
    def getFld(self) :
        __colStrg = 'abcdefgh'
        __rowStrg = '12345678'
        __pos = self.getPos
        return __colStrg[__pos[0]-1] + __rowStrg[__pos[1]-1]

    @property
    def getState(self) :
        return self.__isActive

    @property
    def getColor(self) :
        return self.__color

    def beatFigure(self) : # Figur wird geschlagen und inaktiv gesetzt
        self.__isActive = False

    def reactivate(self, pos) : # Figur wird reaktiviert und mit neuer Position und State versehen
        self.__col = pos[0]
        self.__row = pos[1]
        self.__isActive = True

    def moveToField(self, fld) :
        pos = Figure.fieldToPosition(fld)
        self.__col = pos[0]
        self.__row = pos[1]

    def moveToPos(self, pos) :
        self.__col = pos[0]
        self.__row = pos[1]

    def isOnChessboard(self, pos) :
        bool = False
        col = pos[0]
        row = pos[1]
        if col > 0 and row > 0 and \
            col < 9 and row <9  :
            bool = True
        return bool

    @staticmethod
    def fieldToPosition(field) :
        if len(field) != 2 or (not field[0].isalpha()) or (not field[1].isdigit()) :
            raise ValueError("ungültige Notation!")
        else :
            col = 'abcdefgh'.find(field[0].lower())
            row = '12345678'.find(field[1])
            if col == -1 or row == -1 :
                raise ValueError("dieses Feld gibt es nicht")
            return [col+1, row+1]

    @staticmethod
    def isPositionBusy(pos, objectList):
        bool = False
        for object in objectList:
            if object.getPos == pos:
                bool = True
        return bool


class Knight(Figure) :
    def __init__(self, color, fld) :
        super().__init__(color, fld) # Basisklassenkonstruktor aufgerufen


    # gibt mögliche Züge zurück, nur welche die auch im Bereich des Spielfeldes 
    # sind
    # ACHTUNG - Fehlt noch: Figur darf nicht weggezogen werden wenn der König 
    # dadurch bedroht werden würde!
    def getPossibleMoves(self, others) :
        # ermittelt mögliche Züge der Schachfigur
        self.offset_col_row = [[2, 1], [2, -1], [1, 2], [-1, 2], [-2, 1], [-2, -1],
                            [1, -2], [-1, -2]]
        self.possibleMoves = []
        for self.element in self.offset_col_row :
            self.tmp_col = super().getPos[0] + self.element[0]
            self.tmp_row = super().getPos[1] + self.element[1]
            if super().isOnChessboard([self.tmp_col, self.tmp_row]):
                self.possibleMoves.append([self.tmp_col, self.tmp_row])
        # löscht Felder aus Ergebnisliste auf denen eigene Figuren stehen
        for object in others:
            if object.getPos in self.possibleMoves:
                if object.getColor == self.getColor:
                    self.possibleMoves.remove(object.getPos)
        return self.possibleMoves




class Bishop(Figure) :
    def __init__(self, color, fld) :
        super().__init__(color, fld)

    # j: Zählweise von der Figur aus - siehe __diagonalCount(position, offset, cycle)
    # i: Offset zur Position der Figur, eine ganze Diagonale = maximal 8 Felder
    # isBusy: Feld ist von eigener Farbe besetzt -> bis dahin darf gezogen werden
    # isThrowable: Feld ist von fremder Farbe besetzt -> gehört noch zu den möglichen Zügen
    def getPossibleMoves(self, others) :
        self.possibleMoves = []
        for j in range(4):
            for i in range(1, 8):
                newpos = self.__diagonalCount(self.getPos, i, j)
                if not super().isOnChessboard(newpos):
                    break
                isBusy = False
                isThrowable = False
                for object in others:
                    if object.getPos == newpos:
                        if object.getColor == self.getColor:
                            isBusy = True
                            break
                        else:
                            isThrowable = True
                if isBusy:
                    break
                self.possibleMoves.append(newpos)
                if isThrowable:
                    break
        return self.possibleMoves

    # Hilfsfunktion: ermittelt von der Position (position) der Figur aus die nächsten Felder (offset) in 
    # alle vier Zugrichtungen (cycle) des Läufers
    def __diagonalCount(self, position, offset, cycle):
        pos = None
        if cycle == 0:
            pos = [position[0] + offset, position[1] + offset] # von links unten nach rechts oben
        elif cycle == 1:
            pos = [position[0] + offset, position[1] - offset] # von links oben nach rechts unten
        elif cycle == 2:
            pos = [position[0] - offset, position[1] + offset] # von rechts unten nach links oben
        else:
            pos = [position[0] - offset, position[1] - offset] # von rechts oben nach links unten
        return pos


class Pawn(Figure) :
    def __init__(self, color, fld) :
        super().__init__(color, fld)
        self.__firstMove = True

    # overloaded
    def moveToField(self, fld) :
        super().moveToField(fld)
        self.__firstMove = False
   
    # overloaded
    def moveToPos(self, pos) :
        super().moveToPos(pos)
        self.__firstMove = False


    def getPossibleMoves(self, others):
        self.possibleMoves = []
        
        offsetPositiv = True # Weiss zieht von unten nach oben
        if self.getColor == 'black':
            offsetPositiv = False

        offset_col_row = [ [0, 1], [1, 1], [-1, 1] ]       # ohne Doppelfeld beim ersten Zug!

        for offset in offset_col_row:
            newpos = []
            baseCol = self.getPos[0]             # wir befinden uns in der vertikalen Zugrichtung des Bauern
            if offsetPositiv:                    # Weiss zieht zum oberen Rand des Spielbretts
                newpos = [self.getPos[0] + offset[0], self.getPos[1] + offset[1]]
            else:                                # Schwarz zieht in Richtung unterer Rand
                newpos = [self.getPos[0] + offset[0], self.getPos[1] - offset[1]]
            # wir füllen die Liste mit möglichen Feldern:
            if super().isOnChessboard(newpos):
                if newpos[0] is not baseCol:      # ist das neue Feld abseits der vertikalen Zugrichtung....
                    for object in others:
                        if object.getPos == newpos:
                            if object.getColor is not self.getColor:    # ...muss eine Figur darauf stehen die geschlagen werden darf
                                self.possibleMoves.append(newpos) 
                else:
                    if not Figure.isPositionBusy(newpos, others):    # wenn wir vertikal ziehen muss das Feld frei sein...
                        self.possibleMoves.append(newpos)
                        if self.__firstMove:                    # ...wenns der erste Zug ist dürfen wir zwei Felder ziehen
                            if offsetPositiv:
                                if not Figure.isPositionBusy([newpos[0], newpos[1] + 1], others):
                                    self.possibleMoves.append([newpos[0], newpos[1] + 1])
                            else:
                                if not Figure.isPositionBusy([newpos[0], newpos[1] - 1], others):
                                    self.possibleMoves.append([newpos[0], newpos[1] - 1])
        return self.possibleMoves


class Rook(Figure) :
    def __init__(self, color, fld) :
        super().__init__(color, fld)

    # j: Zählweise von der Figur aus - siehe __verticalCount(position, offset, cycle)
    # i: Offset zur Position der Figur, eine ganze Vertikale = maximal 8 Felder
    # isBusy: Feld ist von eigener Farbe besetzt -> bis dahin darf gezogen werden
    # isThrowable: Feld ist von fremder Farbe besetzt -> gehört noch zu den möglichen Zügen
    def getPossibleMoves(self, others) :
        self.possibleMoves = []
        for j in range(4): # Der Turm zieht in 4 verschiedene Richtungen
            for i in range(1, 8):
                newpos = self.__verticalCount(self.getPos, i, j)
                if not super().isOnChessboard(newpos):
                    break
                isBusy = False
                isThrowable = False
                for object in others:
                    if object.getPos == newpos:
                        if object.getColor == self.getColor:
                            isBusy = True
                            break
                        else:
                            isThrowable = True
                if isBusy:
                    break
                self.possibleMoves.append(newpos)
                if isThrowable:
                    break
        return self.possibleMoves

    # Hilfsfunktion: ermittelt von der Position (position) der Figur aus die nächsten Felder (offset) in 
    # alle vier Zugrichtungen (cycle) des Turms
    def __verticalCount(self, position, offset, cycle):
        pos = None
        if cycle == 0:
            pos = [position[0] + offset, position[1]] # von links nach rechts
        elif cycle == 1:
            pos = [position[0] - offset, position[1]] # von rechts nach links
        elif cycle == 2:
            pos = [position[0], position[1] + offset] # von unten nach oben
        else:
            pos = [position[0], position[1] - offset] # von oben nach unten
        return pos


class Queen(Figure) :
    def __init__(self, color, fld) :
        super().__init__(color, fld)

    # j: Zählweise von der Figur aus - siehe __diagonalCount(position, offset, cycle)
    # i: Offset zur Position der Figur, eine ganze Diagonale = maximal 8 Felder
    # isBusy: Feld ist von eigener Farbe besetzt -> bis dahin darf gezogen werden
    # isThrowable: Feld ist von fremder Farbe besetzt -> gehört noch zu den möglichen Zügen
    def getPossibleMoves(self, others) :
        self.possibleMoves = []
        for j in range(8): # Die Dame kann in 8 Zugrichtungen ziehen
            for i in range(1, 8):
                newpos = self.__diagonal_vertical_Count(self.getPos, i, j)
                if not super().isOnChessboard(newpos):
                    break
                isBusy = False
                isThrowable = False
                for object in others:
                    if object.getPos == newpos:
                        if object.getColor == self.getColor:
                            isBusy = True
                            break
                        else:
                            isThrowable = True
                if isBusy:
                    break
                self.possibleMoves.append(newpos)
                if isThrowable:
                    break
        return self.possibleMoves

    # Hilfsfunktion: ermittelt von der Position (position) der Figur aus die nächsten Felder (offset) in 
    # alle acht Zugrichtungen (cycle) der Dame
    def __diagonal_vertical_Count(self, position, offset, cycle):
        pos = None
        if cycle == 0:
            pos = [position[0] + offset, position[1] + offset] # von links unten nach rechts oben
        elif cycle == 1:
            pos = [position[0] + offset, position[1] - offset] # von links oben nach rechts unten
        elif cycle == 2:
            pos = [position[0] - offset, position[1] + offset] # von rechts unten nach links oben
        elif cycle == 3:
            pos = [position[0] - offset, position[1] - offset] # von rechts oben nach links unten
        elif cycle == 4:
            pos = [position[0] + offset, position[1]] # von links nach rechts
        elif cycle == 5:
            pos = [position[0] - offset, position[1]] # von rechts nach links
        elif cycle == 6:
            pos = [position[0], position[1] + offset] # von unten nach oben
        else:
            pos = [position[0], position[1] - offset] # von oben nach unten
        return pos



# BEGINN TESTCODE

# Funktion zum Finden eines Objektes anhand des Feldes
def findObj(field, objekte) :
    for objekt in objekte :
        if objekt.getFld == field.lower() :
            return objekt
    return False


obj = Queen('white', 'a1')
obj1 = Queen('black', 'a2') 
obj2 = Rook('white', 'a8')
obj3 = Rook('black', 'h1')
obj4 = Knight('white', 'e5')
obj5 = Knight('black', 'd5')
obj6 = Bishop('white', 'a4')
obj7 = Bishop('black', 'g5')
obj8 = Pawn('white', 'b1')
obj9 = Pawn('black', 'b7')

objekte = [obj, obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8, obj9]
aktiveFiguren = [figure for figure in objekte if figure.getState]
inaktiveFiguren = [figure for figure in objekte if not figure.getState]
    

for x in aktiveFiguren:
    print("aktives Objekt:", x.getColor, "hat die Position", x.getPos, " -> ", x.getFld)
    print("(",type(x),")", '\n')
for x in inaktiveFiguren:
    print("inaktives Objekt:", x.getColor, "hat die Position", x.getPos, " -> ", x.getFld)
    print("(",type(x),")", '\n')
for x in aktiveFiguren:
    print(x.getPossibleMoves(aktiveFiguren))


