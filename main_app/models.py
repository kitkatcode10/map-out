from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

# Create your models here.

STYLE_CHOICES = (
    ('L', 'Luxury'),
    ('F', 'Family'),
    ('E', 'Expedition'),
    ('C', 'Cheap')
)

TRANSPORATION_CHOICES = (
    ('C', 'Car'),
    ('A', 'Airplane'),
    ('T', 'Train'),
    ('B', 'Bike'),
    ('S', 'Ship')
)

CATEGORY_CHOICES = (
  ('O', 'Other'),
  ('B', 'Bottoms'),
  ('T', 'Tops'),
  ('F', 'Footwear'),
  ('A', 'Accessories'),
  ('G', 'Gear'), 
)

class Packing(models.Model):
  category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0] )
  item = models.CharField(max_length=50)
  brand = models.CharField(max_length=50)
  colour = models.CharField(max_length=20)
  
  class Meta:
    ordering = ['category']

  def __str__(self):
    return self.item
  
  def get_absolute_url(self):
    return reverse('packing_index', kwargs={'pk': self.id})

  
class Vacation(models.Model):
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date = models.DateField('travel date')
    duration = models.IntegerField()
    style = models.CharField(max_length=1, choices=STYLE_CHOICES, default=STYLE_CHOICES[0][0])
    travellers = models.IntegerField()
    transportation = models.CharField(max_length=1, choices=TRANSPORATION_CHOICES, default=TRANSPORATION_CHOICES[0][0])
    packing = models.ManyToManyField(Packing)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'vacation_id': self.id})

class Itinerary(models.Model):
  date = models.DateField('Itinerary date')
  activity = models.TextField(max_length=250)
  location = models.CharField(max_length=100)
  vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.activity} on {self.date}"

  class Meta:
    ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for vacation_id: {self.vacation_id} @{self.url}"

