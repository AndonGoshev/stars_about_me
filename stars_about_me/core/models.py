from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from stars_about_me.core.choices import LuckyTypeChoices, ZodiacSigns, ElementTypeChoices


class LuckyBase(models.Model):
    zodiac_sign = models.CharField(max_length=20, choices=ZodiacSigns.choices, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    lucky_type = models.CharField(max_length=20, choices=LuckyTypeChoices.choices, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Lucky for {self.zodiac_sign}: {self.content[:30]}..."

class FamousQuoteLucky(LuckyBase):
    author = models.CharField(max_length=100)

class WisdomLucky(LuckyBase):
    pass  # No extra fields, just wisdom messages

class ElementLucky(LuckyBase):
    element = models.CharField(max_length=20, choices=ElementTypeChoices)



class QrCode(models.Model):
    qr_id = models.CharField(max_length=20, unique=True)
    scanned = models.BooleanField(default=False)

    lucky_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    lucky_id = models.PositiveIntegerField(null=True, blank=True)  # Make nullable
    linked_lucky = GenericForeignKey('lucky_type', 'lucky_id')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR {self.qr_id} - {'Used' if self.scanned else 'Unused'}"