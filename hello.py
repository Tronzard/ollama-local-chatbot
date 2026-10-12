
import os

from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load configuration
load_dotenv()

# Step 2: Create an LLM API client
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
    timeout=120.0
)

# Step 3: Send a message to the model
response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[
        {
            "role": "user",
            "content": "Explain neural networks in simple words."
        }
    ]
)

# Step 4: Display the answer
answer = response.choices[0].message.content

print("AI:", answer)
