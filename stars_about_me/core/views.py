from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .forms import ZodiacSignForm
from .horoscope_api.chat_gpt import translate_to_bulgarian
from .horoscope_api.fetch_api import _fetch_horoscope, get_daily_horoscope, get_weekly_horoscope, get_monthly_horoscope
from .models import QrCode, FamousQuoteLucky, WisdomLucky, ElementLucky
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
            template = 'core/display/quote_lucky.html'
            context.update({
                'content': qr_code.linked_lucky.content,
                'author': qr_code.linked_lucky.author,
                'zodiac_sign': zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign],
                'zodiac_sign_eng': qr_code.linked_lucky.zodiac_sign,
            })

        elif lucky_type == 'wisdom':
            template = 'core/display/wisdom_lucky.html'
            context.update({
                'content': qr_code.linked_lucky.content,
                'zodiac_sign': zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign],
                'zodiac_sign_eng': qr_code.linked_lucky.zodiac_sign,
            })

        elif lucky_type == 'element':
            elements_bg = {
                'Fire': 'Огън', 'Earth': 'Земя', 'Air': 'Въздух', 'Water': 'Вода'
            }
            template = 'core/display/element_lucky.html'
            context.update({
                'content': qr_code.linked_lucky.content,
                'element': elements_bg[qr_code.linked_lucky.element],
                'element_eng': qr_code.linked_lucky.element,
            })


        elif lucky_type == 'horoscope':
            if qr_code.scanned:
                template = 'core/display/horoscope_limit.html'
                context.update({
                    'message': 'Този QR код вече е използван за хороскоп. Моля, изтеглете ново късметче.',
                })

            else:
                template = 'core/display/horoscope_lucky.html'
                qr_code.scanned = True
                qr_code.save()

                json_response = {}

                if qr_code.horoscope_data['horoscope_type'] == 'daily':
                    json_response = get_daily_horoscope(qr_code.horoscope_data['zodiac_sign'])

                elif qr_code.horoscope_data['horoscope_type'] == 'weekly':
                    json_response = get_weekly_horoscope(qr_code.horoscope_data['zodiac_sign'])

                elif qr_code.horoscope_data['horoscope_type'] == 'monthly':
                    json_response = get_monthly_horoscope(qr_code.horoscope_data['zodiac_sign'])

                print(translate_to_bulgarian(json_response['horoscope_data']))

                context.update({
                    'message': 'this is the horoscope',
                    'zodiq': qr_code.horoscope_data['zodiac_sign'],
                    'horoskop': qr_code.horoscope_data['horoscope_type'],
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
                qr_code.linked_lucky_type = 'horoscope'

                qr_code.horoscope_data = {
                    'zodiac_sign': form.cleaned_data['zodiac_sign'],
                    'horoscope_type': form.cleaned_data['horoscope_type'],
                }

                qr_code.save()

                # Call show_lucky to display the horoscope message
                return self.show_lucky(qr_code)

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
