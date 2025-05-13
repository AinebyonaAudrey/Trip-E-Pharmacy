import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from pharmacy.models import Medicine

class Command(BaseCommand):
    help = 'Imports drug data from CSV file and updates image paths'

    def handle(self, *args, **kwargs):
        csv_file = 'drug_data.csv'  # Assumes CSV is in project root
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Medicine.objects.create(
                    name=row['Drug Name'],
                    description=row['Description'],
                    category=row['Category'],
                    price=row['Price'],
                    image=row['Image Link']  # Initially uses Placehold.co URLs
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported drugs'))

        # Update image paths to local media/images/ with dynamic extension
        image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        for medicine in Medicine.objects.all():
            base_name = medicine.name.lower().replace(' ', '_')
            for ext in ['.jpg', '.jpeg', '.png']:
                image_name = f"{base_name}{ext}"
                image_path = os.path.join(image_dir, image_name)
                if os.path.exists(image_path):
                    medicine.image = f"/media/images/{image_name}"
                    break
            else:
                medicine.image = '/media/images/default.jpg'  # Fallback if no image found
            medicine.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated medicine image paths'))