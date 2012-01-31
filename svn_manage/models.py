from django.db import models

# Create your models here.
class Repos(models.Model):
    repo_name=models.CharField(max_length=100)
    repo_admin=models.CharField(max_length=100)
    repo_manager=models.CharField(max_length=400)
    created_on=models.DateField()
    status=models.IntegerField()

class Managers(models.Model):
    name=models.CharField(max_length=100)

class Deactivated(models.Model):
    repo_name=models.CharField(max_length=100)
    users=models.TextField(null=True)
    groups=models.TextField(null=True)
    deactiveted_on=models.DateField()
    
    
