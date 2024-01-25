from django.contrib import admin

from .models import Bid, Category, Comment, Listing, User

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
