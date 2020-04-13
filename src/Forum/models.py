from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

# Create your models here.
class PostQuerySet(models.QuerySet):
    def search(self,query):
        lookup = (
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)|
            Q(user__username__icontains=query)
        )
        return self.filter(lookup)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model,using=self._db)

    def search(self,query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,default=1)
    image = models.ImageField(upload_to='image/',blank=True,null=True)
    title = models.CharField(max_length=120)
    content = models.TextField(null=False)
    slug = models.SlugField(unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_time']

    def get_absolute_url(self):
        return f"/forum/{self.slug}"
    
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.fiter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    # print("####create_slug",slug)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    # print(qs)
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        # print("###new slug",new_slug)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_reciever(sender,instance,*args,**kwargs):
    print("Pre saves")
    if not instance.slug:
        instance.slug = create_slug(instance)
    

pre_save.connect(pre_save_post_reciever,sender=Post)