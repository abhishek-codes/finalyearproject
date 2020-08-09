from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from userpage.models import User_detail

# Create your models here.
class CommentManager(models.Manager):
    def fiter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id 
        comments = super(CommentManager,self).filter(content_type=content_type,object_id=object_id).filter(parent=None)
        return comments

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    content_type  = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def children(self):
        child_qs = Comment.objects.filter(parent=self)
        return child_qs

    def get_profile_page(self):
        obj=User_detail.objects.get(user=self.user)
        return obj.get_profile_page()
    
    def get_profile_picture(self):
        obj=User_detail.objects.get(user=self.user)
        return obj.profile_picture.url


    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_delete_url(self):
        return f"/comments/{self.pk}/delete"

    
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type