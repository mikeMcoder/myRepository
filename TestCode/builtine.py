import __builtin__


path = "C:\\Users\\michael.mercado\\Documents\\ThingsToDoandGoals"

def open(path):
    f = __builtin__.open(path, 'r')
    return UpperCaser(f)

class UpperCaser:
    '''Wrapper around a file that converts output to upper-case.'''

    def __init__(self, f):
        self._f = f

    def read(self, count=-1):
        return self._f.read(count).upper()



f_path = open(path)
script = UpperCaser(f_path)

