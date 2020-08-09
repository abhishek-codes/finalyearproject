from django.db import models

# Create your models here.
class Feedback(models.Model):
    exp=[
        ('bad','Bad'),
        ('bverage','Average'),
        ('good','Good'),
        ('excellent','Excellent'),
    ]
    rec=[
        ('very_likely','Very Likely'),
        ('likely','Likely'),
        ('not_recommend','Not Recommend'),
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField()
    experience = models.CharField(max_length=20,choices=exp)
    recommened = models.CharField(max_length=20,choices=rec)
    msg = models.TextField(max_length=400)