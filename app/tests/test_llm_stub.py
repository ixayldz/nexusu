import asyncio
from app.core.providers import call_openai, call_claude, call_gemini

async def _run():
    assert await call_openai("sys", "hi") == "[stubbed-openai-reply]"
    assert await call_claude("sys", "hi") == "[stubbed-claude-reply]"
    assert await call_gemini("sys", "hi") == "[stubbed-gemini-reply]"

def test_llm_stubs():
    asyncio.run(_run())
