from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200,null=True)
    message=models.TextField()
    likes=models.ManyToManyField(User,default=0,related_name="post_likes")
    # count=models.IntegerField()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail',args=(str(self.id)))
