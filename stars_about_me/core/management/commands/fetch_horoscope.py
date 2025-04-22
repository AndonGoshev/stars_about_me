import time
from datetime import date

from django.core.management import BaseCommand

from stars_about_me.core.choices import ZodiacSigns, HoroscopeTypeChoices
from stars_about_me.core.horoscope_helpers.daily_aspects import daily_aspects
from stars_about_me.core.horoscope_helpers.daily_horocope import daily_horoscope
from stars_about_me.core.horoscope_helpers.weekly_aspects import weekly_aspects
from stars_about_me.core.horoscope_helpers.weekly_horoscope import weekly_horoscope
from stars_about_me.core.models import HoroscopeLucky


class Command(BaseCommand):
    help = "Fetch daily and weekly horoscopes, translate them, and store in the database."

    def handle(self, *args, **options):

        horoscope_full_response_time = 0

        daily_aspects_data = daily_aspects()
        weekly_aspects_data = weekly_aspects()

        self.stdout.write(self.style.SUCCESS('Starting horoscope fetch process...'))

        for sign in ZodiacSigns.values:
            self.stdout.write(f'Fetching horoscopes for {sign}...')

            for horoscope_type in HoroscopeTypeChoices:

                zodiac_entry = HoroscopeLucky.objects.filter(zodiac_sign=sign, horoscope_type=horoscope_type).first()

                if not zodiac_entry:
                    self.stdout.write(f'No horoscope for {horoscope_type} for {sign}')
                    continue


                start_time = time.time()
                print(f"Start time: {start_time}")

                if horoscope_type == 'Daily':
                    zodiac_entry.content = daily_horoscope(sign, daily_aspects_data)
                elif horoscope_type == 'Weekly':
                    zodiac_entry.content = weekly_horoscope(sign, weekly_aspects_data)
                zodiac_entry.lucky_type = 'horoscope'
                zodiac_entry.date = date.today()
                zodiac_entry.save()

                end_time = time.time()
                total_time = end_time - start_time
                print(f'Response time: {total_time} seconds')

                horoscope_full_response_time += total_time

        self.stdout.write(self.style.SUCCESS(f'Fetching completed. Full response time: {round(horoscope_full_response_time, 3)} seconds.'))
