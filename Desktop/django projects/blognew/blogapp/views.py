from django.shortcuts import render
from blogapp.forms import postform

from django.urls import reverse_lazy

# Create your views here.
from django.http import HttpResponse
from blogapp.models import post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView

def nav(r):
    return render(r,"blogapp/navbar.html")

class home(ListView):
    model=post
    template_name="blogapp/home.html"
    ordering=['-id']

def detail(r,pk):
    p=post.objects.get(id=pk)
    likes_count=p.likes.count()
    if r.method=='POST':
        if r.user.post_likes.exists():
            p.likes.remove(r.user)
        else:
            p.likes.add(r.user)
        # return redirect
    context={"post":p,"lc":likes_count}
    return render(r,"blogapp/detail.html",context)

# class detail(DetailView):
#     model=post
#     template_name="blogapp/detail.html"


class create(CreateView):
    model=post
    fields=["message","title"]
    template_name="blogapp/create.html"

class update(UpdateView):
    model=post
    fields=["message","title"]
    template_name="blogapp/update.html"

class delete(DeleteView):
    model=post
    template_name="blogapp/delete.html"
    success_url=reverse_lazy("home")


def like(r):
    return HttpResponse("you liked")
