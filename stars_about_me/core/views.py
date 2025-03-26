from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .forms import ZodiacSignForm
from .models import QrCode, FamousQuoteLucky, WisdomLucky, ElementLucky
from random import choice
from django.http import Http404

class QRCodeDetailView(DetailView):
    model = QrCode
    template_name = 'core/luckies.html'
    context_object_name = 'qr_code'

    def get_object(self, queryset=None):
        """Fetch QR code based on qr_id from URL"""
        return get_object_or_404(QrCode, qr_id=self.kwargs['qr_id'])

    def get(self, request, *args, **kwargs):
        qr_code = self.get_object()

        # If the QR code has been scanned, show the lucky message
        if qr_code.scanned:

            lucky_type = qr_code.linked_lucky.lucky_type
            print(lucky_type)

            zodiac_signs_bg = {
                'Aries': 'Овен',
                'Taurus': 'Телец',
                'Gemini': 'Близнаци',
                'Cancer': 'Рак',
                'Leo': 'Лъв',
                'Virgo': 'Дева',
                'Libra': 'Везни',
                'Scorpio': 'Скорпион',
                'Sagittarius': 'Стрелец',
                'Capricorn': 'Козирог',
                'Aquarius': 'Водолей',
                'Pisces': 'Риби'
            }

            context = {
                'qr_code': qr_code,
                'content': qr_code.linked_lucky.content,
                'lucky_type': lucky_type,
            }

            if lucky_type == 'quote':
                template = 'core/display/quote_lucky.html'
                context['author'] = qr_code.linked_lucky.author
                context['zodiac_sign'] = zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign]

            elif lucky_type == 'wisdom':
                template = 'core/display/wisdom_lucky.html'
                context['zodiac_sign'] = zodiac_signs_bg[qr_code.linked_lucky.zodiac_sign]

            elif lucky_type == 'element':
                elements_bg = {
                    'Fire': 'Огън',
                    'Earth': 'Земя',
                    'Air': 'Въздух',
                    'Water': 'Вода'
                }
                template = 'core/display/element_lucky.html'
                context['element'] = elements_bg[qr_code.linked_lucky.element]

            else:
                template = 'core/luckies.html'  # Default template if no type matches

            return render(request, template, context)

        # Otherwise, show the form to choose a zodiac sign and lucky type
        return render(request, 'core/luckies.html', {'qr_code': qr_code, 'form': ZodiacSignForm()})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     qr_code = context['qr_code']
    #
    #     if qr_code.scanned:
    #         context['lucky'] = qr_code.linked_lucky.content
    #     else:
    #         context['form'] = ZodiacSignForm()
    #
    #     return context

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
            zodiac_sign = form.cleaned_data['zodiac_sign']
            lucky_type = form.cleaned_data['lucky_type']

            print(lucky_type)
            print(f'zodiac sign {zodiac_sign}')

            # Get lucky message based on selected zodiac sign and lucky type
            if lucky_type == 'quote':
                lucky_messages = FamousQuoteLucky.objects.filter(zodiac_sign=zodiac_sign)
                print(lucky_messages)
            elif lucky_type == 'wisdom':
                print('we are in wisdom')
                lucky_messages = WisdomLucky.objects.filter(zodiac_sign=zodiac_sign)
                print(lucky_messages)
            elif lucky_type == 'element':


                element = next((key for key, signs in ELEMENT_ZODIAC_SIGNS.items() if zodiac_sign in signs), None)

                print(element)

                lucky_messages = ElementLucky.objects.filter(element=element)

                print(lucky_messages)

            else:
                raise Http404("Lucky type not found.")

            # If there are lucky messages available for the chosen zodiac sign and type
            if lucky_messages.exists():
                lucky = choice(lucky_messages)  # Randomly choose a lucky message
                qr_code.linked_lucky = lucky
                qr_code.scanned = True
                qr_code.save()
                print(lucky_type)

                return redirect('get_lucky', qr_id=qr_code.qr_id)

        return self.get(request, *args, **kwargs)
