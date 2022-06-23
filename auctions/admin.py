from django.contrib import admin
from . import models

@admin.register(models.Auction)
class adminAuction(admin.ModelAdmin):
    list_display = ['id','user', 'title','price', 'create_date','category', 'closed']
    search_fields = ['id','user__username', 'title','price', 'create_date','category', 'closed']
    ordering = ['create_date']
    
@admin.register(models.User)
class adminUser(admin.ModelAdmin):
    list_display = ['username', 'date_joined']
    search_fields = ['username', 'date_joined']

@admin.register(models.Comments)
class adminComment(admin.ModelAdmin):
    list_display = ['comment', 'userComment', 'auction']
    search_fields = ['comment', 'userComment__username', 'auction__id']
    ordering = ['auction']

@admin.register(models.Bids)
class adminComment(admin.ModelAdmin):
    list_display = ['bid_price', 'user', 'auction']
    search_fields = ['bid_price', 'user__username', 'auction__id']
    ordering = ['auction']




