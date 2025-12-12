from anthropic import Anthropic
from app.config import settings
import json

# Cliente de Claude usando tu API Key del .env
client = Anthropic(api_key=settings.claude_api_key)

async def ask_llm(message: str) -> dict:
    """
    Envía el mensaje del usuario a Claude y devuelve una respuesta estructurada.
    Si hay algún error con la API, devolvemos una respuesta de emergencia
    y mostramos el error en consola.
    """

    system_prompt = """
Eres un asistente de un centro médico / laboratorio.
Respondes SIEMPRE en español, de forma clara y amable.

Devuelve SIEMPRE la respuesta en ESTE FORMATO JSON:

{
  "answer": "texto que debo enviar al usuario",
  "action": "none"
}

- "answer": es la respuesta en texto para el paciente.
- "action": de momento siempre "none".
NUNCA devuelvas nada fuera de este JSON.
"""

    try:
        # Llamada a la API de Claude
        response = client.messages.create(
            # Usa un modelo moderno. Puedes usar también
            # el que te sale en el panel: "claude-sonnet-4-20250514"
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            temperature=0.2,
            system=system_prompt,
            messages=[
                {"role": "user", "content": message}
            ],
        )

        raw_text = response.content[0].text

        # Intentamos parsear el JSON que devuelve Claude
        try:
            parsed = json.loads(raw_text)
        except Exception:
            # Si por algún motivo no devuelve JSON perfecto,
            # envolvemos el texto en un JSON nosotros.
            parsed = {
                "answer": raw_text,
                "action": "none"
            }

        return parsed

    except Exception as e:
        # Aquí capturamos errores de API (model incorrecto, API key, red, etc.)
        print("=== ERROR llamando a Claude ===")
        print(repr(e))

        # Devolvemos una respuesta segura para que el endpoint no reviente
        return {
            "answer": "Ahora mismo tengo un problema técnico para consultar la IA. Inténtalo de nuevo en unos minutos.",
            "action": "none"
        }