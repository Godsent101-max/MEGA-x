from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routes import router as auth_router
from chat.routes import router as chat_router
from biometrics.routes import router as biom_router
from analyze.routes import router as analyze_router
from utils_export import router as export_router

app = FastAPI(title="Evo Prototype")

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(chat_router, prefix='/chat', tags=['Chat'])
app.include_router(biom_router, prefix='/biometrics', tags=['Biometrics'])
app.include_router(analyze_router, prefix='/analyze', tags=['Analyze'])
app.include_router(router=None, prefix='/voice', tags=['Voice'])  # placeholder
app.include_router(export_router, prefix='/export', tags=['Export'])

@app.get('/')
def home():
    return {'message':'Evo Prototype API'}
from voice_routes import router as voice_router
from image_routes import router as image_router
app.include_router(voice_router, prefix='/voice', tags=['Voice'])
app.include_router(image_router, prefix='/image', tags=['Image'])
