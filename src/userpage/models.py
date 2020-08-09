from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.
gender = (
    ('n','Not Specified'),
    ('m','Male'),
    ('f','Female'),
    ('o','Other')
)
class User_detail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=gender, default="Not Specified")
    phone = models.CharField(max_length=20)
    dob = models.DateField(auto_now_add=True)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile', blank=True)
    bio = models.TextField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.email
    
    def get_profile_page(self):
        return f"/profile/{self.slug}"
    

def get_profile_pic(self):
    obj=User_detail.objects.get(user=self)
    # print(obj)
    return obj.profile_picture.url

def get_user_profile(self):
    obj=User_detail.objects.get(user=self)
    # print(obj)
    return obj.get_profile_page()

User.add_to_class('get_profile_pic',get_profile_pic)
User.add_to_class('get_user_profile',get_user_profile)
    
def create_slug(instance,new_slug=None):
    slug = slugify(instance.user.username)
    return slug

def pre_save_post_reciever(sender,instance,created,*args,**kwargs):
    if created:
        obj=User_detail.objects.create(user=instance)
    print("Pre saves")
    if not obj.slug:
        obj.slug = create_slug(instance)

# post_save.connect(pre_save_post_reciever,sender=User)