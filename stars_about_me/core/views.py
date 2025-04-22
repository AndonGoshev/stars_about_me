from datetime import timedelta

from dateutil.utils import today
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .forms import ZodiacSignForm
from .models import QrCode, FamousQuoteLucky, WisdomLucky, ElementLucky, HoroscopeLucky
from random import choice
from django.http import Http404


class QRCodeDetailView(DetailView):
    model = QrCode
    template_name = 'core/luckies.html'
    context_object_name = 'qr_code'

    def show_lucky(self, qr_code, second_submit=False):

        # Try to get lucky_type from linked_lucky, or fallback to linked_lucky_type
        lucky_type = getattr(qr_code.linked_lucky, 'lucky_type', None) or qr_code.linked_lucky_type

        zodiac_signs_bg = {
            'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнаци', 'Cancer': 'Рак',
            'Leo': 'Лъв', 'Virgo': 'Дева', 'Libra': 'Везни', 'Scorpio': 'Скорпион',
            'Sagittarius': 'Стрелец', 'Capricorn': 'Козирог', 'Aquarius': 'Водолей', 'Pisces': 'Риби'
        }

        context = {
            'qr_code': qr_code,
            'second_submit': second_submit,
            'lucky_type': lucky_type,
        }

        if lucky_type == 'quote':
            print('clicked')
            template = 'core/display/display.html'
            context.update({
                'content': qr_code.linked_lucky.content,
                'author': qr_code.linked_lucky.author,
                'zodiac_sign': zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign],
                'zodiac_sign_eng': qr_code.linked_lucky.zodiac_sign,
            })

        elif lucky_type == 'wisdom':
            template = 'core/display/display.html'
            context.update({
                'content': qr_code.linked_lucky.content,
                'zodiac_sign': zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign],
                'zodiac_sign_eng': qr_code.linked_lucky.zodiac_sign,
            })

        elif lucky_type == 'element':
            elements_bg = {
                'Fire': 'Огън', 'Earth': 'Земя', 'Air': 'Въздух', 'Water': 'Вода'
            }
            template = 'core/display/display.html'
            context.update({
                'content': qr_code.linked_lucky.content,
                'element': elements_bg[qr_code.linked_lucky.element],
                'element_eng': qr_code.linked_lucky.element,
            })


        elif lucky_type == 'horoscope':

            horoscope_type_map = {
                'Daily': 'дневен',
                'Weekly': 'седмичен',
                'monthly': 'месечен',
            }

            template = 'core/display/display.html'
            # months_bg = [
            #     "", "Януари", "Февруари", "Март", "Април", "Май", "Юни",
            #     "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"
            # ]
            # month_name_bg = months_bg[qr_code.linked_lucky.month_date.month] if qr_code.linked_lucky.month_date else ""

            context.update({
                'content': qr_code.linked_lucky.content,
                'zodiac_sign': zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign],
                'zodiac_sign_eng': qr_code.linked_lucky.zodiac_sign,
                'horoscope_type': horoscope_type_map[qr_code.linked_lucky.horoscope_type],
                'monday_date': qr_code.linked_lucky.monday_date,
                'sunday_date': qr_code.linked_lucky.sunday_date,
                'today_date': today(),
            })

        else:
            template = 'core/luckies.html'

        return render(self.request, template, context)

    def get_object(self, queryset=None):
        """Fetch QR code based on qr_id from URL"""
        return get_object_or_404(QrCode, qr_id=self.kwargs['qr_id'])

    def get(self, request, *args, **kwargs):
        qr_code = self.get_object()

        # If the QR code has been scanned, show the lucky message
        if qr_code.scanned:
            return self.show_lucky(qr_code)

        # Otherwise, show the form to choose a zodiac sign and lucky type
        return render(request, 'core/luckies.html', {'qr_code': qr_code, 'form': ZodiacSignForm()})

    def post(self, request, *args, **kwargs):
        form = ZodiacSignForm(request.POST)

        ELEMENT_ZODIAC_SIGNS = {
            'Fire': ['Aries', 'Sagittarius', 'Leo'],
            'Earth': ['Taurus', 'Virgo', 'Capricorn'],
            'Air': ['Gemini', 'Libra', 'Aquarius'],
            'Water': ['Cancer', 'Scorpio', 'Pisces']
        }

        if form.is_valid():
            qr_code = self.get_object()
            if qr_code.scanned:
                return self.show_lucky(qr_code, True)

            zodiac_sign = form.cleaned_data['zodiac_sign']
            lucky_type = form.cleaned_data['lucky_type']

            # Get lucky message based on selected zodiac sign and lucky type
            if lucky_type == 'quote':
                lucky_messages = FamousQuoteLucky.objects.filter(zodiac_sign=zodiac_sign)

            elif lucky_type == 'wisdom':

                lucky_messages = WisdomLucky.objects.filter(zodiac_sign=zodiac_sign)

            elif lucky_type == 'element':
                element = next((key for key, signs in ELEMENT_ZODIAC_SIGNS.items() if zodiac_sign in signs), None)
                lucky_messages = ElementLucky.objects.filter(element=element)




            elif lucky_type == 'horoscope':
                horoscope_type = form.cleaned_data['horoscope_type']
                print(horoscope_type)
                lucky_messages = HoroscopeLucky.objects.filter(
                    zodiac_sign=zodiac_sign,
                    horoscope_type=horoscope_type.capitalize()
                )

            else:
                raise Http404("Lucky type not found.")


            # If there are lucky messages available for the chosen zodiac sign and type
            if lucky_messages.exists():
                lucky = choice(lucky_messages)  # Randomly choose a lucky message
                qr_code.linked_lucky = lucky
                qr_code.scanned = True
                qr_code.save()

                return redirect('get_lucky', qr_id=qr_code.qr_id)

        return self.get(request, *args, **kwargs)
