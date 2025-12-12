from fastapi import FastAPI, Request, Response
from app.config import settings
from app.whatsapp import handle_whatsapp_message

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok", "message": "Lab bot funcionando v2"}


# ✅ Webhook verification (Meta/WhatsApp)
# Meta llama así:
# /webhook?hub.mode=subscribe&hub.verify_token=XXX&hub.challenge=12345
@app.get("/webhook")
async def webhook_verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # OJO: en tu Render env var es VERIFY_TOKEN (según tu screenshot)
    if mode == "subscribe" and token == settings.verify_token and challenge:
        return Response(content=challenge, media_type="text/plain", status_code=200)

    return Response(content="Forbidden", media_type="text/plain", status_code=403)


# ✅ Webhook receiver (POST)
@app.post("/webhook")
async def webhook_receiver(request: Request):
    payload = await request.json()
    await handle_whatsapp_message(payload)
    return Response(content="EVENT_RECEIVED", media_type="text/plain", status_code=200)
