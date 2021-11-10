from django import forms
from .models import Card, NUMBER_MAX_VALUE, NUMBER_MIN_VALUE
from rest_framework.exceptions import ValidationError

from .utils import get_latest_number_for_series


class FormCard(forms.ModelForm):
    amount = forms.IntegerField(min_value=NUMBER_MIN_VALUE, max_value=NUMBER_MAX_VALUE)
    validity = forms.ChoiceField(choices=Card.VALIDITY_CHOICES)

    class Meta:
        model = Card
        exclude = ['number', 'release_date', 'expiration_date']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        series = self.cleaned_data['series']
        latest_number = get_latest_number_for_series(series=series)
        free = NUMBER_MAX_VALUE - latest_number
        if amount > free:
            return ValidationError('The number of requested cards is not available in this series'.format(series))
        return amount

    def save(self, commit=True):
        return self.instance
