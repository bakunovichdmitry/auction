from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:unique_id>/buy-it-now/', views.BuyItNowView.as_view(), name='buy-now'),
    path('<uuid:unique_id>/make-offer/<int:raise_price>', views.MakeOfferView.as_view()),

]
