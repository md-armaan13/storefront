from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#import user moddel from setting not from auth as it is independent app
from django.conf import settings

class LikeItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #To Identify the object we need 2 things type and id
    #Type is the model name and id is the primary key

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    # `GenericForeignKey` is a feature of Django that allows a model to be related to any other model via a foreign key,
