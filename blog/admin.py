from django.contrib import admin
from .models import Author,Tag,Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter=("author","tag","date")
    list_display=("title","date","author")
    prepopulated_fields={"slug":("title",)}

class CommentModel(admin.ModelAdmin):
    list_display=("user_name","post")


admin.site.register(Post,PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentModel)
