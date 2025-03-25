from django import forms

from stars_about_me.core.choices import ZodiacSigns



class ZodiacSignForm(forms.Form):
    ZODIAC_SIGNS = ZodiacSigns.choices
    LUCKY_TYPES = [
        ('quote', 'Quote'),
        ('wisdom', 'Wisdom'),
        ('element', 'Element')
    ]

    zodiac_sign = forms.ChoiceField(choices=ZODIAC_SIGNS)
    lucky_type = forms.ChoiceField(choices=LUCKY_TYPES)