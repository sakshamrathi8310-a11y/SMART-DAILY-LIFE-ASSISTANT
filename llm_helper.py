from groq import Groq

client = Groq(api_key="key")

def get_ai_suggestion(data, stress, prod, health):

    prompt = f"""
    User Data:
    Sleep: {data['sleep']}
    Screen Time: {data['screen_time']}
    Steps: {data['steps']}
    Work Hours: {data['work_hours']}
    Mood: {data['mood']}
    Food: {data['food']}

    Predictions:
    Stress: {stress}
    Productivity: {prod}
    Health: {health}

    Give short:
    - 3 suggestions
    - 1 warning
    - 1 positive insight
    """

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content