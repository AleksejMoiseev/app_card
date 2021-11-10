from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your models here.

SERIES_MIN_VALUE = 1000
SERIES_MAX_VALUE = 9999

NUMBER_MIN_VALUE = 1
NUMBER_MAX_VALUE = 999999

THREE_YEARS = timedelta(days=1095)
ONE_YEAR = timedelta(days=365)
SIX_MONTH = timedelta(days=180)
ONE_MONTH = timedelta(days=30)


class Card(models.Model):
    VALIDITY_CHOICES = (
        (THREE_YEARS, '3 years'),
        (ONE_YEAR, '1 year'),
        (SIX_MONTH, '6 months'),
        (ONE_MONTH, '1 month'),
    )

    series = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(SERIES_MIN_VALUE),
                    MaxValueValidator(SERIES_MAX_VALUE)]
    )
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(NUMBER_MIN_VALUE),
                    MaxValueValidator(NUMBER_MAX_VALUE)]
    )
    release_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        unique_together = ['series', 'number']
        constraints = [
            models.CheckConstraint(
                check=models.Q(series__gte=SERIES_MIN_VALUE) & Q(series__lte=SERIES_MAX_VALUE),
                name='series__value'),
            models.CheckConstraint(
                check=models.Q(number__gte=NUMBER_MIN_VALUE) & Q(number__lte=NUMBER_MAX_VALUE),
                name='number_value')
        ]

    def display_number(self):
        return '{0: 07}'.format(self.number).strip()

    def __str__(self):
        return f'Card № {self.pk} Series: {self.series} Number {self.display_number()}'
