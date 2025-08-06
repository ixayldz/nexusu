"""
Tek noktadan LLM erişimi.
• Test / CI’de LIVE=False ⇒ stub cevap döner, dış API yok.
• Gerçek çağrı için ortam değişkeni: ENABLE_LIVE_LLM=true
"""

import os
from typing import Any, Dict

import openai
import anthropic
import google.generativeai as genai

# ────────────────────────────────────────────────────────────────────────────
# 1) Canlı mı, stub mu?
#    Varsayılan: FALSE  → güvenli (stub)
# ────────────────────────────────────────────────────────────────────────────
LIVE = os.getenv("ENABLE_LIVE_LLM", "false").lower() == "true"

# ────────────────────────────────────────────────────────────────────────────
# 2) OpenAI o3
# ────────────────────────────────────────────────────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY", "")

async def call_openai(system: str, user: str) -> str:
    if not LIVE:
        return "[stubbed-openai-reply]"
    client = openai.AsyncOpenAI()
    chat = await client.chat.completions.create(
        model="o3",
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=0.2,
    )
    return chat.choices[0].message.content


# ────────────────────────────────────────────────────────────────────────────
# 3) Anthropic Claude 4 Sonnet
# ────────────────────────────────────────────────────────────────────────────
anthropic_client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

async def call_claude(system: str, user: str) -> str:
    if not LIVE:
        return "[stubbed-claude-reply]"
    chat = await anthropic_client.messages.create(
        model="claude-4-sonnet-20240229",
        system=system,
        messages=[{"role": "user", "content": user}],
        max_tokens=2048,
    )
    return chat.content[0].text


# ────────────────────────────────────────────────────────────────────────────
# 4) Google Gemini 2.5 Pro
# ────────────────────────────────────────────────────────────────────────────
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))

async def call_gemini(system: str, user: str) -> str:
    if not LIVE:
        return "[stubbed-gemini-reply]"
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    resp = await model.generate_content_async(
        [system, user], generation_config={"temperature": 0.2}
    )
    return resp.text


# ────────────────────────────────────────────────────────────────────────────
# 5) Genel seçim yordamı
# ────────────────────────────────────────────────────────────────────────────
def llm_call(model_name: str):
    mapping = {
        "openai-o3": call_openai,
        "claude-4-sonnet": call_claude,
        "gemini-2.5-pro": call_gemini,
    }
    return mapping.get(model_name, lambda *_: "[unknown-model]")
