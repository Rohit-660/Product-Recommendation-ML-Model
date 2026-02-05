from django.core.management.base import BaseCommand
from recommendations.services.als_inference_service import (
    generate_top_buys_from_model
)

class Command(BaseCommand):
    help = "Generate Top Buys in Redis using trained ALS model"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating Top Buys...")
        generate_top_buys_from_model()
        self.stdout.write(self.style.SUCCESS("Top Buys stored in Redis"))
