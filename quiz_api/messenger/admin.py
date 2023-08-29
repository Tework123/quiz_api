from django.contrib import admin

from messenger.models import Relationship, Chat, Message, Image

admin.site.register(Relationship)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Image)
