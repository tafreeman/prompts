from tools.llm.llm_client import LLMClient
try:
    out = LLMClient.generate_text('local:phi4','Say OK in one word.')
    print('SUCCESS', out[:200])
except Exception as e:
    print('ERROR', type(e).__name__, str(e)[:500])
