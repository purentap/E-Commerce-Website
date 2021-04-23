from django.db import models

# Create your models here.


class Product(models.Model):
    model_no = models.CharField(max_length=200, blank=True, null=True)
    album_name = models.CharField(max_length=200, blank=True, null=True)
    artist_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)
    warrantry = models.CharField(max_length=200, blank=True, null=True)
    distributor = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=200, blank=True, null=True)
    stock = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('product-detail-view', args[str(self.id)])

    def __str__(self):
        return(self.album_name)
