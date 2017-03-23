# from __future__ import unicode_literals

from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User



# Data model 
class Entry(models.Model):    

    picture = models.ImageField(upload_to="images", default="images/default.jpg")
    # content_type = models.CharField(max_length=50, blank = True)    
    first_name = models.CharField(max_length = 20, blank = True)
    last_name = models.CharField(max_length = 20, blank = True)
    age = models.CharField(max_length = 3 , blank= True)
    bio = models.CharField(max_length = 430 , blank=True)
    created_by = models.OneToOneField(User, related_name="entry_creators")
    creation_time = models.DateTimeField()
    update_time   = models.DateTimeField(blank = True)
    followers = models.ManyToManyField(User, blank = True)


    def __unicode__(self):
        return 'id=' + str(self.id) + 'last_name' + str(self.last_name)

class Comments(models.Model):
    user = models.ForeignKey(User,default = None)
    comment = models.CharField(max_length = 160)
    # picture = models.ImageField(upload_to="images",blank = True)
    timestamp = models.DateTimeField(auto_now = True)
    postid = models.CharField(max_length = 10000)
    
    def __unicode__(self):
        return 'id = ' + str(self.id) + 'comment' + str(self.comment)

class Posts(models.Model):
    user = models.ForeignKey(User,default = None)
    text = models.CharField(max_length = 160)
    timestamp = models.DateTimeField(auto_now = True)
    entry = models.ForeignKey(Entry,blank = True)
    comments = models.ManyToManyField(Comments,blank = True , related_name = "comments", null = True)

    def __unicode__(self):
        return 'id = ' + str(self.id) + 'post=' + str(self.text)
