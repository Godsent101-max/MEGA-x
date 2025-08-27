from fastapi import APIRouter, UploadFile, File, HTTPException
import os, tempfile, base64, requests, json
router = APIRouter()

@router.post('/stt')
async def stt(file: UploadFile = File(...)):
    rep_token = os.getenv('REPLICATE_API_TOKEN')
    if rep_token:
        # Attempt to use Replicate's whisper or other STT model (user must verify model/version)
        try:
            headers = {"Authorization": f"Token {rep_token}", "Content-Type":"application/json"}
            # This is a placeholder: recommend using replicate python client for robust integration
            return {'text': '[stt via replicate not implemented in prototype]', 'confidence': 0.0}
        except Exception as e:
            pass
    # OpenAI fallback if key set
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        try:
            import openai, tempfile
            openai.api_key = openai_key
            ext = os.path.splitext(file.filename)[1] or '.wav'
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                tmp.write(await file.read()); tmp.flush(); tmp_path = tmp.name
            with open(tmp_path, 'rb') as audio_file:
                resp = openai.Audio.transcriptions.create(file=audio_file, model='whisper-1')
            os.remove(tmp_path)
            return {'text': resp['text'], 'confidence': resp.get('confidence', 0.0)}
        except Exception as e:
            return {'text': f'[stt error: {e}]', 'confidence': 0.0}
    return {'text': '[no STT provider configured]', 'confidence':0.0}

@router.post('/tts')
async def tts(body: dict):
    text = body.get('text','')
    # Try Coqui TTS via public API if key present
    coqui_key = os.getenv('COQUI_API_KEY')
    if coqui_key:
        try:
            # Example Coqui.ai API call - user must configure model and endpoint
            url = "https://api.coqui.ai/tts"  # placeholder
            headers = {"Authorization": f"Bearer {coqui_key}", "Content-Type":"application/json"}
            payload = {"text": text, "model":"tts_model"}
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            r.raise_for_status()
            audio = r.content
            return {'audio_b64': 'data:audio/mpeg;base64,' + base64.b64encode(audio).decode('utf-8')}
        except Exception as e:
            pass
    # ElevenLabs fallback if set
    eleven_key = os.getenv('ELEVENLABS_API_KEY')
    if eleven_key:
        try:
            import requests, base64
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {"xi-api-key": eleven_key, "Content-Type":"application/json"}
            payload = {"text": text, "voice_settings":{"stability":0.5,"similarity_boost":0.75}}
            r = requests.post(url, json=payload, headers=headers, stream=True, timeout=30)
            r.raise_for_status()
            data = r.content
            return {'audio_b64': 'data:audio/mpeg;base64,' + base64.b64encode(data).decode('utf-8')}
        except Exception as e:
            return {'error': str(e)}
    return {'error':'No TTS provider configured. Set COQUI_API_KEY or ELEVENLABS_API_KEY'}