import os
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('OPENAI_KEY')

PROMPT = """You help users by generating checklists from a given user prompt. Take your time determining what items should be included on the checklist. Give as many items as you can think of. Checklist items should be comma delimited.
Here is an example.
Prompt: Generate a checklist for a hiking trip
Checklist: Sleeping bag, sleeping pad, backpack, tent, water bottles, hiking shoes or boots, hiking poles, shirt, pants, headlamp, water filtration device, bug spray, sunscreen"""


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


def create_checklist_name(message: str):
    prompt = f"""Create a brief name for a checklist that would be created from a message.
    Message: Create a checklist for a snowboarding trip
    Name: Snowboarding Trip
    
    Message: {message}
    Name: """

    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=8
    )

    return str(completion.choices[0].text).strip().replace("\n", "")


def list_models():
    return openai.Model.list()


if __name__ == "__main__":
    # print(list_models())
    # test_message = "Generate a checklist for a long day out paddleboarding"
    # checklist = create_checklist(test_message)

    test_message = "Generate a checklist for a two-day hiking trip"
    subject = create_checklist_name(test_message)

    # print(checklist)
    print(subject)
