from django.urls import path

from . import views

urlpatterns = [
    path('lots/', views.LotListView.as_view(), name='lots'),
]
