from inspect import getframeinfo, stack
from termcolor import cprint
#
# Classe qui s'occupe du logging
#
class Logger:
    
    #
    # DONE
    # Affiche l'état du jeux. 
    # Args : Array des sessions
    # Return : Aucun
    #
    @staticmethod
    def printCurrentState(gameState):
        cprint('\n\n-----GAME STATE-----\n', 'cyan')
        cprint('{0} active sessions'.format(len(gameState)), 'cyan')
        for i in gameState:
            cprint('Session url : {0} - Session player ids : {1}'.format(i[0], i[1]), 'cyan')
        cprint('\n--------------------\n\n', 'cyan')

    #
    # DONE
    # Affiche un message, avec plus d'infos que print()
    # Args : Message à afficher
    # Return : Aucun
    #
    @staticmethod
    def log(message):
        caller = getframeinfo(stack()[1][0])
        path = caller[0]
        if '\\' in path:
            path = path.split('\\')[-1]
        line = caller[1]
        cprint('{0}:{1} - {2}'.format(path, line, message), 'magenta')
    
    @staticmethod
    def warn(message):
        caller = getframeinfo(stack()[1][0])
        path = caller[0]
        if '\\' in path:
            path = path.split('\\')[-1]
        line = caller[1]
        cprint('{0}:{1} - {2}'.format(path, line, message), 'yellow')
        
    @staticmethod
    def error(message):
        caller = getframeinfo(stack()[1][0])
        path = caller[0]
        if '\\' in path:
            path = path.split('\\')[-1]
        line = caller[1]
        cprint('{0}:{1} - {2}'.format(path, line, message), 'red')
        
    @staticmethod
    def dbg(message):
        caller = getframeinfo(stack()[1][0])
        path = caller[0]
        if '\\' in path:
            path = path.split('\\')[-1]
        line = caller[1]
        cprint('{0}:{1} - {2}'.format(path, line, message), 'red', 'on_white')