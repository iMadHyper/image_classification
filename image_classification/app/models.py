from django.db import models


class ObjectImage(models.Model):
    image = models.ImageField(verbose_name='Фото', upload_to='images/', blank=True, null=True)