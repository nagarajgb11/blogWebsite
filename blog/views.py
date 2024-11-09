from typing import Any, Dict
from django.db import models
from django.shortcuts import render,get_object_or_404
from datetime import date
from .models import Post
from django.views.generic import ListView,DetailView,TemplateView,CreateView,View
from .form import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

'''all_posts = [
    {
        "slug": "hike-in-the-mountains",
        "image": "mountains.jpg",
        "author": "Maximilian",
        "date": date(2021, 7, 21),
        "title": "Mountain Hiking",
        "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
        "content": """
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
        """
    },
    {
        "slug": "programming-is-fun",
        "image": "coding.jpg",
        "author": "Maximilian",
        "date": date(2022, 3, 10),
        "title": "Programming Is Great!",
        "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
        "content": """
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
        """
    },
    {
        "slug": "into-the-woods",
        "image": "woods.jpg",
        "author": "Maximilian",
        "date": date(2020, 8, 5),
        "title": "Nature At Its Best",
        "excerpt": "Nature is amazing! The amount of inspiration I get when walking in nature is incredible!",
        "content": """
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
        """
    }
]'''



##def get_date(post):
  # return post['date']

# Create your views here.

'''def starting_page(request):
  lastest_posts = Post.objects.all().order_by("-date")[:3] #django convert this line to sql command. in django negative indexing is not supporeted
  #sorted_posts = sorted(all_posts,key=get_date)
  #lastest_posts = sorted_posts[-3:]
  return render(request,"blog/index.html",{
     "posts":lastest_posts
  })'''
class starting_page(ListView):
   template_name = "blog/index.html"
   context_object_name ="posts"
   ordering = ["-date"]
   model = Post

   def get_queryset(self):
      queryset =  super().get_queryset()
      data = queryset[:3]
      return data

'''def posts(request):
  all_posts = Post.objects.all().order_by("-date")[:3]
  return render(request,'blog/all-posts.html',{
     "all_posts":all_posts
  })'''

class posts(ListView):
   template_name = "blog/all-posts.html"
   context_object_name = "all_posts"
   model = Post
   ordering = ["-date"]

'''def post_details(request,slug):
    #identified_post = next(post for post in all_posts if post['slug']==slug)
    #identified_post=Post.objects.get(slug=slug)
    identified_post=get_object_or_404(Post,slug=slug)
    return render(request,'blog/post-detail.html',{
       "post":identified_post,
       "post_tags":identified_post.tag.all()
    })'''

'''class post_details(DetailView):
   template_name='blog/post-detail.html'
   model = Post
   
   def get_context_data(self, **kwargs):
      context =super().get_context_data(**kwargs)
      context["comment_form"] = CommentForm()
      context["post_tags"]=self.object.tag.all()
      return context'''

class post_details(View):
   def is_stored(self,request,post_id):
      stored_posts = request.session.get("stored_posts")
      if stored_posts is not None:
         is_saved_later = post_id in stored_posts
      else:
         is_saved_later = None
      return is_saved_later
   
   def get(self,request,slug):
      post = Post.objects.get(slug=slug)
      context={
         "post" :post,
         "post_tags":post.tag.all(),
         "comment_form":CommentForm(),
         "comments":post.comments.all().order_by("-id"),
         "is_saved_later":self.is_stored(request, post.id)
      }
      return render(request,"blog/post-detail.html",context)
   
   def post(self,request,slug):
      comment_form = CommentForm(request.POST)
      post = Post.objects.get(slug=slug)

      if comment_form.is_valid():
         comment=comment_form.save(commit=False)
         comment.post = post
         comment.save()
         return HttpResponseRedirect(reverse("post_detail_page",args=[slug]))
      
      context={
         "post" :post,
         "post_tags":post.tag.all(),
         "comment_form":comment_form,
         "comments":post.comments.all().order_by("-id"),
         "is_saved_later":self.is_stored(request, post.id)
      }
      return render(request,"blog/post-detail.html",context)
   
class Read(View):
   def get(self,request):
      stored_posts = request.session.get("stored_posts")
      context ={}
      if stored_posts is None or len(stored_posts) == 0:
         context["posts"] = []
         context["has_posts"] = False
      else:
         posts = Post.objects.filter(id__in=stored_posts)
         context["posts"] = posts
         context["has_posts"] = True
      
      return render(request,"blog/stored.html",context)
   def post(self,request):
      stored_posts = request.session.get("stored_posts")

      if stored_posts is None:
         stored_posts = []
      post_id = int(request.POST['post_id'])
      if post_id not in stored_posts:
         stored_posts.append(post_id)
         request.session["stored_posts"] = stored_posts #to save the stored_posts in session

      else:
         stored_posts.remove(post_id)
      request.session["stored_posts"] = stored_posts
      
      return HttpResponseRedirect("/")      


      
   
   


