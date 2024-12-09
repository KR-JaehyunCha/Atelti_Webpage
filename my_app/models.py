from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField()
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
