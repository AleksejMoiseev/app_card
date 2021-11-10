from django.contrib import admin

from .forms import FormCard
from .models import Card
from datetime import timedelta

# Register your models here.
from .utils import create_pull_cards


@admin.register(Card)
class AdminCard(admin.ModelAdmin):
    form = FormCard
    list_display = ('display_id', 'series', 'display_number')
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        amount = data['amount']
        series = data['series']
        validity = timedelta(days=int(data['validity']))
        create_pull_cards(
            amount=amount,
            validity=validity,
            series=series
        )

    def save_related(self, request, form, formsets, change):
        pass

    def display_number(self, obj):
        return obj.display_number()

    def display_id(self, obj):
        return obj.pk

    display_number.short_description = 'Номер карты'
    display_id.short_description = 'Идентификационный номер'


admin.AdminSite.site_title = 'Управление картами'
admin.AdminSite.site_header = 'Управление картами'