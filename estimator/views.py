from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Estimator, Job, Trade, ResourceGroup, get_estimator_with_earliest_completion_time
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        trades = serializer.validated_data.pop('trades')
        base_data = {
            'title': serializer.validated_data['title'],
            'description': serializer.validated_data['description'],
            'status': 'pending'
        }
        
        created_jobs = []
        errors = []
        
        try:
            # Create input for time prediction
            user_input = [{
                "is_workable": True,
                "trades": trades
            }]
            
            # Get time estimates for all trades
            estimated_time_dict = time_predictor.predict_estimated_times(user_input)
            
            # Create a job for each trade
            for trade_name in trades:

                estimator = get_estimator_with_earliest_completion_time(trade_name)
                if not estimator:
                    errors.append(f"No estimator found for trade: {trade_name}")
                    continue
                
                # Get job time for this trade
                job_time = estimated_time_dict.get(trade_name, 0)
                
                wait_time = 0
                if hasattr(estimator, 'job') and estimator.job and estimator.job.estimated_completion_time:
                    wait_time = (estimator.job.estimated_completion_time - datetime.now()).total_seconds()
                    wait_time = max(0, wait_time)
                
                # Calculate total time and completion time
                total_seconds = job_time + wait_time
                estimated_completion_time = datetime.now() + timedelta(seconds=total_seconds)
                
                # Create the job
                job_data = {
                    **base_data,
                    'title': f"{base_data['title']} - {trade_name}",
                    'estimator': estimator,
                    'estimated_completion_time': estimated_completion_time
                }
                
                job = Job.objects.create(**job_data)
                created_jobs.append(job)
            
            if errors:
                return Response({
                    "errors": errors,
                    "created_jobs": JobSerializer(created_jobs, many=True).data
                }, status=status.HTTP_207_MULTI_STATUS)
            
            return Response(JobSerializer(created_jobs, many=True).data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": f"Error creating jobs: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def estimate_time(self, request):
        serializer = EstimateTimeInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_inputs = serializer.validated_data['user_inputs']
        
        try:
            # Use the ML predictor to estimate time
            estimated_time_dict = time_predictor.predict_estimated_times(user_inputs)

            trade_times_dict = {}
            for trade in estimated_time_dict:
                estimator = get_estimator_with_earliest_completion_time(trade)
                wait_time = 0
                if estimator and hasattr(estimator, 'job') and estimator.job and estimator.job.estimated_completion_time:
                    wait_time = (estimator.job.estimated_completion_time - datetime.now()).total_seconds()
                    wait_time = max(0, wait_time)
                trade_times_dict[trade] = {
                    "job_time": estimated_time_dict[trade],
                    "wait_time": wait_time
                }

            # Calculate overall time as max of job_time + wait_time across all trades
            response_dict = {}
            overall_seconds = max(
                trade_data["job_time"] + trade_data["wait_time"] 
                for trade_data in trade_times_dict.values()
            )
            response_dict["eta"] = datetime.now() + timedelta(seconds=overall_seconds)
            response_dict["eta_in_days"] = round(overall_seconds / 86400, 2)
            response_dict["trade_wise_times"] = trade_times_dict
            
            return Response(response_dict)

        except Exception as e:
            return Response(
                {"error": f"Error estimating time: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class ResourceGroupViewSet(viewsets.ModelViewSet):
    queryset = ResourceGroup.objects.all()
    serializer_class = ResourceGroupSerializer
