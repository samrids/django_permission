import os
import datetime
from django.db import models

def get_avatar_full_path(instance, filename): 
    ext = filename.split('.')[-1]
    filename = '{0}.{1}'.format(instance.pk, ext)    
    return os.path.join("avatars", str(instance.pk), filename) 

class Snippets(models.Model):
    
    first_name    = models.CharField(max_length=150, null=False, blank=False)
    last_name     = models.CharField(max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    adult         = models.BooleanField(default=False)

    status_text   = models.CharField(max_length=120, null=False, blank=False)
    remark_text   = models.CharField(max_length=120, null=False, blank=False)

    avatar        = models.ImageField(upload_to=get_avatar_full_path, null=True, blank=True, default='avatars/default_avatar.png')

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

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

        super(Snippets, self).save(*args, **kwargs)