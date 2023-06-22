from django.db import models
from django.utils import timezone

# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        abstract = True
        db_table = "base_tbl"