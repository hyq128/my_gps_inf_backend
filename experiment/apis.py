from .models import experiment
from .serializers import seeExperimentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from account.models import CustomUser

class seeExperimentApi(APIView):
    permission_classes=[]
    def get(self,request):
        now = datetime.now()
        # 筛选end_time在当前时间之前的实验记录
        exp_list = experiment.objects.filter(end_time__gt=now)
        serializer = seeExperimentSerializer(exp_list, many=True)
        return Response(serializer.data)

class chooseExperimentApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if request.data.get('exp_name') is None:
            return Response("Please select an experiment")
        
        new_exp_name = request.data.get('exp_name')
        new_experiment = experiment.objects.get(exp_name=new_exp_name)
        new_exp_id = new_experiment.exp_id

        # 找到用户当前参与的实验
        try:
            current_exp = experiment.objects.get(exp_id=user.exp_id)
            # 从当前实验的 participants_name 字段中删除用户名
            participants = current_exp.participants_name.split(';')
            participants = [p for p in participants if p and p != user.username]
            current_exp.participants_name = ';'.join(participants) + ';'
            current_exp.save()
        except experiment.DoesNotExist:
            pass

        # 更新新实验的 participants_name 字段
        new_participants = new_experiment.participants_name + user.username + ";"
        experiment.objects.filter(exp_id=new_exp_id).update(participants_name=new_participants)

        # 更新用户信息
        CustomUser.objects.filter(username=user.username).update(exp_id=new_exp_id, exp_name=new_exp_name, exp_state="active")
        return Response(f"Your choice {new_exp_name} has been successfully saved !")

class myExperimentApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        username=request.user.username
        if CustomUser.objects.get(username=username).exp_id==-1:
            return Response("You are not currently participating in any experiments")
        else:
            Serializer = seeExperimentSerializer(experiment.objects.get(exp_id=CustomUser.objects.get(username=username).exp_id))
            return Response([Serializer.data])
        

class exitExperimentApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # 获取当前用户信息
        user = request.user
        if not user.exp_id:
            return Response("You are not currently participating in any experiments")

        try:
            # 获取用户当前参与的实验信息
            exp = experiment.objects.get(exp_id=user.exp_id)
        except experiment.DoesNotExist:
            return Response("The experiment does not exist")

        participants = exp.participants_name.split(";")

        # 移除当前用户
        if user.username in participants:
            participants.remove(user.username)
            exp.participants_name = ";".join(participants)
            exp.save()
            CustomUser.objects.filter(username=user.username).update(exp_id=-1, exp_name="", exp_state="inactive")
            return Response("You have successfully exited the experiment")
        else:
            return Response("You are not participating in the experiment or have quit")