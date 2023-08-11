from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,editable=True,default=uuid.uuid4())
    created_at=models.DateField(auto_now=True)

    class Meta:
        abstract=True

class Student(BaseModel):
    name=models.CharField(max_length=100)
    school=models.TextField()
    age=models.IntegerField()