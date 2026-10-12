
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field, ValidationError



# LOAD CONFIGURATION

load_dotenv()

BASE_URL = os.getenv("LLM_BASE_URL")
API_KEY = os.getenv("LLM_API_KEY")
MODEL = os.getenv("LLM_MODEL")

if not all([BASE_URL, API_KEY, MODEL]):
    raise RuntimeError(
        "Missing configuration. Check your .env file."
    )


# CREATE THE CLIENT


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=120.0
)


# DEFINE DATA MODELS


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class Conversation(BaseModel):
    messages: list[Message] = Field(default_factory=list)


# Chat history will be saved next to this script
HISTORY_FILE = (
    Path(__file__).resolve().parent / "chat_history.json"
)



# SAVE CONVERSATION


def save_chat(chat: Conversation):
    json_data = chat.model_dump_json(indent=2)

    HISTORY_FILE.write_text(
        json_data,
        encoding="utf-8"
    )

    print("Conversation saved!")


# LOAD PREVIOUS CONVERSATION


def load_chat() -> Conversation:

    if not HISTORY_FILE.exists():
        return Conversation()

    try:
        json_data = HISTORY_FILE.read_text(
            encoding="utf-8"
        )

        return Conversation.model_validate_json(
            json_data
        )

    except (OSError, ValidationError) as error:
        print("Could not load chat history:", error)
        return Conversation()


# MAIN CHATBOT

def main():

    chat = load_chat()

    print("Welcome to your local AI chatbot!")
    print("Commands: /save, /clear, /exit")

    while True:

        try:
            user_input = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):
            break

        # Handle exit
        if user_input == "/exit":
            break

        # Handle saving
        if user_input == "/save":
            try:
                save_chat(chat)
            except OSError as error:
                print("Save failed:", error)
            continue

        # Handle clearing conversation
        if user_input == "/clear":
            chat = Conversation()

            try:
                save_chat(chat)
            except OSError as error:
                print("Could not clear saved history:", error)

            print("Conversation cleared!")
            continue

        # Ignore empty messages
        if not user_input:
            continue

        # Get recent conversation history
        history = [
            message.model_dump()
            for message in chat.messages[-10:]
        ]

        # Prepare messages for the LLM
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI tutor."
            },
            *history,
            {
                "role": "user",
                "content": user_input
            }
        ]

        # Send messages to the model
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7
            )

            answer = response.choices[0].message.content

            if not answer:
                print("The model returned an empty answer.")
                continue

            # Store user's message
            chat.messages.append(
                Message(
                    role="user",
                    content=user_input
                )
            )

            # Store AI response
            chat.messages.append(
                Message(
                    role="assistant",
                    content=answer
                )
            )

            print("\nAI:", answer)

        except OpenAIError as error:
            print("API error:", error)

        except (IndexError, ValidationError) as error:
            print("Invalid model response:", error)

    # Save when exiting
    try:
        save_chat(chat)
    except OSError as error:
        print("Save failed:", error)


if __name__ == "__main__":
    main()
