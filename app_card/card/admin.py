from django.contrib import admin
from .models import Card

# Register your models here.


@admin.register(Card)
class AdminCard(admin.ModelAdmin):

    list_display = ('id', 'series', 'display_number')

    def display_number(self, obj):
        return obj.display_number()

    display_number.short_description = 'Номер карты'


admin.AdminSite.site_title = 'Управление картами'
admin.AdminSite.site_header = 'Управление картами'