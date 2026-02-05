from django.core.management.base import BaseCommand
from recommendations.services.als_training_service import (
    train_and_save_als_model
)

class Command(BaseCommand):
    help = "Train ALS model and save pickle"

    def handle(self, *args, **kwargs):
        self.stdout.write("Training ALS model...")
        train_and_save_als_model()
        self.stdout.write(self.style.SUCCESS("ALS model saved"))
