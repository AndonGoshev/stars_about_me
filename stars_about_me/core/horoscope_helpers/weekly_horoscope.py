import time
from openai import OpenAI
from stars_about_me import settings
from stars_about_me.core.horoscope_helpers.daily_aspects import daily_aspects
from stars_about_me.core.horoscope_helpers.weekly_aspects import weekly_aspects

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def weekly_horoscope(sign, aspects):
    try:

        # Combine the sign and aspects to be included in the prompt
        user_content = f"Sign: {sign}\nPlanetary Aspects:\n{aspects}"

        # Call OpenAI API to generate horoscope
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            temperature=0.5,
            messages=[
                {"role": "system", "content": f"""
                                You are astrologer!

                                Use formal language so it can be good for any gender ,dont use overcomplicate the words , dont use complex astrological terms ,just make the copy accessible for everyone. Simple yet emotionally powerful.

                                Write a weekly horoscope in bulgarian grammatically correct , in "The pattern" astrology app vibe!

                                **This is important - You can mention one of the planetary aspects, ***pick randomly*** one and how they affect."

                                **Think of how the planetary aspects will personally influence the person for the given sign. And your answer should be different for any a different sign based on the planets. Also make sure that for all the signs the horoscope will be different use very personal approach.**

                                Use the sign and the planetary aspects that the user provides to create the horoscope!

                                The text style is reflective, introspective, and personalized, offering gentle guidance with a focus on emotional depth,
                                 self-awareness, and growth, while encouraging a sense of empowerment.

                                Maximum length 128 words.

                                Dont mention the sign.

                                """},
                {"role": "user", "content": user_content, }
            ]
        )

        # Fixed line for correct access
        horoscope_text = response.choices[0].message.content
        return horoscope_text

    except Exception as e:
        print(f"Error: {e}")
        return None
