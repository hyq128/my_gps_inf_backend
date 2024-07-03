from .models import expHistory
from .serializers import expHistorySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class updateExpHistoryApi(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        username=request.user.username
        serializer = expHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_time=serializer.validate.get('start_time')
        end_time=serializer.validate.get('end_time')
        exp_type=serializer.validate.get('exp_type')

        expHistory.objects.create(username=username,start_time=start_time,end_time=end_time,exp_type=exp_type)
        return Response("Success")


class GetExpHistoryApi(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        username=request.user.username
        expHistory_list=expHistory.objects.filter(username=username)
        serializer=expHistorySerializer(expHistory_list,many=True)
        return Response(serializer.data)