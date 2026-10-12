
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Read one configuration variable
model_name = os.getenv("LLM_MODEL")

print("Model:", model_name)
print("Server:", os.getenv("LLM_BASE_URL"))
print("API key configured:", bool(os.getenv("LLM_API_KEY")))
