from django.contrib import admin

from .models import Auction
from lots.models import Lot


class LotInline(admin.StackedInline):
    model = Lot


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]
