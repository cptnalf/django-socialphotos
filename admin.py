from django.contrib import admin
from spt.models import Photo, UserPhoto, StarTag, TagType, AnnotatedTag

class PhotoAdmin(admin.ModelAdmin):
  prepopulated_fields = { 'slug': ('path', )}
  list_display = ('path' ,)
  

class AnnotatedTagAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_filter = [ 'created' ]
  list_display = ('userPhoto', 'tag', 'created')

class TagTypeAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name', )
  

class StarTagAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}
  list_display = ('name', 'starType')

class UserPhotoAdmin(admin.ModelAdmin):
  list_display = ('user', 'photo')

admin.site.register(Photo, PhotoAdmin)
admin.site.register(UserPhoto)
admin.site.register(StarTag, StarTagAdmin)
admin.site.register(TagType, TagTypeAdmin)
admin.site.register(AnnotatedTag, AnnotatedTagAdmin)
