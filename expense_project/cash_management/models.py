from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    
    
class InfoModel(models.Model):
    GENDER_TYPE = [
        ('male','male'),
        ('female','female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_info')
    name = models.CharField(null=True,max_length=100)
    email = models.EmailField(null=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    profile_image = models.ImageField(
        upload_to='profile_image/',
        blank=True,
        null=True,
        max_length=50
    )
    gender = models.CharField(null=True,blank=True, choices=GENDER_TYPE,max_length=100)
    def __str__(self):
        return f'{self.name}'

###If you created a custom user model using AbstractUser, you should NOT import User like this: from django.contrib.auth.models import User##


class AddCash(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    source = models.CharField(max_length=100,null=True)
    datetime = models.DateTimeField(auto_now=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} - {self.source}'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    datetime = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
    

""" Simple rule:
Many-to-one ➜ ForeignKey
One-to-one ➜ OneToOneField
Many-to-many ➜ ManyToManyField

Why ForeignKey is used for many-to-one :

Because each record belongs to one parent, but the parent can 
have many children. in Django (and in database design in general),
“one-to-many” and “many-to-one” are the same relationship, 
just viewed from opposite directions."""