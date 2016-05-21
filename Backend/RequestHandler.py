from SessionStorage import SessionStorage
from RequestKind import RequestKind
from Logger import Logger

#
# Classe qui gère les requètes
#
class RequestHandler:
    
    #
    # DONE
    # Initialisation
    # Args : Aucun
    # Return : Aucun
    #
    def __init__(self):
        Logger.log('Request handler init')
        self.SessionStorage = SessionStorage()

    #
    # DONE
    # Distribue les requètes vers des fonctions
    # Args : Requète
    # Return : Valeur renvoyée par la fonction 
    #
    def dispatchRequest(self, rq):
        Logger.log('dispatching request : ' + str(rq.requestKind))
        if rq.requestKind is not False:
            if rq.requestKind == RequestKind.CreateNewGameRequest:
                return self.handleNewGameRequest()
            if rq.requestKind == RequestKind.JoinGameRequest:
                return self.handleJoinGameRequest(rq)
            if rq.requestKind == RequestKind.GameUpdateRequest:
                return self.handleGameUpdateRequest(rq)
            if rq.requestKind == RequestKind.MoveRequest:
                return self.handleMoveRequest(rq)
        else:
            return False

    #
    # DONE
    # Fonction qui gère les requètes de création de nouvelle partie
    # Args : Aucun
    # Return : Valeur renvoyée par la SessionStorage.addNewSession()
    #
    def handleNewGameRequest(self):
        Logger.log('Handling new game')
        res = self.SessionStorage.addNewSession()
        
        return res
        
    
    #
    # DONE
    # Fonction qui gère les requètes de join
    # Args : Objet Request
    # Return : Id de joueur
    #
    def handleJoinGameRequest(self, rq):
        res = self.SessionStorage.joinGame(rq.params['uniqueurl'])
        return res
    
    #
    # DONE
    # Fonction qui geère les requètes de mise à jour de la game
    # Args : Objet Request
    # Return : Json de la partie
    #
    def handleGameUpdateRequest(self, rq):
        res = self.SessionStorage.getGameStateJson(rq.params['uniqueurl'])
        return res
    
    # 
    # TODO
    # Fonction qui gère les requètes de mouvement
    # Args : Objet Request
    # Return : TODO
    #
    def handleMoveRequest(self, rq):
        res = self.SessionStorage.move(
            rq.params['uniqueid'],
            rq.params['uniqueurl'],
            rq.params['move'])
        return res
