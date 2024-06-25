from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager,UserManager

class Role(models.TextChoices):
    PUBLISHER = 'PUB', 'As Publisher'
    COMMENTER = 'COMT', 'As Commenter'

class PublisherManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Role.PUBLISHER)
    
    def create(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.PUBLISHER)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create(username, email, password, **extra_fields)
    
    
class CommenterManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        return super().get_queryset(*args, **kwargs).filter(role=Role.COMMENTER)
    
    def create(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

class User(AbstractUser):
    role = models.CharField(max_length=4, choices=Role.choices, default=Role.PUBLISHER)
    profile = models.ImageField(upload_to="user-profile/", blank=True, null=True)
    biography = models.CharField(max_length=200, null=True, blank=True)
    website_url = models.URLField(validators=[URLValidator], null=True, blank=True)
    website_name = models.CharField(max_length=50,null=True,blank=True)

    REQUIRED_FIELDS = ["email",]

    publisher = PublisherManager()
    commentor = CommenterManager()
    objects = UserManager()

    
    class Meta:
        abstract = False

    def __str__(self) -> str:
        return f"{self.username}"


class Publisher(User):
    base_role = Role.PUBLISHER

    REQUIRED_FIELDS = ["website_url","email"]

    class Meta:
        verbose_name_plural = "Publisher User"
        proxy = True

    objects = PublisherManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.website_url:
                raise ValidationError("Website URL is required.")
            self.role = self.base_role
        super().save(*args, **kwargs)


class Commenter(User):
    base_role = Role.COMMENTER

    class Meta:
        verbose_name_plural = "Commentor User"
        proxy = True

    objects = CommenterManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)


class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "followers"
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower} follows {self.user}"

