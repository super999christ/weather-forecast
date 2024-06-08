from django.urls import path

from . import views

urlpatterns = [
    path('<str:operation_name>/template/<int:forecast_date>/<int:forecast_hour>/',
         views.ForecastDetail.as_view(), name='forecast_detail'),
]
