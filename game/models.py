from django.db import models
from django.urls import reverse

# Create your models here.
class GameCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):

    name = models.CharField(max_length=100)
    createTime = models.DateTimeField(auto_now_add=True)
    excrept = models.TextField(max_length=300)
    times = models.PositiveIntegerField(default=0)
    icon = models.ImageField()
    version = models.CharField(max_length = 30)
    game = models.FileField(default="")
    inTro = models.TextField(blank=True)
    foreImg = models.ImageField()

    category = models.ForeignKey(GameCategory)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game:gameInfo', kwargs={'pk': self.pk})

    def increase_times(self):
        self.times += 1
        self.save(update_fields=['times'])

