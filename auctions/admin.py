from django.contrib import admin

from .models import Auction
from lots.models import Lot


class LotInline(admin.StackedInline):
    model = Lot
    extra = 0

    # def has_add_permission(self, request, obj=None):
    #     return False


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    inlines = [LotInline]
    pass
