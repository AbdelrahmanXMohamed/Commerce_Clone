from django.contrib import admin
from  .models import Auctions,User,Category,Watchlist
# Register your models here.
admin.site.register(Auctions)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Watchlist)