import os
from enum import Enum
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(dotenv_path="backend/.env")


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class GPTAnswers(Enum):
    LEGAL = "legal"
    ILLEGAL = "illegal"


def check_user_challenge_for_legal(challenge_text: str) -> GPTAnswers:
    def get_answer():
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an legal expert, that looks at text and \
                    decides if it is legal or illegal for a person to do that task. \
                    You will only aswer with 'legal' or 'illegal'.",
                },
                {
                    "role": "user",
                    "content": challenge_text,
                },
            ],
        )
        # print(chat_completion)
        return chat_completion.choices[0].message.content.lower()

    answer = get_answer()
    if answer not in ("legal", "illegal"):
        answer = get_answer()
    return answer
