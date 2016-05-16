#!/usr/bin/python
# -*- coding: utf-8 -*-
from Pieces import *
from Logger import Logger
import json
from time import time

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
        self.eatenPieces = []
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
            Queen(0, 3, 4),
            NoPiece(3, 5),
            NoPiece(3, 6),
            Pawn(1, 3, 7),
            Bishop(1, 3, 8),
            NoPiece(4, 1),
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
            King(1, 5, 5),
            NoPiece(5, 6),
            Pawn(1, 5, 7),
            NoPiece(5, 8),
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
    # Return : nouveau tableau contenant les pièces 
    #
    def updateBoard(self, move):
        oldPieceIndex = self.getPieceIndex(move['oldX'], move['oldY'])
        newPieceIndex = self.getPieceIndex(move['x'], move['y'])
        
        oldPiece = self.board[oldPieceIndex]
        newPiece = self.board[newPieceIndex]
        
        Logger.dbg(oldPiece.__name__)
        Logger.dbg(newPiece.__name__)
                    
        tempBoard = list(self.board)
        
        if not isinstance(newPiece, NoPiece):
            Logger.dbg('eating')
            if oldPiece.canEat(move['x'], move['y']):
                
                self.eatenPieces.append(newPiece)
            
        tempBoard[oldPieceIndex] = NoPiece(self.board[oldPieceIndex].x, self.board[oldPieceIndex].y)
        tempBoard[newPieceIndex] = type(self.board[oldPieceIndex])(
            self.board[oldPieceIndex].joueur, self.board[newPieceIndex].x, self.board[newPieceIndex].y)
            # python is ok with me doing that
        
        return tempBoard
        
        
                
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
    # Return : index de la pièce si elle est dans le tableau, False sinon
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
    # Return : Aucun
    #
    def doMove(self, move):
        pieceIndex = self.getPieceIndex(move['oldX'], move['oldY'])
        if pieceIndex is not False:
            if self.board[pieceIndex].joueur == self.playerTurn:
                piece = self.board[pieceIndex]
                if piece.canAccessPosition(move['x'], move['y']):
                    canMove = piece.canMoveTo(move['x'], move['y'], self.board)
                    if canMove:
                        tempBoard = self.updateBoard(move)
                        resp = self.checkCheck(self.playerTurn, tempBoard)
                        if resp is True:
                            Logger.dbg("CHECK")
                            legalMoves = self.getAllLegalMoves(self.playerTurn)
                            if len(legalMoves) > 0:
                                return {'error': 'Still check'}
                            else:
                                return {'error': 'Check mate batar'}
                        else:
                            Logger.dbg("NOT CHECK")
                            self.playerTurn = 0 if self.playerTurn == 1 else 1
                            self.board = tempBoard
                            return self.getState()
                    else:
                        Logger.dbg('There\'s a piece on the path')
                        return {'error': 'Piece on the path'}
                else:
                    Logger.dbg('nope')
                    return {'error': 'Piece can\'t go there'}
            else:
                Logger.dbg('not his piece')
                return {'error': 'this piece doesn\'t belong to you'}
            
                
        
    #
    # DONE
    # Renvoie une représentation JSON du tableau contenant les pièces
    # Args : Aucun
    # Return : tableau contenant les pièces et le tour du joueur
    #
    def getState(self):
        resData = {}
        tempBoard = list(self.getBoard()) # Sehr important, sinon modifier tempBoard modifiera self.board, parceque Python. 
        for i in range(len(tempBoard)):
            if type(tempBoard[i]) is not str and type(tempBoard[i]) is not list:
                tempBoard[i] = [tempBoard[i].__name__, tempBoard[i].joueur]
        resData['board'] = tempBoard
        resData['playerTurn'] = self.playerTurn
        resData['ready'] = self.ready
        return resData
 
    #
    # Todo
    #
    def checkIntegrity(self):
        errors = {'missingPieces': False, 'coordinatesError': False}
        errors['missingPieces'] = ((len([x for x in self.board if x.__name__ != "E"]) + len(self.eatenPieces)) == 32)
        return errors
            
            
            
    def checkCheck(self, player, board):
        piecesNotOwned = [x for x in board if x.joueur != player and x.__name__ != "E"]
        king = [x for x in board if x.joueur == player and x.__name__ == "K"][0]
        for piece in piecesNotOwned:
            if piece.canAccessPosition(king.x, king.y):
                if piece.canMoveTo(king.x, king.y, board) and piece.canEat(king.x, king.y):
                    return True
        return False
        
            
    def getAllLegalMoves(self, player):
        legalMoves = []
        pieces = [x for x in self.board if x.__name__ != "E" and x.joueur == player]
        for piece in pieces:
            moves = [m for m in piece.getPseudoLegalMoves() if piece.canMoveTo(m[0], m[1], self.board)]
            for move in moves:
                m = {"oldX": piece.x, "oldY": piece.y, "x": move[0], "y": move[1]}
                tempBoard = self.updateBoard(m)
                if not self.checkCheck(player, tempBoard):
                    legalMoves.append(m)
        return legalMoves
 
 
 
 
 
 
 