from django.urls import path

from . import views

urlpatterns = [
    path('', views.LotListView.as_view(), name='lots'),
    path('<uuid:unique_id>/', views.LotDetailView.as_view(), name='lot_detail'),
]
