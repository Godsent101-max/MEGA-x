Replicate Integration Notes
---------------------------
- Replicate requires a model 'version' id when calling the predictions endpoint.
- For Stable Diffusion, find a public model and its version id on https://replicate.com.
- Replace the placeholder 'version' in backend/image_routes.py with the real version id.
- Consider using the official replicate Python client for easier interaction:
    pip install replicate
    import replicate
    client = replicate.Client(api_token=os.getenv('REPLICATE_API_TOKEN'))
    output = client.predict("owner/model:version", input={"prompt": "..."})