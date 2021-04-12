from django.db import models

# Create your models here.
class Product(models.Model):
    album_name = models.CharField(max_length=200, blank=False)
    artist_name = models.CharField(max_length=200, blank=False)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return(self.album_name)

