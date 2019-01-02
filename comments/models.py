from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# from shop.models import Product

# Create your models here.

class CommentManager(models.Manager):
    def filter_by_product(self, product):
        content_type = ContentType.objects.get_for_model(product.__class__)
        obj_id = product.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)

        return qs




class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE,)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comments/%Y/%m/%d', blank=True, null=True)

    objects = CommentManager()

    def __str__(self):
        return self.user.username
