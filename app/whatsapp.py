import httpx
from app.config import settings
from app.llm import ask_llm


GRAPH_VERSION = "v24.0"


async def send_whatsapp_text(to_wa_id: str, text: str):
    """
    Envía un mensaje usando WhatsApp Cloud API.
    Requiere WHATSAPP_TOKEN y WHATSAPP_PHONE_ID.
    """
    if not settings.whatsapp_token or not settings.whatsapp_phone_id:
        print("SEND SKIPPED: falta WHATSAPP_TOKEN o WHATSAPP_PHONE_ID")
        return

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{settings.whatsapp_phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_token}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_wa_id,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, headers=headers, json=data)

    if r.status_code >= 300:
        print("WHATSAPP SEND ERROR:", r.status_code, r.text)
    else:
        print("WHATSAPP SEND OK:", r.text)


def extract_incoming_text(payload: dict) -> tuple[str | None, str | None]:
    """
    Devuelve (from_wa_id, message_text) si el payload contiene un mensaje de texto.
    """
    try:
        entry = payload["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        messages = value.get("messages", [])
        if not messages:
            return None, None

        msg = messages[0]
        from_wa_id = msg.get("from")

        if msg.get("type") == "text":
            text = msg["text"]["body"]
            return from_wa_id, text

        return from_wa_id, None
    except Exception as e:
        print("PARSE ERROR:", str(e))
        return None, None


async def handle_whatsapp_webhook(payload: dict):
    """
    Maneja eventos entrantes. Si es mensaje de texto, responde con LLM/fallback.
    """
    from_wa_id, text = extract_incoming_text(payload)

    # Si no es mensaje (puede ser statuses, etc.)
    if not from_wa_id:
        return

    if not text:
        await send_whatsapp_text(from_wa_id, "Por ahora solo puedo leer mensajes de texto 🙂")
        return

    reply = await ask_llm(text)
    await send_whatsapp_text(from_wa_id, reply)