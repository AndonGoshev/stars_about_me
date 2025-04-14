import time

from openai import OpenAI

from stars_about_me import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def translate_to_bulgarian(text):
    start_time = time.time()
    print(start_time)
    response = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "system", "content": "Translate the following horoscope to Bulgarian and make it up to 500 chars but dont change any of the meaning:"},
            {"role": "user", "content": text}
        ]
    )

    end_time = time.time()

    print(f'response time = {end_time - start_time}')
    return response.choices[0].message.content
