from django.core.management.base import BaseCommand
from recommendations.services.market_basket_service import (
    train_and_save_market_basket
)

class Command(BaseCommand):
    help = "Train market basket model and save pickle"

    def handle(self, *args, **kwargs):
        self.stdout.write("Training Market Basket model...")
        train_and_save_market_basket()
        self.stdout.write(self.style.SUCCESS("Market Basket model saved"))
