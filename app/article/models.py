import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    content = QuillField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)

    edited = models.BooleanField(default=False)
    edtied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_draft = models.BooleanField(default=True)

    tags = models.ManyToManyField("common.Tag", related_name="articles", blank=True)
    rate = GenericRelation("common.Rate")
    comments = GenericRelation("common.Comment")
    Report = GenericRelation("common.Report")
    image = models.ForeignKey(
        "common.Image",
        related_name="articles",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Check if an article with the same slug already exists
        existing_article = (
            Article.objects.filter(slug=self.slug).exclude(id=self.id).first()
        )

        if existing_article:
            # If an article with the same slug exists, generate a unique slug
            for i in range(1, 200):
                new_slug = f"{self.slug}-{i}"
                if len(new_slug) > 200:
                    # If the new slug is too long, raise an error
                    new_slug = str(uuid.uuid4())[:200]
                if (
                    not Article.objects.filter(slug=new_slug)
                    .exclude(id=self.id)
                    .exists()
                ):
                    # If the new slug is unique, use it and stop the loop
                    self.slug = new_slug
                    break

        super().save(*args, **kwargs)

    # this one can be usefull for share btn
    # def get_absolute_url(self):
    #     return reverse("blog_entry_detail", args=[str(self.id)])
