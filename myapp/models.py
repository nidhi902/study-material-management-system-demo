from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Studymaterial(models.Model):
    materialtype=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    batch=models.CharField(max_length=100)
    course=models.CharField(max_length=100, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    file=models.FileField(upload_to='uploads/')
    text=models.TextField(max_length=2000, null=True, blank=True)
    uploaded_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.materialtype}  -{self.course} - UPLOADED BY {self.uploaded_by} - ON {self.uploaded_at.strftime('%y-%m-%d %H:%M:%S')}" 
    
    
class profile(models.Model):
    ROLE_CHOICES=(
        ('student','Student'),
        ('teacher','Teacher'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=50,blank=True,null=True)
    accessbox=models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"
        