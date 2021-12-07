import pytest
from django import urls
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone

from ..models import Auction, AuctionStatusChoice, AuctionTypeChoice


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='test_user',
        password='test'
    )


@pytest.fixture
def user_token(user):
    client = Client()
    response = client.post(
        urls.reverse('jwt_token'),
        {
            'username': user.username,
            'password': 'test'
        }
    )
    return response.data['access']


@pytest.fixture
def auth_client(user_token):
    return Client(HTTP_AUTHORIZATION=f'Bearer {user_token}')


@pytest.fixture
def english_auction(db):
    return Auction.objects.create(
        status=AuctionStatusChoice.IN_PROGRESS.value,
        type=AuctionTypeChoice.ENGLISH.value,
        start_price=100,
        current_price=100,
        step=50,
        opening_date=timezone.now(),
        closing_date=timezone.now() + timezone.timedelta(minutes=8),
        buy_now_price=10000,
    )


@pytest.mark.django_db
def test_buy_it_now(auth_client, english_auction):
    response = auth_client.post(
        urls.reverse('buy_it_now', args=[english_auction.unique_id])
    )
    assert response.status_code == 200
    assert Auction.objects.get(pk=english_auction.unique_id).current_price == english_auction.buy_now_price


@pytest.mark.django_db
def test_correct_make_offer(auth_client, english_auction):
    response = auth_client.post(
        urls.reverse('make_offer', args=[english_auction.unique_id]),
        data={
            'raise_price': english_auction.step
        }
    )
    updated_auction = Auction.objects.get(pk=english_auction.unique_id)
    assert response.status_code == 200
    assert updated_auction.current_price != english_auction.current_price
    assert updated_auction.current_price == english_auction.current_price + english_auction.step
