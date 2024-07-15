from django.urls import path
from .apis import seeExperimentApi,chooseExperimentApi

urlpatterns = [
    path('seeExp/', seeExperimentApi.as_view(),name="seeExperiment"),
    path('chooseExp/', chooseExperimentApi.as_view(),name='chooseExperiment')
]

