import os
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('OPENAI_KEY')

PROMPT = """You help users by generating checklists from a given user prompt. Take your time determining what items should be included on the checklist. Give as many items as you can think of. Checklist items should be comma delimited.
Here is an example.
Prompt: Generate a checklist for a hiking trip
Checklist: Sleeping bag, sleeping pad, backpack, tent, water bottles, hiking shoes or boots, hiking poles, shirt, pants, headlamp, water filtration device"""


def create_checklist(message: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": message}
        ]
    )

    response = completion.choices[0].message["content"]

    return str(response).split(', ')


if __name__ == "__main__":
    test_message = "Generate a checklist for a long day out paddleboarding"
    checklist = create_checklist(test_message)

    print(checklist)
