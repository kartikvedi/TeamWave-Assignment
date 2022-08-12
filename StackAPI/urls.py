from django.urls import path
from . import views

urlpatterns=[path('Index',views.index,name='Index'),
             path('Show',views.Show,name='Show')]
