from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from PIL import Image
import os
from django.conf import settings

# Create your models here.


STATUS = [
    ("Available", "Available"),
    ("Rented", "Rented"),
    ("Maintenance", "Maintenance"),
]

CURRENT_YEAR = datetime.now().year
YEAR_CHOICES = [(r, r) for r in range(CURRENT_YEAR - 6, CURRENT_YEAR + 1)]


class Brand(models.Model):
    brand = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        self.brand = self.brand.title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.brand


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=20)
    # image = models.ImageField(upload_to="models/", default="")

    def save(self, *args, **kwargs):
        self.model_name = self.model_name.title()
        super().save(*args, **kwargs)
        


    def __str__(self):
        return self.model_name


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    plate_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(choices=STATUS, default="Available")
    price_per_day = models.DecimalField(decimal_places=2, max_digits=6)
    image = models.ImageField(upload_to="cars/", default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.plate_number = self.plate_number.upper()
        if self.plate_number.startswith("WW"):
            self.plate_number = self.plate_number.replace("-", "")
        super().save(*args, **kwargs)
        if self.image:
                img_path = self.image.path
                img = Image.open(img_path)

                # Make the image square by cropping the center
                width, height = img.size
                min_dim = min(width, height)
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2
                img = img.crop((left, top, right, bottom))

                # Resize to a standard size
                img = img.resize((500, 500))

                # New WebP path
                webp_path = os.path.splitext(img_path)[0] + '.webp'

                # Save as WebP
                img.save(webp_path, 'WEBP', quality=85)

                # Update the model's image field
                self.image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)

                # Delete old image if not webp
                if not img_path.endswith('.webp'):
                    os.remove(img_path)

                super().save(update_fields=['image'])  # Save with updated path

    def __str__(self):
        return f"{self.brand} {self.model}"


class Client(models.Model):
    first_name = models.CharField(max_length=15, null=False)
    last_name = models.CharField(max_length=15, null=False)
    phone = models.CharField(max_length=15, null=False)
    cin = models.ImageField(upload_to="clients/cin/")
    driver_licence = models.ImageField(upload_to="clients/licence/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_client')
        ]

    # full_name = models.CharField(max_length=50, editable=False, unique=True, default=f"{first_name} {last_name}")

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if self.cin and self.driver_licence:
    #         cin_path = self.cin.path
    #         licence_path = self.driver_licence.path

    #         cin_name = os.path.splitext(self.full_name + "_cin" + os.path.splitext(cin_path)[1])
            

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.cin:
    #             img_path = self.cin.path
    #             img = Image.open(img_path)

    #             # Make the image square by cropping the center
    #             width, height = img.size
    #             min_dim = min(width, height)
    #             left = (width - min_dim) / 2
    #             top = (height - min_dim) / 2
    #             right = (width + min_dim) / 2
    #             bottom = (height + min_dim) / 2
    #             img = img.crop((left, top, right, bottom))

    #             # Resize to a standard size
    #             img = img.resize((500, 500))

    #             # New WebP path
    #             webp_path = os.path.splitext(img_path)[0] + '.webp'

    #             # Save as WebP
    #             img.save(webp_path, 'WEBP', quality=85)

    #             # Update the model's image field
    #             self.cin.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)

    #             # Delete old image if not webp
    #             if not img_path.endswith('.webp'):
    #                 os.remove(img_path)

    #             super().save(update_fields=['cin'])  # Save with updated path

    #     if self.driver_licence:
    #         img_path = self.driver_licence.path
    #         img = Image.open(img_path)

    #         # Make the image square by cropping the center
    #         width, height = img.size
    #         min_dim = min(width, height)
    #         left = (width - min_dim) / 2
    #         top = (height - min_dim) / 2
    #         right = (width + min_dim) / 2
    #         bottom = (height + min_dim) / 2
    #         img = img.crop((left, top, right, bottom))

    #         # Resize to a standard size
    #         img = img.resize((500, 500))

    #         # New WebP path
    #         webp_path = os.path.splitext(img_path)[0] + '.webp'

    #         # Save as WebP
    #         img.save(webp_path, 'WEBP', quality=85)

    #         # Update the model's image field
    #         self.cin.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)

    #         # Delete old image if not webp
    #         if not img_path.endswith('.webp'):
    #             os.remove(img_path)

    #         super().save(update_fields=['driver_licence'])  # Save with updated path

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField(editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    # status = models.CharField(max_length=10, editable=False)    
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

    def calculate(self):
        delta = self.end_date - self.start_date
        return delta.days

    def save(self, *args, **kwargs):
        if not self.price_per_day:
            self.price_per_day = self.car.price_per_day

        self.days = self.calculate()
        self.total_price = self.price_per_day * self.days
        self.car.status = "Rented"
        self.car.save()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} - {self.car} from {self.start_date} to {self.end_date}"
        


