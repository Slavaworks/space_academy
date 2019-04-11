from django.contrib import admin

from .models import Candidates, Jedies, Planets, Quests, Questions

admin.site.register(Planets)
admin.site.register(Quests)
admin.site.register(Questions)
admin.site.register(Jedies)
admin.site.register(Candidates)
