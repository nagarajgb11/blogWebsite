from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Author(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()

    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    def __str__(self):
        return self.fullname()
        


class Post(models.Model):
    title = models.CharField(max_length=150,null=False)
    excerpt = models.CharField(max_length=200)
    #image_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="posts",null=True)
    date = models.DateField( auto_now=True)
    slug = models.SlugField(unique=True,db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
     
    def __str__(self):
         return f"{self.user_name}  {self.post}" 

    

