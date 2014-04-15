# Decoratori
# https://www.artima.com/weblogs/viewpost.jsp?thread=240808


from datetime import datetime
from functools import wraps

def timer(f):
    msg = f.__name__
    @wraps(f)
    def decorated(*args,**kwargs):
        print '\t-------------------\n'
        print msg, 'debug iniziato'
        startTime = datetime.now()
        return f(*args,**kwargs)
        endTime = datetime.now()
        print msg, 'debug finito'
        print 'timer: ', endTime - startTime
        print '\n\t------------------'
    return decorated
