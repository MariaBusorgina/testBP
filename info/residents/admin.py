from django.contrib import admin

from .models import House, Resident, Apartment, Car, ParkingSpace, Ownership


class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'house_number')


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'passport_data')


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'house')


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'state_number', 'brand', 'resident')


class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'house', 'reserved_for')


class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'resident', 'percentage_ownership')


admin.site.register(House, HouseAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(ParkingSpace, ParkingSpaceAdmin)
admin.site.register(Ownership, OwnershipAdmin)

