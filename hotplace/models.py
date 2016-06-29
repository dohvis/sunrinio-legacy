from django.db import models

from location_field.models.plain import PlainLocationField

from accounts.models import User


class Place(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    location = PlainLocationField(zoom=16)

    @property
    def x(self):
        return self.location.split(',')[1]

    @property
    def y(self):
        return self.location.split(',')[0]

    def __str__(self):
        return "{}".format(self.name)


class Review(models.Model):
    place = models.ForeignKey(Place, related_name='reviews')
    user = models.ForeignKey(User, related_name='recently_visit')
    rate = models.IntegerField(default=5)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return "{}: {}".format(self.place.name, self.comment[:10])


class Image(models.Model):
    image = models.ImageField()
    review = models.ForeignKey(Review, related_name='images')

    def __str__(self):
        return "{}'s image".format(self.review.place.name)
