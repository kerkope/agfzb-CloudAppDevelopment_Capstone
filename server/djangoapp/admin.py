from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 10

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name',  'id', 'c_type', 'year', 'make']
    search_fields = ['name']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    search_fields = ['name']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)