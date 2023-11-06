from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField
from storages.backends.s3boto3 import S3Boto3Storage

from elisasrecipe import settings


class ProfileImage(models.Model):
    image = models.ImageField(
        upload_to="profile_pictures", storage=S3Boto3Storage(), null=True, blank=True
    )


class ArticleImage(models.Model):
    image = models.ImageField(
        upload_to="article_pictures", storage=S3Boto3Storage(), null=True, blank=True
    )


class User(AbstractUser):
    favorite_recipes = models.ManyToManyField(
        "recipe.Recipe", related_name="favorite_recipes"
    )
    favorite_articles = models.ManyToManyField(
        "account.Article", related_name="favorite_articles"
    )
    bio = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    profile_picture = models.OneToOneField(
        ProfileImage, on_delete=models.SET_NULL, null=True, blank=True
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="myapp_user_groups",  # specify a custom related name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="myapp_user_permissions",  # specify a custom related name
        related_query_name="user",
    )
    # Socials
    youtube_handle = models.URLField(blank=True)
    twitter_handle = models.URLField(blank=True)
    instagram_handle = models.URLField(blank=True)
    facebook_handle = models.URLField(blank=True)
    tiktok_handle = models.URLField(blank=True)
    website = models.URLField(blank=True)
    comments = GenericRelation("recipe.Comment")
    tags = models.ManyToManyField("recipe.Tag", blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.usernmae)
        user = User.objects.filter(slug=self.slug).exclude(id=self.id)
        if user.exists():
            slug, nb = self.slug.split("-")
            nb += 1
            self.slug = f"{slug}-{int(nb)}"
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    content = QuillField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    edited = models.BooleanField(default=False)
    edtied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_draft = models.BooleanField(default=True)

    image = models.OneToOneField(
        ArticleImage, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField("recipe.Tag", blank=True)
    comments = GenericRelation("recipe.Comment")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        art = Article.objects.filter(slug=self.slug).exclude(id=self.id)
        if art.exists():
            slug, nb = art.slug.split("-")
            nb += 1
            self.slug = f"{slug}-{int(nb)}"
        super().save(*args, **kwargs)

    # this one can be usefull for share btn
    # def get_absolute_url(self):
    #     return reverse("blog_entry_detail", args=[str(self.id)])


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
