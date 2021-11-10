from django.contrib import admin

from .forms import FormCard
from .models import Card
from datetime import timedelta

# Register your models here.
from .utils import create_pull_cards
from django.urls import path
from django.shortcuts import render, redirect


@admin.register(Card)
class AdminCard(admin.ModelAdmin):
    form = FormCard
    change_list_template = "admin/change_list.html"
    list_display = ('display_id', 'series', 'display_number', 'release_date', 'expiration_date')
    list_per_page = 15
    list_display_links = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('generate/', self.generate),
        ]
        return my_urls + urls

    def generate(self, request):
        if request.method == "POST":
            form = self.form(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                series = form.cleaned_data['series']
                validity = timedelta(days=int(form.cleaned_data['validity']))
                create_pull_cards(
                    amount=amount,
                    validity=validity,
                    series=series
                )
                self.message_user(request, f"Your generate: {amount} cards ")
                return redirect('/admin/card/card/')
        else:
            form = self.form()
        return render(
            request, "admin/card.html", {"form": form}
        )

    def has_add_permission(self, request):
        return False

    def display_number(self, obj):
        return obj.display_number()

    def display_id(self, obj):
        return obj.pk

    display_number.short_description = 'Номер карты'
    display_id.short_description = 'Идентификационный номер'


admin.AdminSite.site_title = 'Управление картами'
admin.AdminSite.site_header = 'Управление картами'