from django.db import models

# Create your models here.


class Favorite(models.Model):
    item_id = models.BigIntegerField()
    user = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE)
