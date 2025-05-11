from django.contrib import admin
from .models import Estimator, Job, Trade, ResourceGroup

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'estimator', 'status', 'created_at')
    search_fields = ('id', 'title', 'estimator', 'estimator__email', 'estimator__name')

@admin.register(Estimator)
class EstimatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('id', 'name', 'email')

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(ResourceGroup)
class ResourceGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number_of_resources', 'created_at')
    search_fields = ('id', 'name')
