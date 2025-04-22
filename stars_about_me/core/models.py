from datetime import timedelta

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from stars_about_me.core.choices import LuckyTypeChoices, ZodiacSigns, ElementTypeChoices, HoroscopeTypeChoices


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


class HoroscopeLucky(LuckyBase):
    horoscope_type = models.CharField(max_length=10, choices=HoroscopeTypeChoices.choices)  # Daily, Weekly, Monthly
    date = models.DateField()  # Date for the horoscope (to distinguish which day it belongs to)

    monday_date = models.DateField(null=True, blank=True)
    sunday_date = models.DateField(null=True, blank=True)

    def get_week_start_and_end(self, given_date):
        # Calculate the start (Monday) and end (Sunday) of the week
        start_of_week = given_date - timedelta(days=given_date.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        return start_of_week, end_of_week

    def save(self, *args, **kwargs):
        # If `week_monday` and `week_sunday` are not set, calculate them based on `date`
        if not self.monday_date or not self.sunday_date:
            start_of_week, end_of_week = self.get_week_start_and_end(self.date)
            # Save the Monday and Sunday of the week
            self.monday_date = start_of_week
            self.sunday_date = end_of_week

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.horoscope_type.capitalize()} Horoscope for {self.zodiac_sign} on {self.date}: {self.content[:30]}..."



class QrCode(models.Model):
    qr_id = models.CharField(max_length=20, unique=True)
    scanned = models.BooleanField(default=False)

    lucky_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    lucky_id = models.PositiveIntegerField(null=True, blank=True)  # Make nullable
    linked_lucky = GenericForeignKey('lucky_type', 'lucky_id')
    linked_lucky_type = models.CharField(max_length=20, null=True, blank=True)  # Add this line
    horoscope_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR {self.qr_id} - {'Used' if self.scanned else 'Unused'}"