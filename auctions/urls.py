from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:unique_id>/history/', views.AuctionHistoryView.as_view(), name='auction-history'),
    path('<uuid:unique_id>/buy-it-now/', views.BuyItNowView.as_view(), name='buy-it-now'),
    path('<uuid:unique_id>/make-offer/', views.MakeOfferView.as_view(), name='make-offer'),
]
