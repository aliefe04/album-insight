from django.contrib import admin
from .models import Album, Review

# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_year', 'genre', 'cover_image') # Changed cover_image_url to cover_image
    list_filter = ('artist', 'genre', 'release_year')
    search_fields = ('title', 'artist', 'genre')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('album', 'reviewer_name', 'rating', 'created_at')

admin.site.register(Album, AlbumAdmin)
admin.site.register(Review, ReviewAdmin)
