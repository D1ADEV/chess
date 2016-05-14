from Math import Math
from Logger import Logger

class Piece(object):
    def canAccessPosition(self, newX, newY):
        raise NotImplementedError
    
    def getAvailablePositions(self):
        raise NotImplementedError
        
    def canMoveTo(self, x, y, board):
        vector = Math.getVectorFromCoordinates(self.x, self.y, x, y)
        vector.prt()
        
        validPieces = [pc for pc in board 
            if pc.__name__ != "E" and not self == pc]
        
        collinearPieces = [pc for pc in validPieces
            if Math.areCollinear(Math.getVectorFromCoordinates(pc.x, pc.y, x, y), vector)]
        
        for i in collinearPieces:
            Logger.dbg('{0} - {1} - {2}'.format(i.__name__, i.x, i.y))
        
        onTheWay = [pc for pc in collinearPieces 
            if Math.isInTheInterval(self.x, x, pc.x) and Math.isInTheInterval(self.y, y, pc.y)]
        
        for i in onTheWay:
            Logger.dbg('{0} - {1} - {2}'.format(i.__name__, i.x, i.y))
            
        if len(onTheWay) == 0:
            return True
        else:
            return False
            

class NoPiece:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.joueur = -1
        self.__name__ = 'E'


class Pawn(Piece):

    def __init__(self, joueur, x, y):
        self.x = x
        self.y = y
        self.joueur = joueur
        self.__name__ = 'P'

    def getOwnerShip(self):
        return self.joueur

    def canAccessPosition(self, newX, newY):
        if 1 <= self.x <= 8 and 1 <= self.y <= 8 and 1 <= newX <= 8 and 1 <= newY <= 8:
            if [newX, newY] in self.getAvailablePositions():
                return True
            else:
                return False
        else:
            return False

    def getAvailablePositions(self):
        arr = []
        if self.joueur == 0:
            if self.y == 2:
                arr.append([self.x, self.y + 2])
                arr.append([self.x, self.y + 1])
                arr.append([self.x - 1, self.y + 1])
                arr.append([self.x + 1, self.y + 1])
            else:
                arr.append([self.x, self.y + 1])
                arr.append([self.x + 1, self.y + 1])
                arr.append([self.x - 1, self.y + 1])
        else:
            if self.y == 7:
                arr.append([self.x, self.y - 2])
                arr.append([self.x, self.y - 1])
                arr.append([self.x - 1, self.y - 1])
                arr.append([self.x + 1, self.y - 1])
            else:
                arr.append([self.x, self.y - 1])
                arr.append([self.x + 1, self.y - 1])
                arr.append([self.x - 1, self.y - 1])
        return arr


class King(Piece):

    def __init__(self, joueur, x, y):
        self.x = x
        self.y = y
        self.joueur = joueur
        self.__name__ = 'K'

    def getOwnerShip(self):
        return self.joueur

    def canAccessPosition(self, newX, newY):
        if 1 <= self.x <= 8 and 1 <= self.y <= 8 and 1 <= newX <= 8 and 1 <= newY <= 8: #Verifie que c'est dans l'echequier
            if [newX, newY] in self.getAvailablePositions(): #Verifie la disponibilite avec l'autre fonction, grace a l'inventaire
                return True
            else:
                return False
        else: 
            return False

    def getAvailablePositions(self): #Inventaire de toutes les positions valides
        arr = []
        arr.append([self.x, y - 1])
        arr.append([self.x + 1, self.y - 1])
        arr.append([self.x + 1, self.y])
        arr.append([self.x + 1, self.y + 1])
        arr.append([self.x, self.y + 1])
        arr.append([self.x - 1, self.y + 1])
        arr.append([self.x - 1, self.y])
        arr.append([self.x - 1, self.y - 1])
        return arr


class Knight(Piece):
     def __init__(self, joueur, x, y):
        self.x = x
        self.y = y
        self.joueur = joueur
        self.__name__ = 'Kn'

     def getOwnerShip(self):
        return self.joueur

     def canAccessPosition(self, newX, newY):
        if 1 <= self.x <= 8 and 1 <= self.y <= 8 and 1 <= newX <= 8 and 1 <= newY <= 8: #Verifie que c'est dans l'echequier
            if [newX, newY] in self.getAvailablePositions(): #Verifie la disponibilite avec l'autre fonction, grace a l'inventaire
                return True
            else:
                return False
        else:
            return False

     def getAvailablePositions(self):
        arr = []
        arr.append([self.y + 2, self.x + 1])
        arr.append([self.y + 2, self.x - 1])
        arr.append([self.y + 1, self.x + 2])
        arr.append([self.y - 1, self.x + 2])
        arr.append([self.y - 2, self.x + 1])
        arr.append([self.y - 2, self.x - 1])
        arr.append([self.y + 1, self.x - 2])
        arr.append([self.y - 1, self.x - 2])

        for i in range(0, len(
                arr)):  # [y, x] parceque je suis un noob. Reverse pour avoir [x, y] parceque la flemme de changer l'ordre
            arr[i].reverse()

        return arr


class Bishop(Piece):

     def __init__(self, joueur, x, y):
        self.x = x
        self.y = y
        self.joueur = joueur
        self.__name__ = 'B'

     def getOwnerShip(self):
        return self.joueur

     def canAccessPosition(self, newX, newY):
        if 1 <= self.x <= 8 and 1 <= self.y <= 8 and 1 <= newX <= 8 and 1 <= newY <= 8: #Verifie que c'est dans l'echequier
            if [newX, newY] in self.getAvailablePositions(): #Verifie la disponibilite avec l'autre fonction, grace a l'inventaire
                return True
            else:
                return False
        else:
            return False


     def getAvailablePositions(self):
        arr = []
        for i in range(-8, 8):
            if 1 <= (self.x +i) <= 8 and 1 <= (self.y +i) <= 8 and i != 0:  # Diag de haut gauche a bas droit
                #print('self.x : ' + str(self.x + i) + ' self.y : ' + str(y + i))
                arr.append([self.x + i, self.y + i])
            if 1 <= (self.x -i) <= 8 and 1 <= (self.y +i) <= 8 and i != 0:  # Diag haut droit bas gauche
                #print('2 : X : ' + str(x - i) + ' Y : ' + str(y + i))
                arr.append([self.x - i, self.y + i])
        return arr


class Rook(Piece):

     def __init__(self, joueur, x, y):
        self.x = x
        self.y = y
        self.joueur = joueur
        self.__name__ = 'R'

     def getOwnerShip(self):
        return self.joueur

     def canAccessPosition(self, newX, newY):
        if 1 <= self.x <= 8 and 1 <= self.y <= 8 and 1 <= newX <= 8 and 1 <= newY <= 8: #Verifie que c'est dans l'echequier
            if [newX, newY] in self.getAvailablePositions(): #Verifie la disponibilite avec l'autre fonction, grace a l'inventaire
                return True
            else:
                return False
        else:
            return False

     def getAvailablePositions(self):
        arr = []
        for i in range(0, 9):
            arr.append([self.x + i, self.y])
            arr.append([self.x - i, self.y])
            arr.append([self.x, self.y + i])
            arr.append([self.x, self.y - i])
        return arr
        
        
class Queen(Piece):
	def __init__(self, joueur, x, y):
		self.x = x
		self.y = y
		self.joueur = joueur
		self.__name__ = 'Q'
		
	def canAccessPosition(self, newX, newY):
		if 1 <= self.x <= 8 and 1 <= self.y <= 8 and 1 <= newX <= 8 and 1 <= newY <= 8: #Verifie que c'est dans l'echequier
			if [newX, newY] in self.getAvailablePositions(): #Verifie la disponibilite avec l'autre fonction, grace a l'inventaire
				return True
			else:
				return False
		else:
			return False
	def getAvailablePositions(self):
		arr = []
		for i in range(0, 9):
			arr.append([self.x + i, self.y])
			arr.append([self.x - i, self.y])
			arr.append([self.x, self.y + i])
			arr.append([self.x, self.y - i])
		for i in range(-8, 8):
			if 1 <= (self.x +i) <= 8 and 1 <= (self.y +i) <= 8 and i != 0:  # Diag de haut gauche a bas droit
				#print('self.x : ' + str(self.x + i) + ' self.y : ' + str(y + i))
				arr.append([self.x + i, self.y + i])
			if 1 <= (self.x -i) <= 8 and 1 <= (self.y +i) <= 8 and i != 0:  # Diag haut droit bas gauche
				#print('2 : X : ' + str(x - i) + ' Y : ' + str(y + i))
				arr.append([self.x - i, self.y + i])
		return arr
		
		