from django.db import models
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True, default = None, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    email = models.EmailField()
    logo = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name="postlogo")
    pdf  = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name="postpdf")

    class Meta:
        ordering = ['-created_on']

    class Meta:
        verbose_name = u'Message'
        verbose_name_plural = u'Messages'

    def __str__(self):
        return self.title
