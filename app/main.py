from fastapi import FastAPI, Request, Response
from app.config import settings
from app.whatsapp import handle_whatsapp_message
import json

app = FastAPI()


# Healthcheck (Render manda HEAD)
@app.get("/")
def root():
    return {"status": "ok", "message": "Lab bot funcionando"}

# Endpoint de verificación (para WhatsApp, más adelante)
@app.get("/webhook")
async def verify(mode: str = "", challenge: str = "", token: str = ""):
    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        return int(challenge)
    return {"error": "verification failed"}

# Endpoint que recibe mensajes (POST)
@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print("EVENT HIT:", json.dumps(payload)[:2000])
    await handle_whatsapp_message(payload)
    return "EVENT_RECEIVED"