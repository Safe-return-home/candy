from django.shortcuts import render, get_object_or_404
from post.models import Posting
from django.db.models import Count

def Post(request):
    sort_condition=request.GET.get('sort', 'name')
    # http://127.0.0.1:8000/countermeasure/?sort=recent
    if sort_condition=="recent":
        posts=Posting.objects.order_by('-upload_time')
        return render(request, 'post.html', {'post': posts})
    # http://127.0.0.1:8000/countermeasure/?sort=name
    elif sort_condition=="name":
        posts=Posting.objects.order_by('title')
        return render(request, 'post.html', {'post': posts})
    #posts=Posting.objects.all()


def Post_detail(request, pk):
    post_detail=get_object_or_404(Posting, pk=pk)
    return render(request, 'post_detail.html', {'post_detail':post_detail})
def sounds(request):
    return render(request, 'sounds.html', {})
