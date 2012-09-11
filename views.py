from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.template import RequestContext
import django.contrib.auth
from spt.models import Photo, UserPhoto, TagType, StarTag, AnnotatedTag
import spt.utils

class AddTagForm(forms.Form):
  upid = forms.IntegerField(widget=forms.HiddenInput, required=False)
  userid = forms.IntegerField(widget=forms.HiddenInput, required=False)
  photoid = forms.IntegerField(widget=forms.HiddenInput, required=False)
  tags = forms.CharField(widget=forms.Textarea, required=False)

  def make_changes(self):
    pass
  
def index(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/login/?next=%s' % request.path)
  
  photos = Photo.objects.all().order_by('-added')[:10]
  return render_to_response('spt/index.html', {'photos': photos })

def photo_detail(request, photo_slug):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/login/?next=%s' % request.path)
  
  if request.method == 'POST' :
    form = AddTagForm(request.POST)
    if form.is_valid():
      tags_char = form.cleaned_data['tags']
      tags = spt.utils.parse_tags(tags_char)
      
      if tags != '' or tags is not None:
        up = None
        
      if form.cleaned_data['upid'] is None:
        # so, need to create a new userphoto record.
        nu = auth.models.User.objects.get(pk=form.cleaned_data['userid'])
        ph = Photo.objects.get(pk=form.cleaned_data['photoid'])
        up = UserPhoto(user=nu, photo=ph)
        up.save()
      else:
        up = UserPhoto.objects.get(pk=form.cleaned_data['upid'])
        
        for x in tags:
          parts = x.split(':')
          print parts
          tt = TagType.objects.filter(name__iexact=parts[0])
          if tt is not None:
            tt = tt[0]
          st, created = StarTag.objects.get_or_create(starType=tt, name=parts[1])
                      
          anntag = AnnotatedTag(tag=st, userPhoto=up)
          anntag.save()
            
  p = get_object_or_404(Photo, slug=photo_slug)
  ups = None
  
  if p is not None:
    ups = UserPhoto.objects.filter(photo=p)
    
    g = ups.filter(user=request.user)
    if g is not None:
      form = AddTagForm({'upid' : g[0].id }, auto_id=True)
    else:
      form = AddTagForm({'upid': None, 'photoid':p.id, 'userid':request.user.id}, auto_id=True)
      
  return render_to_response('spt/photo_detail.html', 
                            {'photo': p, 
                             'userphotos':ups,
                             'lu': request.user,
                             'form':form,
                             },
                            context_instance=RequestContext(request))

def tags_list(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/login/?next=%s' % request.path)
  
  tags = StarTag.objects.all().order_by('name')
  
  return render_to_response('spt/tag_list.html',
                            {'tags': tags, 'lu': request.user },
                            context_instance=RequestContext(request))


def tag_detail(request, tag_slug):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/login/?next=%s' % request.path)
  
  tag = get_object_or_404(StarTag, slug=tag_slug)
  ats = AnnotatedTag.objects.filter(tag=tag)
  
  photos = set()
  for at in ats:
    k = at.userPhoto.photo
    if k not in photos:
      photos.add(k)
      
  
  return render_to_response('spt/tag_detail.html',
                            {'tag': tag, 'lu':request.user, 'photos':photos },
                            context_instance=RequestContext(request))

