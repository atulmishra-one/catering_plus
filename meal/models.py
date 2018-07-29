from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together= (('parent', 'slug'), )
        verbose_name_plural = 'categories'
        app_label = 'meal'

    def __str__(self):
        return self.name

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs


class Meal(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True)
    category = TreeForeignKey('Category', null=True, blank=True, db_index=True, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    image = ProcessedImageField(
        upload_to='meals/image/',
        processors=[ResizeToFill(220, 200)],
        format='PNG',
        options={'quality': 100},
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

