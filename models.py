from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext
from django.template.defaultfilters import slugify

class Photo(models.Model):
  path = models.CharField(max_length=512)
  slug = models.SlugField(max_length=120)
  added = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return self.path
  
class TagType(models.Model):
  name = models.CharField(max_length=32)
  slug = models.SlugField(max_length=32)
  
  def __unicode__(self):
    return self.name


class StarTag(models.Model):
  name = models.CharField(verbose_name=_('Name'), max_length=100)
  slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)
  starType = models.ForeignKey(TagType)
  
  def save(self, *args, **kwargs):
    if not self.pk:
      if not self.slug:
        self.slug = slugify(self.name)
    
    super(StarTag, self).save(*args, **kwargs)
  
  def __unicode__(self):
    return self.name

class AnnotatedTag(models.Model):
  """
  intermediate 'through' table for tags user's added.
  this will allow us to up or down vote the individual tags, etc...
  """
  userPhoto = models.ForeignKey('UserPhoto')
  tag = models.ForeignKey(StarTag)
  created = models.DateTimeField(auto_now=True)
  
  def __unicode__(self):
    return str(self.userPhoto) + ' -- ' + str(self.tag) + str(self.created)


class UserPhoto(models.Model):
  photo = models.ForeignKey(Photo)
  user = models.ForeignKey(User)
  tags = models.ManyToManyField(StarTag, through=AnnotatedTag)
  
  def __unicode__(self):
    return str(self.photo) + ' -- ' + str(self.user)


