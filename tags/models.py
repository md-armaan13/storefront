from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

#Creating CUSTOM MANAGER FOR GETTING TAGGEDITEM
class TaggedItemManager(models.Manager):
    def get_tag_for(self , obj_type , obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        tag_item = TaggedItem.objects.filter(content_type = content_type,object_id = obj_id)
        return tag_item
 



class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class TaggedItem(models.Model):
    objects = TaggedItemManager()#for adding custom manager
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    #To Identify the object we need 2 things type and id
    #Type is the model name and id is the primary key

    #Here we are using generic foreign key to identify the object
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
   # `GenericForeignKey` is a feature of Django that allows a model to be related to any other model via a foreign key,
   #  without you having to create the foreign key field yourself.