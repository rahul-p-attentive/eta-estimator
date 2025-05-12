from rest_framework import serializers
from .models import Estimator, Job, Trade, ResourceGroup

class EstimatorSerializer(serializers.ModelSerializer):
    trade = serializers.PrimaryKeyRelatedField(queryset=Trade.objects.all())

    class Meta:
        model = Estimator
        fields = ['id', 'name', 'email', 'trade']

class JobSerializer(serializers.ModelSerializer):
    trades = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )
    estimator = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'estimated_completion_time', 'status', 'estimator', 'trades', 'created_at', 'updated_at']

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
    user_inputs = serializers.ListField(
        child=TradeEstimationInputSerializer()
    ) 