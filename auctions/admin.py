from django.contrib import admin

from .models import EnglishAuction, DutchAuction


@admin.register(EnglishAuction)
class EnglishAuctionAdmin(admin.ModelAdmin):
    pass


@admin.register(DutchAuction)
class DutchAuctionAdmin(admin.ModelAdmin):
    pass
