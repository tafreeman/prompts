from tools.llm.llm_client import LLMClient
try:
    out = LLMClient.generate_text(
        'gh:openai/gpt-4o-mini',
        'Reply with exactly: SUBAGENTS_OK',
        system_instruction='You are a concise test assistant.',
        temperature=0.0,
        max_tokens=20,
    )
    print(out.strip())
except Exception as e:
    print('ERROR', type(e).__name__, str(e))
