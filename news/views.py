from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from news.models import News, Comments, Likes
from .forms import CommentaryModelForm, NewsModelForm, CommentaryModelForm
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
# Create your views here.

def index(request, *args, **kwargs):
    qs = News.objects.all()
    context = {'news_list': qs }
    return render(request, 'index.html', context)

def detail_view(request, pk):
    user=request.user
    liked = False
    try:
        obj = News.objects.get(id=pk)
    except:
        raise Http404

    if request.user.is_authenticated and obj.likes.filter(user=user):
        liked = True
    return render(request, 'news/detail.html', {'single_object': obj, 'liked':liked})

def test_view(request, *args, **kwargs):
    data = dict(request.GET)
    print(data)
    obj = News.objects.get(id = data['pk'][0])
    return HttpResponse(f'<b>{obj.article}</b>')

@login_required
@permission_required('user.is_staff', raise_exception=True)
def create_view(request, *args, **kwargs):
    if request.method == "POST":
       form = NewsModelForm(request.POST, request.FILES)
       if form.is_valid():
           obj = form.save(commit=False)
           obj.author = request.user
           obj.save()
           form = NewsModelForm()
           return render(request, 'forms.html', {'form':form, 'obj':obj})
    form = NewsModelForm(request.POST or None)
    return render(request, 'forms.html', {'form':form})

@login_required
@permission_required('user.is_staff')
def edit_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = NewsModelForm(request.POST, instance=obj)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
    else:
        form = NewsModelForm(instance=obj)

    return render(request, 'edit_news_form.html', {'single_object':obj, 'form':form})

@login_required
@permission_required('user.is_staff')
def delete_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    obj.delete()
    return HttpResponseRedirect(reverse('index'))

@login_required
def commentary_view(request, pk):
    form = CommentaryModelForm(request.POST or None)
    try:
        comm = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404

    if form.is_valid():
        text = form.cleaned_data.get('text')
        user = request.user
        commentary_obj = Comments(user=user, text=text)
        commentary_obj.save()
        comm.commentary.add(commentary_obj)
        comm.save()
        return HttpResponseRedirect(reverse('detail-news', args=[pk]))
        
    return render(request, 'news/commentary.html', {'single_object':comm, 'form':form})

@login_required
def likes_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        user = request.user
        if not obj.likes.filter(user=user):
           like_obj = Likes(user=user, like=True)
           like_obj.save()
           obj.likes.add(like_obj)
           obj.save()
        else:
            obj.likes.filter(user=user).delete()
    return HttpResponseRedirect(reverse('detail-news', args=[pk]))


