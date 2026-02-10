from django.core.management.base import BaseCommand
from recommendations.services.market_basket_service import (
    store_bought_together_in_redis
)

class Command(BaseCommand):
    help = "Train market basket model and save pickle"

    def handle(self, *args, **kwargs):
        self.stdout.write("Storing Market Basket model in Redis...")
        store_bought_together_in_redis()
        self.stdout.write(self.style.SUCCESS("Market Basket model stored in Redis"))
