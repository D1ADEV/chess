#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from RequestKind import RequestKind
from Request import Request
from RequestHandler import RequestHandler
from Logger import Logger
from flask.ext.cors import CORS

#Classe qui gère l'API REST

class Server:
    
    #
    #DONE
    #Initialisation du serveur
    #Args : ip du serveur, port du serveur
    #Return : Aucun
    #
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.__name__ = "Server"
        self.RequestHandler = RequestHandler()
        self.app = Flask(__name__)
        self.app.debug = False
        CORS(self.app)
        self.startListening()

    # 
    # DONE
    # Démarre vraiment le serveur (API REST)
    # Args : Aucun
    # Return Aucun 
    #
    def startListening(self):
        Logger.log('Listening')

        #
        # TODO 
        # Gère les requètes sur /
        # Args : Aucun
        # Return : Code html de la page d'index (pas fini)
        #
        @self.app.route("/", methods=['GET'])
        def index():
            Logger.printCurrentState(
                self.RequestHandler.SessionStorage.sessions)
            return "index"
            
        #
        # DONE
        # Gère les requètes sur /move/url/id
        # Args : Une url unique de partie, l'id de la personne qui joue, une réprésentation JSON du mouvement par POST
        # Return : JSON
        #
        @self.app.route("/move/<uniqueurl>/<int:uniqueid>", methods=['POST'])
        def move(uniqueurl, uniqueid):
            Logger.printCurrentState(
                self.RequestHandler.SessionStorage.sessions)
            Logger.log('Received request on /move')
            res = self.RequestHandler.dispatchRequest(
                Request(
                    uniqueurl=uniqueurl,
                    uniqueid=uniqueid,
                    requestKind=RequestKind.MoveRequest))
            return str(res)
            
            
        #
        # DONE
        # Gère les requètes sur /createnewgame
        # Args : Aucun
        # Return : ID de la game créée. 
        #
        @self.app.route("/createnewgame", methods=['GET'])
        def create():
            Logger.printCurrentState(
                self.RequestHandler.SessionStorage.sessions)
            Logger.log('Received request on /createnewgame')
            res = self.RequestHandler.dispatchRequest(
                Request(requestKind=RequestKind.CreateNewGameRequest))
            Logger.log(res)
            return str(res)
        #
        # DONE
        # Gère les requètes sur /joingame/uniqueurl
        # Args : Url unique
        # Return : Id de joueur si la game peut être créée, False sinon
        #
        @self.app.route("/joingame/<int:uniqueurl>", methods=['GET'])
        def join(uniqueurl):
            Logger.printCurrentState(
                self.RequestHandler.SessionStorage.sessions)
            Logger.log('Received request on /joingame')
            res = self.RequestHandler.dispatchRequest(
                Request(requestKind=RequestKind.JoinGameRequest, uniqueurl=uniqueurl))
            return str(res)
        
        #
        # DONE
        # Gère les requètes sur /gameupdate/uniqueurl
        # Args : Url unique
        # Return : JSON représentant la partie
        # 
        @self.app.route("/gameupdate/<int:uniqueurl>", methods=['GET'])
        def update(uniqueurl):
            Logger.printCurrentState(self.RequestHandler.SessionStorage.sessions)
            Logger.log('Received a request on /gameupdate')
            res = self.RequestHandler.dispatchRequest(
                Request(requestKind=RequestKind.GameUpdateRequest, uniqueurl=uniqueurl))
            return str(res)
        
        # 
        # DONE
        # Url de debug
        # Args : Aucun
        # Return : Renvoie les sessions stockées, à supprimer en prod.
        #
        @self.app.route("/debug", methods=['GET'])
        def debug():
            return str(self.RequestHandler.SessionStorage.sessions)
            

        self.app.run(host=self.ip, port=self.port)
