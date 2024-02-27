from django.contrib import admin
from .models import Room, Messages, Topic
from django.contrib.auth import get_user_model


admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Topic)
admin.site.register(get_user_model())
