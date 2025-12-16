from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    # optional extras (useful in admin)
    country = models.CharField(max_length=60, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN = "SEDAN"
    SUV = "SUV"
    WAGON = "WAGON"
    COUPE = "COUPE"
    HATCHBACK = "HATCHBACK"
    TRUCK = "TRUCK"
    VAN = "VAN"

    CAR_TYPES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (COUPE, "Coupe"),
        (HATCHBACK, "Hatchback"),
        (TRUCK, "Truck"),
        (VAN, "Van"),
    ]

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models",
    )

    dealer_id = models.IntegerField()  # matches Cloudant dealership id
    name = models.CharField(max_length=120)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    year = models.IntegerField()

    # optional extras
    msrp = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
