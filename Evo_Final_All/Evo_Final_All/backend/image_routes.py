from fastapi import APIRouter, HTTPException
import os, base64, requests, tempfile, json
router = APIRouter()

@router.post('/gen')
def gen_image(body: dict):
    prompt = body.get('prompt','')
    if not prompt:
        raise HTTPException(status_code=400, detail='prompt required')
    # Try Replicate first if token present
    rep_token = os.getenv('REPLICATE_API_TOKEN')
    if rep_token:
        try:
            headers = {"Authorization": f"Token {rep_token}", "Content-Type":"application/json"}
            # example using replicate's stablediffusion v1.5 (model slug may vary)
            data = {"version":"ff4d6c3b9e4c..." , "input":{"prompt": prompt, "width":512, "height":512}}
            # Note: user must replace version with actual model version ID or use Replicate SDK.
            # We'll attempt a simple POST to Replicate's API as placeholder.
            r = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=data, timeout=60)
            r.raise_for_status()
            res = r.json()
            # predictions may include output url list
            out = res.get('output')
            if out:
                # return first output (could be URL or base64 depending on model)
                return {'url': out[0] if isinstance(out, list) else out}
        except Exception as e:
            # fallback to OpenAI below
            pass
    # Try OpenAI Images if key present
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        try:
            import openai
            openai.api_key = openai_key
            res = openai.Image.create(prompt=prompt, n=1, size="512x512")
            url = res['data'][0]['url']
            return {'url': url}
        except Exception as e:
            return {'error': f'openai image error: {e}'}
    return {'error': 'No image provider configured. Set REPLICATE_API_TOKEN or OPENAI_API_KEY.'}