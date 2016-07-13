from django.db import models

from location_field.models.plain import PlainLocationField

from accounts.models import User


class Place(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    telephone = models.CharField(max_length=32, blank=True)
    x = models.FloatField()
    y = models.FloatField()
    location = PlainLocationField(zoom=16, blank=True)
    rate_avg = models.FloatField(default=0.0)

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        if len(self.location) < 1:  # if new objects
            self.location = "{},{}".format(str(self.y), str(self.x))
        locations = self.location.split(",")
        if locations != [float(self.y), float(self.x)]:
            self.y = locations[0]
            self.x = locations[1]
        super(Place, self).save(*args, **kwargs)


class Review(models.Model):
    place = models.ForeignKey(Place, related_name='reviews')
    user = models.ForeignKey(User, related_name='recently_visit')
    rate = models.FloatField(default=0.0)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return "{}: {}".format(self.place.name, self.comment[:10])


class Image(models.Model):
    image = models.ImageField()
    review = models.ForeignKey(Review, related_name='images')

    def __str__(self):
        return "{}'s image".format(self.review.place.name)
