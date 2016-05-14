from Logger import Logger

class Math:
    @staticmethod
    def getVectorFromCoordinates(ax, ay, bx, by):
        return Vector(bx - ax, by - ay)
    
    @staticmethod
    def areCollinear(vector, vector2):
        return vector.x * vector2.y == vector.y * vector2.x
        
    @staticmethod
    def isInTheInterval(low, high, value):
        if low <= high:
            return (low <= value <= high)
        else:
            return (high <= value <= low)
    
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def prt(self):
        Logger.dbg('x : {0} - y : {1}'.format(self.x, self.y))
        