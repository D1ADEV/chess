#!/usr/bin/python
# -*- coding: utf-8 -*-
from Pieces import *
from Logger import Logger
import json

class Game:

    #
    # DONE
    # Initialisation de la partie
    # Args : Aucun
    # Return Aucun
    #
    def __init__(self):
        self.ready = False
        self.players = 0
        self.board = []
        self.playerTurn = 0
        self.initBoard()

    #
    # DONE
    # Initialisation du tableau qui contient toutes les pièces de l'échiquier
    # Args : Aucun
    # Return : Aucun
    #
    def initBoard(self):
        self.board = [
            Rook(0, 1, 1),
            Pawn(0, 1, 2),
            NoPiece(1, 3),
            NoPiece(1, 4),
            NoPiece(1, 5),
            NoPiece(1, 6),
            Pawn(1, 1, 7),
            Rook(1, 1, 8),
            Knight(0, 2, 1),
            Pawn(0, 2, 2),
            NoPiece(2, 3),
            NoPiece(2, 4),
            NoPiece(2, 5),
            NoPiece(2, 6),
            Pawn(1, 2, 7),
            Knight(1, 2, 8),
            Bishop(0, 3, 1),
            Pawn(0, 3, 2),
            NoPiece(3, 3),
            NoPiece(3, 4),
            NoPiece(3, 5),
            NoPiece(3, 6),
            Pawn(1, 3, 7),
            Bishop(1, 3, 8),
            Queen(0, 4, 1),
            Pawn(0, 4, 2),
            NoPiece(4, 3),
            NoPiece(4, 4),
            NoPiece(4, 5),
            NoPiece(4, 6),
            Pawn(1, 4, 7),
            Queen(1, 4, 8),
            King(0, 5, 1),
            Pawn(0, 5, 2),
            NoPiece(5, 3),
            NoPiece(5, 4),
            NoPiece(5, 5),
            NoPiece(5, 6),
            Pawn(1, 5, 7),
            King(1, 5, 8),
            Bishop(0, 6, 1),
            Pawn(0, 6, 2),
            NoPiece(6, 3),
            NoPiece(6, 4),
            NoPiece(6, 5),
            NoPiece(6, 6),
            Pawn(1, 6, 7),
            Bishop(1, 6, 8),
            Knight(0, 7, 1),
            Pawn(0, 7, 2),
            NoPiece(7, 3),
            NoPiece(7, 4),
            NoPiece(7, 5),
            NoPiece(7, 6),
            Pawn(1, 7, 7),
            Knight(1, 7, 8),
            Rook(0, 8, 1),
            Pawn(0, 8, 2),
            NoPiece(8, 3),
            NoPiece(8, 4),
            NoPiece(8, 5),
            NoPiece(8, 6),
            Pawn(1, 8, 7),
            Rook(1, 8, 8)
            ]

    #
    # DONE
    # Renvoie le tableau qui contient toutes les pièces de l'échiquier
    # Args : Aucun
    # Return : Un tableau contenant les pièces
    #
    def getBoard(self):
        return self.board

    #
    # Met a jour le tableau contenant les pièces après un mouvement
    # Args : L'index de la pièce qui va bouger
    # Return : Aucun
    #
    def updateBoard(self, move):
        oldPieceIndex = self.getPieceIndex(move['oldX'], move['oldY'])
        oldPiece = self.board[oldPieceIndex]
        Logger.log(oldPiece.__name__)
        tempBoard = self.board
        for i in range(len(self.board)):
            if self.board[i].x == move['x'] and self.board[i].y == move['y']:
                if isinstance(self.board[oldPieceIndex], Pawn):
                    self.board[i] = Pawn(move['id'], move['x'], move['y'])
                    self.board[oldPieceIndex] = NoPiece(move['oldX'], move['oldY'])
                    
                
    #
    # DONE
    # Un joueur peut-il rejoindre la partie?
    # Args : Aucun
    # Return : True si c'est possible, False sinon
    #
    def playerCanJoin(self):
        if self.players < 2:
            return True
        else:
            return False
    #
    # DONE
    # Ajoute un joueur à la partie
    # Args : Aucun
    # Return Aucun
    #
    def join(self):
        self.players += 1
        if self.players == 2:
            self.ready = True
            self.initBoard()

    #
    # DONE
    # La coordonnée est elle occupée? 
    # Args : coordonée x, coordonée y
    # Return : index de la coordonnée si il n'y a pas de pièce, True sinon
    #
    def isSpaceOccupied(self, x, y):
        for i in range(len(self.board)):
            if self.board[i].x == x and self.board[i].y == y:
                if isinstance(self.board[i], NoPiece):
                    return i
                else:
                    return True
                    
    
    #
    # DONE
    # Renvoie l'index d'une pièce en fonction de son x et y
    # Args : x, y de la pièce
    # Return : index de la pièce si elle est dans le tableau, False 
    #
    def getPieceIndex(self, x, y):
        for i in range(len(self.board)):
            if self.board[i].x == x and self.board[i].y == y:
                return i
        return False
    
    #
    # TODO
    # S'occupe de bouger les pièces sur l'échiquier 
    # Args : move (JSON?) pas fini donc pas sur
    # Return : Sais pas encore (pas fini)
    #
    def doMove(self, move):
       #Logger.log(move)
        r = self.isSpaceOccupied(move['x'], move['y'])
        if r is True:
            return 'space taken'
        elif isinstance(r, int):
            self.updateBoard(move)
    #
    # DONE
    # Renvoie une représentation JSON du tableau contenant les pièces
    # Args : Aucun
    # Return : tableau contenant les pièces et le tour du joueur
    #
    def getState(self):
        resData = {}
        tempBoard = self.board
        for i in range(len(tempBoard)):
            if type(tempBoard[i]) is not str and type(tempBoard[i]) is not list:
                tempBoard[i] = [tempBoard[i].__name__, tempBoard[i].joueur]
        
        resData['board'] = tempBoard
        resData['playerTurn'] = self.playerTurn
        resData['ready'] = self.ready
        return resData
 
 
 
 
 