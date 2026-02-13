import os
for k in [
    'GITHUB_TOKEN','GH_TOKEN','PROMPTEVAL_ALLOW_REMOTE',
    'OPENAI_API_KEY','GEMINI_API_KEY','GOOGLE_API_KEY','ANTHROPIC_API_KEY'
]:
    v=os.getenv(k)
    print(k, bool(v), (v[:4]+'...') if v else None)
