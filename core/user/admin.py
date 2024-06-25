from django.contrib import admin
from user.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Publisher)
admin.site.register(Commenter)