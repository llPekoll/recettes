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

    image = models.OneToOneField(
        "common.Image", on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField("common.Tag", blank=True)
    comments = GenericRelation("common.Comment")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        art = (
            Article.objects.filter(slug__contains=self.slug).exclude(id=self.id).last()
        )
        if art:
            slug_and_maybe_number = art.slug.split("-")
            slug = slug_and_maybe_number[0]
            if len(slug_and_maybe_number) > 1:
                nb = int(slug_and_maybe_number[-1])
                nb += 1
                self.slug = f"{slug}-{int(nb)}"
            else:
                self.slug = f"{slug}-1"

        if len(self.slug) > 199:
            nb = int(slug_and_maybe_number[-1])
            nb += 1
            self.slug = f"{self.slug[:100]}-{nb}"

        super().save(*args, **kwargs)

    # this one can be usefull for share btn
    # def get_absolute_url(self):
    #     return reverse("blog_entry_detail", args=[str(self.id)])
