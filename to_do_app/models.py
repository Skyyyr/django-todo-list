from django.db import models
from to_do_list_app.models import To_do_list
from django.utils.timezone import datetime

# Create your models here.
class To_do(models.Model):
    name = models.CharField(max_length=256, null=False)
    created_at = models.TimeField(default=datetime.time(datetime.now()), null=False)
    completed_at = models.TimeField(null=True, blank=True)
    to_do_list = models.ForeignKey(To_do_list, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"