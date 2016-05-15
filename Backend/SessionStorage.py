from random import randint
from Game import Game
from json import dumps
from Logger import Logger

#
# Classe qui renferme la magie du système de sessions, et la plupart des fonctions "haut niveau" du gameplay
# ("haut niveau" comme dans "il y a une fonction move, mais elle bouge rien, c'est les classes spécialisées qui s'en occupent".
#
class SessionStorage:
    
    #
    # DONE
    # Initialisation, création du tableau self.sessions. (Vide en prod, rempli pour le debug)
    # Args : Aucun
    # Return : Aucun
    #
    def __init__(self):
        self.sessions = [[456, [12, 13], Game()]]
        self.sessions[0][2].initBoard()
        # sessions : [[uniqueurl, [player1uniqueid, player2uniqueid], Game],
        # [...]]

    #
    # DONE
    # Crée un tableau contenant deux ids
    # Args : Aucun
    # Return : Un tableau de deux ids "aléatoires", non identiques
    #
    def generateUniqueIds(self):
        return [randint(0, 1000), randint(1001, 2000)]

    #
    # DONE
    # Crée un id (url) de partie unique
    # Args : Aucun
    # Return : Url si pas ou peu de collisions, un message d'erreur sinon
    #
    def generateUniqueUrl(self):
        u = randint(0, 5000)
        Logger.log('Generating unique url')
        if len(self.sessions) < 4000:
            for e in self.sessions:
                if u in e:
                    Logger.warn('Collision')
                    return self.generateUniqueUrl()
            Logger.log('No collision')
            return u
        else:
            return {'error': 'Too many sessions'}

    #
    # DONE
    # Crée une nouvelle session
    # Args : Aucun
    # Return : JSON {uniqueurl :
    #
    def addNewSession(self):
        Logger.log('Adding new session')
        url = self.generateUniqueUrl()
        if isinstance(url, int):
            ids = self.generateUniqueIds()
            self.sessions.extend([[url, ids, Game()]])
        else:
            Logger.error(url['error'])
            return False
        return dumps({'uniqueurl': url})

    #
    # DONE
    # Ajoute un joueur à une session
    # Args : un id (url) de partie
    # Return : Si la partie est libre un JSON {'id: id}, sinon False
    #
    def joinGame(self, uniqueurl):
        index = self.gameExists(uniqueurl)
        if index is not False:
            if self.sessions[index][2].playerCanJoin() is True:
                self.sessions[index][2].join()
                uid = self.sessions[index][1][self.sessions[index][2].players - 1] # the hard way
                turn = self.sessions[index][1].index(uid)
                return dumps({'id': uid, 'turn': turn}) 
            else:
                return False
        else:
            return False

    #
    # DONE
    # Renvoie le State de la partie
    # Args : un id (url) de partie
    # Return : un représentation JSON de la partie associée à l'id
    #
    def getGameStateJson(self, url):
        index = self.gameExists(url)
        if index is not None:
            res = self.sessions[index][2].getState()
            return dumps(res)

    #
    # DONE
    # La partie existe-t-elle? 
    # Args : un id (url) de partie
    # Return : index de la partie dans self.sessions si elle existe, None sinon
    #
    def gameExists(self, uniqueurl):
        for i in range(0, len(self.sessions)):
            if self.sessions[i][0] == int(uniqueurl):
                Logger.log('Game {0} exists'.format(uniqueurl))
                return i
        Logger.warn('Game {0} doesn\'t exist'.format(uniqueurl))
        return None
    
    #
    # TODO
    # Bouger des pièces
    # Args : un id de joueur; un id (url) de partie, un move en JSON
    # Return : TODO
    #
    def move(self, uniqueid, uniqueurl, move):
        i = self.gameExists(uniqueurl)
        if i is not None:
            if self.sessions[i][1][self.sessions[i][2].playerTurn] == int(uniqueid):
                res = self.sessions[i][2].doMove(move)
                Logger.dbg(res)
                return dumps(res)
            else:
                return dumps({'error': 'Not your turn'}) 
        else:
            return dumps({'error': 'The game doesn\'t exit on the server anymore, sorry'}) 




