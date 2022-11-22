from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Info(models.Model):
    name = models.CharField('info name', max_length=120)
    publisher_name = models.CharField('publisher name', blank=True, null=True, max_length=60)
    publisher = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    info = models.TextField(max_length=10000)
    sumRev = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=2)

    def __str__(self):
        return self.name


class Pages(models.Model):
    page_name = models.CharField('page name', max_length=30)
    page_image = models.ImageField(null=True, blank=True, upload_to="images/")
    auth_users = models.ManyToManyField(User, blank=True)
    web = models.URLField('website page', blank=True, null=True)

    def __str__(self):
        return self.page_name


RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class InfoReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.CharField(choices=RATING, max_length=150)
