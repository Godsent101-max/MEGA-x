from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import USERS, newid
router = APIRouter()

class SignupIn(BaseModel):
    username: str
    password: str

@router.post('/signup')
def signup(body: SignupIn):
    if body.username in USERS:
        raise HTTPException(status_code=400, detail='username exists')
    uid = newid('user')
    USERS[body.username] = {'id': uid, 'username': body.username, 'password': body.password}
    return {'message':'created'}

class LoginIn(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(body: LoginIn):
    u = USERS.get(body.username)
    if not u or u['password'] != body.password:
        raise HTTPException(status_code=400, detail='invalid credentials')
    # simple token = username for prototype
    return {'access_token': body.username, 'token_type':'bearer'}