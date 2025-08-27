# Evo Prototype\n\nMinimal prototype with backend (FastAPI) and frontend (React). See backend/requirements.txt and frontend/package.json for setup.\n\nDisclaimer: prototype uses naive in-memory storage and placeholder biometric functions. Not for production.

## Advanced Features Added
- /voice/stt and /voice/tts endpoints (require OPENAI_API_KEY or ELEVENLABS_API_KEY)
- /image/gen endpoint (uses OpenAI Images if OPENAI_API_KEY set)
- Encrypted biometric storage using Fernet (EVO_FERNET_KEY env or generated key)

Set environment variables before running:
- OPENAI_API_KEY (optional for STT & images)
- ELEVENLABS_API_KEY (optional for TTS)
- EVO_FERNET_KEY (optional, 44-char base64 key)

Notes: This is a development prototype. For production, don't store raw images; build templates and liveness checks, secure keys, and use proper storage.


## Dockerized Setup

Build and run (requires Docker and docker-compose):
```bash
docker-compose build
docker-compose up
```
- Backend will be available at http://localhost:8000
- Frontend at http://localhost:3000

Set environment variables for provider keys before running:
- OPENAI_API_KEY (optional)
- REPLICATE_API_TOKEN (for Replicate image generation)
- COQUI_API_KEY (for Coqui TTS) or ELEVENLABS_API_KEY if preferred
- EVO_FERNET_KEY (optional, 44-char base64 key)

