from django.shortcuts import render
from post.models import Posting

def Post(request):
    posts=Posting.objects.all()
    return render(request, 'post.html', {'post':posts})

def sounds(request):
    return render(request, 'sounds.html', {})
