from django.db import models
from uuslug import uuslug


class PageContentType(models.Model):
    """
    The kind of content contained in a content block.
    Used to serialize content blocks.
    """
    slug = models.SlugField(
        blank=True,
        max_length=255,
        unique=True,
        editable=False,
        primary_key=True
    )
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuslug(
                self.name,
                instance=self,
                max_length=100,
                separator='-',
                start_no=2
            )
        super(PageContentType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
