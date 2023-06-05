from django.db import models
from users.models import CustomUser
import requests


class PetBreeds:
    API_URL = 'https://api.thedogapi.com/v1/breeds'

    @classmethod
    def get_pet_breeds(cls):
        if not hasattr(cls, 'breeds'):
            cls.breeds = cls.fetch_pet_breeds()
        return cls.breeds

    @classmethod
    def fetch_pet_breeds(cls):
        response = requests.get(cls.API_URL)
        if response.status_code == 200:
            data = response.json()
            breeds = [breed['name'] for breed in data]
            return breeds
        return []


class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    BREED_CHOICES = PetBreeds.get_pet_breeds()
    breed = models.CharField(max_length=150, choices=[
                             (breed, breed) for breed in BREED_CHOICES])
    age = models.IntegerField()

    def __str__(self):
        return self.name
