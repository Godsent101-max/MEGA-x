from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from .utils import enroll_face, verify_face

router = APIRouter()

def get_user_from_token(authorization: str = Header(None)):
    if not authorization: return None
    parts = authorization.split()
    if len(parts)==2 and parts[0].lower()=='bearer': return parts[1]
    return None

class EnrollIn(BaseModel):
    image_b64: str

@router.post('/enroll/face')
def enroll(payload: EnrollIn, authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    res = enroll_face(user, payload.image_b64)
    if not res.get('ok'): raise HTTPException(status_code=400, detail='enroll failed')
    return {'status':'ok', 'path': res.get('path')}

class VerifyIn(BaseModel):
    image_b64: str

@router.post('/verify/face')
def verify(payload: VerifyIn, authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    if not user: raise HTTPException(status_code=401, detail='unauth')
    res = verify_face(user, payload.image_b64)
    return {'status':'ok', 'match': res.get('match')}