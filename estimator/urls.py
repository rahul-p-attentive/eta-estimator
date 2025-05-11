from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstimatorViewSet, JobViewSet, TradeViewSet, ResourceGroupViewSet

router = DefaultRouter()
router.register(r'estimators', EstimatorViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'resource_groups', ResourceGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 