from django.contrib import admin
from .models import Game, Game_Genre,Milesstones
# Register your models here.


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date','console',)
    search_fields = ('title', 'console','release_date',)
admin.site.register(Game,GameAdmin)

class GENRESAdmin(admin.ModelAdmin):
    list_display = ('genre',)
admin.site.register(Game_Genre, GENRESAdmin)

class MILESTONES(admin.ModelAdmin):
    list_display = ('milestone', 'discount')
admin.site.register(Milesstones,MILESTONES)

