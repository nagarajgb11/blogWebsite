from django.urls import path
from .import views
urlpatterns = [
    #path("",views.starting_page,name="starting_pages"),
    path("",views.starting_page.as_view(),name = "starting_pages"),
    #path("posts",views.posts,name="posts_page"),
    path("posts",views.posts.as_view(),name="posts_page"),
    #path("posts/<slug:slug>",views.post_details,name="post_detail_page"),                                        
    path("posts/<slug:slug>",views.post_details.as_view(),name="post_detail_page"),
    path("read-later",views.Read.as_view(),name="read-later")                                                          
]
#posts/my-first-post,<slug>search engine friendly identifier
#slug tranformer(should contain num or texts,dashes,not any special char)