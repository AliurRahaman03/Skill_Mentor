from openai import OpenAI

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="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")

def generate_roadmap(user_name, skills, target_role="Full Stack Developer"):
    prompt = f"""
You are an expert tech mentor. Create a 6-week learning roadmap for {user_name},
who currently knows {', '.join(skills)} and wants to become a {target_role}.
Return JSON like: {{ "title": "...", "weeks": {{ "week_1": [...], ... }} }}
"""
    response = client.chat.completions.create(
        model="openrouter/andromeda-alpha",  # Using more widely available model
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
