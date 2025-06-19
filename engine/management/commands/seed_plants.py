from django.core.management.base import BaseCommand
from engine.models import PlantSpecies

class Command(BaseCommand):
    help = 'Seeds the database with plant species'

    def handle(self, *args, **kwargs):
        data = [
            {"name": "Сосна", "growth_rate": 0.8, "aggression": 0.6, "light_preference": "sun", "max_radius": 3.0, "max_height": 15.0},
            {"name": "Берёза", "growth_rate": 1.0, "aggression": 0.5, "light_preference": "partial", "max_radius": 2.5, "max_height": 12.0},
            {"name": "Крапива", "growth_rate": 1.2, "aggression": 0.9, "light_preference": "sun", "max_radius": 0.8, "max_height": 1.5},
            {"name": "Папоротник", "growth_rate": 0.6, "aggression": 0.3, "light_preference": "shade", "max_radius": 1.2, "max_height": 0.5},
            {"name": "Мох", "growth_rate": 0.3, "aggression": 0.2, "light_preference": "shade", "max_radius": 0.5, "max_height": 0.2},
        ]

        for item in data:
            obj, created = PlantSpecies.objects.get_or_create(name=item["name"], defaults=item)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {item['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"{item['name']} already exists"))
