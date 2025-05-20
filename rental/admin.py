from django.contrib import admin
from .models import Car, Client, Rental, CarModel, Brand
    


# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "brand")

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "model_name")

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "model", "year", "plate_number", "status", "price_per_day", "image", "created_at")
    list_filter = ("status",)
    search_fields = ("brand", "model")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "cin", "driver_licence", "created_at")

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "client", "start_date", "end_date", "days", "price_per_day", "total_price", "created_at")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "car":
            kwargs["queryset"] = Car.objects.filter(status="Available")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

