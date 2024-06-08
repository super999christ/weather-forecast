from django.urls import include, path

urlpatterns = [
    path('weather/', include('weather.urls')),
]
