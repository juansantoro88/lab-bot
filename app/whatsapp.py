import json
from app.llm import ask_llm

async def handle_whatsapp_message(payload: dict):
    print("=== Payload recibido en /webhook ===")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    # Extraer mensaje enviado por el usuario (aún formato dummy)
    user_message = payload.get("text") or ""

    # Enviar ese mensaje a la IA (mock)
    response = await ask_llm(user_message)

    print("=== Respuesta IA ===")
    print(response)

    return response