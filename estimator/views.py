from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Estimator, Job, Trade, ResourceGroup
from .serializers import EstimatorSerializer, JobSerializer, TradeSerializer, ResourceGroupSerializer, EstimateTimeInputSerializer
from .ml_predictor import time_predictor

# Create your views here.

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

    @action(detail=True, methods=['get'])
    def estimators(self, request, pk=None):
        trade = self.get_object()
        estimators = Estimator.objects.filter(trade=trade)
        serializer = EstimatorSerializer(estimators, many=True)
        return Response(serializer.data)

class EstimatorViewSet(viewsets.ModelViewSet):
    queryset = Estimator.objects.all()
    serializer_class = EstimatorSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        estimator_id = request.data.get('estimator')
        if not Estimator.objects.filter(id=estimator_id).exists():
            return Response({"error": "Estimator not found"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def estimate_time(self, request):
        serializer = EstimateTimeInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_inputs = serializer.validated_data['user_inputs']
        
        try:
            # Use the ML predictor to estimate time
            estimated_time_dict = time_predictor.predict_estimated_times(user_inputs)

            # For each trade get estimator whose assigned jobs will be done first (based on estimated_completion_time)
            for trade in estimated_time_dict:
                estimator = Estimator.objects.filter(trade=trade).jobs.order_by('estimated_completion_time').first()


            return Response({
                "estimated_time": estimated_time,
                "trade_estimations": trade_estimations
            })
            
        except Exception as e:
            return Response(
                {"error": f"Error estimating time: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ResourceGroupViewSet(viewsets.ModelViewSet):
    queryset = ResourceGroup.objects.all()
    serializer_class = ResourceGroupSerializer
