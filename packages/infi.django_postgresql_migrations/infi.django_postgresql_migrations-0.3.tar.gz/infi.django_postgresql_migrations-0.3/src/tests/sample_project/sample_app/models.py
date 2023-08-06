from django.db import models

class SampleModel(models.Model):

    int_field = models.IntegerField()
    char_field = models.CharField(max_length=100)
    text_field = models.TextField()

