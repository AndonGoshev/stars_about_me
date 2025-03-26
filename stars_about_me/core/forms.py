from django import forms

from stars_about_me.core.choices import ZodiacSigns



class ZodiacSignForm(forms.Form):
    ZODIAC_SIGN_CHOICES = [
        ('Aries', 'Овен'),
        ('Taurus', 'Телец'),
        ('Gemini', 'Близнаци'),
        ('Cancer', 'Рак'),
        ('Leo', 'Лъв'),
        ('Virgo', 'Дева'),
        ('Libra', 'Везни'),
        ('Scorpio', 'Скорпион'),
        ('Sagittarius', 'Стрелец'),
        ('Capricorn', 'Козирог'),
        ('Aquarius', 'Водолей'),
        ('Pisces', 'Риби'),
    ]
    LUCKY_TYPES = [
        ('quote', 'Quote'),
        ('wisdom', 'Wisdom'),
        ('element', 'Element')
    ]

    zodiac_sign = forms.ChoiceField(
        choices=ZODIAC_SIGN_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'zodiac-radio'})
    )
    lucky_type = forms.ChoiceField(choices=LUCKY_TYPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert the bound field (a list of radio widgets) to a dictionary.
        bound_zodiac = list(self['zodiac_sign'])
        self.zodiac_signs = {
            'aries': bound_zodiac[0],
            'taurus': bound_zodiac[1],
            'gemini': bound_zodiac[2],
            'cancer': bound_zodiac[3],
            'leo': bound_zodiac[4],
            'virgo': bound_zodiac[5],
            'libra': bound_zodiac[6],
            'scorpio': bound_zodiac[7],
            'sagittarius': bound_zodiac[8],
            'capricorn': bound_zodiac[9],
            'aquarius': bound_zodiac[10],
            'pisces': bound_zodiac[11],
        }