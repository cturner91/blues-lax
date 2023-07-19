from django.contrib import admin
from .models import GalleryPhoto, Player, Article, MatchPoints, Fixture, Committee
from django.utils.html import format_html


class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'preview','type','last_updated')
  list_filter = ('type','date', 'last_updated')

class PlayerAdmin(admin.ModelAdmin):
  list_display = ('name','show')
  list_filter = ('type',)


class MatchPointsAdmin(admin.ModelAdmin):
  list_display = ('player','match')
  list_filter = ('match','match__date','player')

class FixtureAdmin(admin.ModelAdmin):
  list_display = ('date','opposition','competition', 'type')
  list_filter = ('date','opposition','competition', 'type')

class GalleryPhotoAdmin(admin.ModelAdmin):
  list_display = ('caption','show', 'order','image_tag')
  list_filter = ('datetime_created','show')

  def image_tag(self,obj):
    return format_html(f'<img src="{obj.image.url}" style="width: 80px; height:80px;" />')



admin.site.register(Player, PlayerAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(MatchPoints, MatchPointsAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(GalleryPhoto, GalleryPhotoAdmin)
admin.site.register(Committee)
