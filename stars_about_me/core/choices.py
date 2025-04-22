from django.db import models


class LuckyTypeChoices(models.TextChoices):
    quote = 'quote'
    wisdom = 'wisdom'
    element = 'element'
    horoscope = 'horoscope'


class ZodiacSigns(models.TextChoices):
    aries = 'Aries'
    taurus = 'Taurus'
    gemini = 'Gemini'
    cancer = 'Cancer'
    leo = 'Leo'
    virgo = 'Virgo'
    libra = 'Libra'
    scorpio = 'Scorpio'
    sagittarius = 'Sagittarius'
    capricorn = 'Capricorn'
    aquarius = 'Aquarius'
    pisces = 'Pisces'


class ElementTypeChoices(models.TextChoices):
    fire = 'Fire'
    water = 'Water'
    earth = 'Earth'
    air = 'Air'


class HoroscopeTypeChoices(models.TextChoices):
    daily = 'Daily'
    weekly = 'Weekly'