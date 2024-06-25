from django.db import models
from user.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class BasePost(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()

    class Meta:
        abstract = True

class Post(BasePost):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to="posts/images",null=True,blank=True)
    title = models.CharField(max_length=150,null=True,blank=True)
    # this will keep track of the emogi icons of a post in a thread
    like = models.PositiveIntegerField(null=True,blank=True)
    ok = models.PositiveIntegerField(null=True,blank=True) 
    loved = models.PositiveIntegerField(null=True,blank=True) 
    dislike = models.PositiveIntegerField(null=True,blank=True) 
    angry = models.PositiveIntegerField(null=True,blank=True) 
    def __str__(self) -> str:
        return f"{self.title}"
    


class Comment(BasePost):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    like = models.PositiveIntegerField(null=True,blank=True)
    dislike = models.PositiveIntegerField(null=True,blank=True)
    upvote = models.PositiveIntegerField(null=True,blank=True)
    sub_comments = models.ForeignKey("self",on_delete=models.CASCADE, related_name='sub_comment',null=True,blank=True)

    def __str__(self) -> str:
        return f"comment on {self.post} {self.body}"


class Thread(models.Model):
    sub_url = models.SlugField()
    post = models.ForeignKey(Post, related_name="thread",on_delete=models.CASCADE)

    @property
    def base_url(self):
        return f"{self.post.created_by.website_url}"
    
    @property
    def complete_url(self):
        return f"{self.base_url}{self.sub_url}"
    
    def clean(self):
        super().clean()
        if Thread.objects.filter(sub_url=self.sub_url, post__created_by__website_url=self.post.created_by.website_url).exists():
            raise ValidationError('there already a thread on this register site please provide a unique slug for the data integerity purpose so u do lose the existing data for your site ! .')
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Thread on {self.complete_url}"