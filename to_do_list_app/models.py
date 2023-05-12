from django.db import models

# Create your models here.
class To_do_list(models.Model):
    name = models.CharField(max_length=256, null=False)

    def __str__(self):
        return f"{self.name}"