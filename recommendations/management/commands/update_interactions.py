from django.core.management.base import BaseCommand
from recommendations.services.interaction_service import (
    update_user_product_interactions
)

class Command(BaseCommand):
    help = "Update user-product interaction table incrementally"

    def handle(self, *args, **kwargs):
        self.stdout.write("Updating interactions...")
        update_user_product_interactions()
        self.stdout.write(self.style.SUCCESS("Interactions updated"))
