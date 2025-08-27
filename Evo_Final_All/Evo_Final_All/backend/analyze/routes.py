from fastapi import APIRouter
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

router = APIRouter()
_an = SentimentIntensityAnalyzer()

class TextIn(BaseModel):
    text: str

@router.post('/sentiment')
def sentiment(body: TextIn):
    s = _an.polarity_scores(body.text)
    return s