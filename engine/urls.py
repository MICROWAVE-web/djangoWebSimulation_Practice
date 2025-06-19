# api/urls.py
from django.urls import path
from .views import CellListView, StepSimulationView, ResetSimulationView, change_value, get_param

urlpatterns = [
    path('cells/', CellListView.as_view()),
    path('step/', StepSimulationView.as_view()),
    path('reset/', ResetSimulationView.as_view()),
    path('change/<str:param>/<int:val>/', change_value),
    path('get_param/<str:param>/', get_param)
]
