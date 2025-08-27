from fastapi import APIRouter, Depends, Response, Header, HTTPException
import io, json
from database import MESSAGES
router = APIRouter()

def get_user_from_token(authorization: str = Header(None)):
    if not authorization: return None
    parts = authorization.split()
    if len(parts)==2 and parts[0].lower()=='bearer': return parts[1]
    return None

@router.get('/txt/{session_id}')
def export_txt(session_id: int, authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    buff = io.StringIO()
    for m in [v for v in MESSAGES.values() if v['session_id']==session_id and v['user']==user]:
        buff.write(f"{m['message']}\n---\n{m['response']}\n\n")
    return Response(content=buff.getvalue(), media_type='text/plain', headers={'Content-Disposition':f'attachment; filename=chat_{session_id}.txt'})