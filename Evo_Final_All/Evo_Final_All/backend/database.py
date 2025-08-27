# simple in-memory 'db' for prototype (not for production)
USERS = {}
SESSIONS = {}
MESSAGES = {}
_next_ids = {'user':1, 'session':1, 'message':1}
def newid(kind):
    _next_ids[kind] += 1
    return _next_ids[kind]-1