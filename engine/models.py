from django.db import models


class PlantSpecies(models.Model):
    name = models.CharField(max_length=100)
    growth_rate = models.FloatField(default=1.0)  # как быстро растет
    aggression = models.FloatField(default=1.0)  # сколько ресурсов "высасывает"
    light_preference = models.CharField(
        max_length=10,
        choices=[('sun', 'Sun'), ('shade', 'Shade'), ('partial', 'Partial')],
        default='partial'
    )
    shape = models.CharField(max_length=20, default='circle')  # пока только circle
    max_radius = models.FloatField(default=1.0)
    max_height = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class PlantInstance(models.Model):
    species = models.ForeignKey(PlantSpecies, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    radius = models.FloatField(default=0.1)
    height = models.FloatField(default=0.1)
    health = models.FloatField(default=1.0)  # от 0 до 1

    def __str__(self):
        return f"{self.species.name} at ({self.x}, {self.y})"


