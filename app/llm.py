from anthropic import Anthropic
from app.config import settings

# Cambia el modelo aquí si te vuelve a dar 404
CLAUDE_MODEL = "claude-3-5-haiku-20241022"

client = Anthropic(api_key=settings.claude_api_key)

async def ask_llm(message: str) -> str:
    if not settings.claude_api_key:
        return "No tengo configurada la clave de Claude todavía."

    try:
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=300,
            temperature=0.2,
            system="Responde breve y claro en español.",
            messages=[{"role": "user", "content": message}],
        )
        # SDK devuelve lista de bloques; normalmente el primero es texto
        return resp.content[0].text if resp.content else "OK"
    except Exception as e:
        return f"Error con LLM: {e}"