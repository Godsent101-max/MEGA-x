Evo Final All - Production Packaging
===================================

This package contains the Evo prototype with Dockerfiles and docker-compose for local production-like testing.

Quick start:
1. Copy `.env.example` to `.env` and fill in API keys.
2. Build and run:
   make build
   make up
3. Visit frontend at http://localhost:3000 and backend at http://localhost:8000

Notes:
- The backend will look for OPENAI_API_KEY, REPLICATE_API_TOKEN, COQUI_API_KEY, ELEVENLABS_API_KEY and EVO_FERNET_KEY in the environment.
- For production: use a secret manager for keys, enable HTTPS (reverse proxy), and use managed databases and object storage.

Included files: docker-compose.yml, .env.example, Makefile, backend/, frontend/