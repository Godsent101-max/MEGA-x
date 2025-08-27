from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from database import SESSIONS, MESSAGES, newid

router = APIRouter()

def get_user_from_token(authorization: str = Header(None)):
    # token format: Bearer <username>
    if not authorization: return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    return None

class ChatIn(BaseModel):
    message: str
    session_id: int | None = None

class ChatOut(BaseModel):
    id: int
    message: str
    response: str
    session_id: int

@router.post('/session')
def new_session(authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    sid = newid('session')
    SESSIONS[sid] = {'id': sid, 'user': user, 'title': 'New session'}
    return {'session_id': sid}

@router.get('/sessions')
def list_sessions(authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    return [{'session_id': s['id']} for s in SESSIONS.values() if s['user']==user]

@router.post('/', response_model=ChatOut)
def chat(body: ChatIn, authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    if body.session_id is None:
        # find last session or create
        user_sessions = [s for s in SESSIONS.values() if s['user']==user]
        if not user_sessions:
            sid = newid('session'); SESSIONS[sid] = {'id': sid, 'user': user, 'title':'New session'}
        else:
            sid = user_sessions[-1]['id']
    else:
        sid = body.session_id
    mid = newid('message')
    # simple echo response for prototype with sentiment marker
    response = f"Evo (prototype) reply to: {body.message}"
    MESSAGES[mid] = {'id': mid, 'session_id': sid, 'user': user, 'message': body.message, 'response': response}
    return {'id': mid, 'message': body.message, 'response': response, 'session_id': sid}

@router.get('/history/{session_id}')
def history(session_id: int, authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    items = [m for m in MESSAGES.values() if m['session_id']==session_id and m['user']==user]
    return items