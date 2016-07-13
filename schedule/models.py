from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField()

    def __str__(self):
        return self.name
