from rest_framework import serializers
from .models import Estimator, Job, Trade, ResourceGroup

class EstimatorSerializer(serializers.ModelSerializer):
    trade = serializers.PrimaryKeyRelatedField(queryset=Trade.objects.all())

    class Meta:
        model = Estimator
        fields = ['id', 'name', 'email', 'trade']

class JobSerializer(serializers.ModelSerializer):
    estimator = serializers.PrimaryKeyRelatedField(queryset=Estimator.objects.all())

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'estimated_completion_time', 'status', 'estimator', 'created_at', 'updated_at']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id','name']

class ResourceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceGroup
        fields = ['id', 'name', 'number_of_resources', 'created_at', 'updated_at']

class TradeEstimationInputSerializer(serializers.Serializer):
    is_workable = serializers.BooleanField()
    trades = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

class EstimateTimeInputSerializer(serializers.Serializer):
    trade_estimations = serializers.ListField(
        child=TradeEstimationInputSerializer()
    ) 