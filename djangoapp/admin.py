from django.contrib import admin
from .models import CarMake, CarModel


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "founded_year")
    search_fields = ("name", "country")


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "year", "car_type", "dealer_id", "is_available")
    list_filter = ("car_make", "car_type", "year", "is_available")
    search_fields = ("name", "car_make__name")
