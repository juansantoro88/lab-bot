import json
from fastapi import FastAPI, Request, Response
from app.config import settings
from app.whatsapp import handle_whatsapp_webhook

app = FastAPI()


# Healthcheck (Render hace HEAD /)
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

    if mode == "subscribe" and token == settings.verify_token and challenge:
        return Response(content=challenge, media_type="text/plain", status_code=200)

    return Response(content="Forbidden", media_type="text/plain", status_code=403)


# Webhook receiver (POST)
@app.post("/webhook")
async def webhook_receiver(request: Request):
    payload = await request.json()

    # Log corto para ver en Render logs (clave para debug)
    print("EVENT HIT:", json.dumps(payload)[:2000])

    await handle_whatsapp_webhook(payload)
    return Response(content="EVENT_RECEIVED", media_type="text/plain", status_code=200)