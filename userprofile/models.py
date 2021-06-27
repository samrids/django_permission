import os
import datetime
from django.db import models
from django.contrib.auth.models import User

def get_avatar_full_path(instance, filename): 
    ext = filename.split('.')[-1]
    filename = '{0}.{1}'.format(instance.pk, ext)    
    return os.path.join("avatars", str(instance.pk), filename) 

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class Province(models.Model):
    province_code = models.SmallIntegerField(null=False)
    province_name = models.CharField(max_length=150,null=False,blank=False)

class Amphur(models.Model):
    amphur_code = models.SmallIntegerField(null=False) 
    amphur_name = models.CharField(max_length=150,null=False,blank=False)    
    province_code = models.SmallIntegerField(null=False)
    province = models.ForeignKey(to=Province,null=False,blank=False,on_delete=models.CASCADE, default=1)



class Address(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    phone= models.CharField(max_length=15, null=False, blank=False)
    
     
    addr_detail = models.CharField(max_length=250, null=False, blank=False)

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)    
class Profile(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    adult         = models.BooleanField(default=False)

    bio_text      = models.CharField(max_length=120, null=True, blank=True)
    status_text   = models.CharField(max_length=120, null=True, blank=True)

    avatar        = models.ImageField(upload_to=get_avatar_full_path, null=True, blank=True, default='avatars/default_avatar.png')

    gender        = models.CharField(max_length=1, choices=GENDER_CHOICES,null=False,blank=False,default='M')
    mobile        = models.CharField(max_length=15,null=True,blank=True)

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    @property
    def age(self):
        today = datetime.date.today()
        if self.date_of_birth is None:
            return 0
        rest = 1 if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day) else 0
        return today.year - self.date_of_birth.year - rest

    def is_adult(self):        
        if (datetime.date.today() - self.date_of_birth) > datetime.timedelta(days=18*365):
            self.adult = True

    def save(self, *args, **kwargs):
        if not self.date_of_birth is None:
            self.is_adult()

        super(Profile, self).save(*args, **kwargs)