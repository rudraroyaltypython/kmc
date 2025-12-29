from django.urls import path
from .views import analysis_list, probability_table

app_name = 'analyzer'

urlpatterns = [
    path('', analysis_list, name='analysis_list'),
    path('probability/', probability_table, name='probability_table'),

]
