from django.db import models
from django.db.models import Avg # Import Avg

# Create your models here.

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    cover_image = models.FileField(upload_to='album_covers/', blank=True, null=True) # New field for file uploads

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title

class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField() # Assuming a numerical rating, e.g., 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.album.title} by {self.reviewer_name}'
