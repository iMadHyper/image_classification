from django.urls import re_path, path
from . import views, views_api


app_name = 'main'
urlpatterns = [
    re_path(r'^$', views.main, name='main'),
    path('api/predict', views_api.PredictAPI.as_view(), name='predict_api'),
]