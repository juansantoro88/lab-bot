from app.config import settings

async def ask_llm(user_text: str) -> str:
    # Si no hay Claude API key, fallback simple
    if not settings.claude_api_key:
        return f"Recibido: {user_text}"

    try:
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=settings.claude_api_key)

        msg = await client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=250,
            temperature=0.3,
            system="Eres un asistente útil y breve. Responde en español.",
            messages=[{"role": "user", "content": user_text}],
        )
        # msg.content suele ser lista de bloques
        return "".join([c.text for c in msg.content if hasattr(c, "text")]).strip() or "OK"
    except Exception as e:
        print("LLM ERROR:", str(e))
        return f"Recibido: {user_text}"