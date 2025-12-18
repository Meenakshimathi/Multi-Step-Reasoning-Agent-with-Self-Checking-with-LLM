from together import Together

# ⚠️ Hardcoded key (assignment-only)
TOGETHER_API_KEY = "tgp_v1_YoPbQ8A13NCfQieTpQdUiTdAjszSzo7YS8U31QR1Mh0"

client = Together(api_key=TOGETHER_API_KEY)

# ✅ THIS MODEL IS SERVERLESS
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

def call_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content
