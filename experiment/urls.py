from django.urls import path
from .apis import seeExperimentApi,chooseExperimentApi,exitExperimentApi,myExperimentApi,seeExperimentHistoryApi

urlpatterns = [
    path('seeExp/', seeExperimentApi.as_view(),name="seeExperiment"),
    path('chooseExp/', chooseExperimentApi.as_view(),name='chooseExperiment'),
    path('exitExp/', exitExperimentApi.as_view(),name='exitExperiment'),
    path('myExp/', myExperimentApi.as_view(),name='myExperiment'),
    path('seeExpHistory/', seeExperimentHistoryApi.as_view(),name='seeExperimentHistory'),
]

