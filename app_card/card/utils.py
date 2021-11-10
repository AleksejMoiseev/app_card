from .models import Card
from django.utils import timezone
from django.db import transaction


def get_latest_number_for_series(series):
    try:
        latest_card_in_series = Card.objects.filter(series=series).latest('number')
    except Card.DoesNotExist:
        return 0
    else:
        return latest_card_in_series.number


@transaction.atomic
def create_pull_cards(amount, validity, series, max_value_for_create=1000):
    start_number = get_latest_number_for_series(series=series) + 1
    stop_number = start_number + amount
    release_date = timezone.now()
    expiration_date = release_date + validity
    cards = []
    for number in range(start_number, stop_number):
        if len(cards) == max_value_for_create:
            Card.objects.bulk_create(cards)
        cards.append(
            Card(
                series=series,
                number=number,
                release_date=release_date,
                expiration_date=expiration_date
            )
        )

    if cards:
        Card.objects.bulk_create(cards)