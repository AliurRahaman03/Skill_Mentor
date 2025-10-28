import os
from openai import OpenAI

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
#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
def generate_roadmap(user_name, skills, target_role="Full Stack Developer"):
    prompt = f"""
You are an expert tech mentor. Create a 6-week learning roadmap for {user_name},
who currently knows {', '.join(skills)} and wants to become a {target_role}.
Return JSON like: {{ "title": "...", "weeks": {{ "week_1": [...], ... }} }}
"""
    response = client.chat.completions.create(
        model="openai/gpt-5-image-mini",  # Using more widely available model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    try:
        # New API returns a structured object
        text = response.choices[0].message.content
        import json
        data = json.loads(text)
    except Exception as e:
        data = {
            "title": "AI Response Error",
            "weeks": {},
            "error": str(e)
        }
    return data
