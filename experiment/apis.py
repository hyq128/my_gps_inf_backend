from .models import experiment
from .serializers import seeExperimentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from account.models import CustomUser

class seeExperimentApi(APIView):
    def get(self,request):
        now = datetime.now()
        # 筛选end_time在当前时间之前的实验记录
        exp_list = experiment.objects.filter(end_time__gt=now)
        serializer = seeExperimentSerializer(exp_list, many=True)
        return Response(serializer.data)

class chooseExperimentApi(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        if request.data.get('exp_name')==None:
            return Response("请选择一个实验")
        exp_name=request.data.get('exp_name')
        exp_id=experiment.objects.get(exp_name=exp_name).exp_id
        participants=experiment.objects.get(exp_name=exp_name).participants_name+request.user.username+";"
        experiment.objects.filter(exp_id=exp_id).update(participants_name=participants)
        CustomUser.objects.filter(username=request.user.username).update(exp_id=exp_id,exp_name=exp_name,exp_state="active")
        return Response("您的实验已成功保存",{"exp_id":exp_id,"exp_name":exp_name})

class exitExperimentApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # 获取当前用户信息
        user = request.user
        if not user.exp_id:
            return Response("您当前没有参与任何实验")

        try:
            # 获取用户当前参与的实验信息
            exp = experiment.objects.get(exp_id=user.exp_id)
        except experiment.DoesNotExist:
            return Response("实验不存在")

        participants = exp.participants_name.split(";")

        # 移除当前用户
        if user.username in participants:
            participants.remove(user.username)
            exp.participants_name = ";".join(participants)
            exp.save()
            CustomUser.objects.filter(username=user.username).update(exp_id=-1, exp_name="", exp_state="inactive")
            return Response("您已成功退出实验")
        else:
            return Response("您未参与该实验或已经退出")