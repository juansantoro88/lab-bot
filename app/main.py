from fastapi import FastAPI, Request, Response
from app.config import settings
from app.whatsapp import handle_whatsapp_message
import json

app = FastAPI()

# Healthcheck (Render manda HEAD)
@app.get("/")
@app.head("/")
async def root():
    return {"status": "ok", "message": "Lab bot funcionando v2"}

# Meta Webhook Verify (GET)
@app.get("/webhook")
async def webhook_verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("VERIFY HIT:", mode, token, challenge, "EXPECTED:", settings.verify_token)

    if mode == "subscribe" and token == settings.verify_token and challenge is not None:
        # DEBE ser texto plano
        return Response(content=str(challenge), media_type="text/plain", status_code=200)

    return Response(content="Forbidden", media_type="text/plain", status_code=403)

# Meta Webhook Events (POST)
@app.post("/webhook")
async def webhook_events(request: Request):
    payload = await request.json()
    print("EVENT HIT:", json.dumps(payload)[:2000])
    await handle_whatsapp_message(payload)
<<<<<<< HEAD
    return Response(content="EVENT_RECEIVED", media_type="text/plain", status_code=200)
=======
    return Response(content="EVENT_RECEIVED", media_type="text/plain", status_code=200)
>>>>>>> 3933034 (Webhook v2 y healthcheck)
