from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostModelForm
from django.contrib import messages
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect,HttpResponse,Http404
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# Create your views here.
def list_post_view(request):
    qs = Post.objects.all()
    template = 'forum/list.html'
    context = {'object_list' : qs}
    return render(request,template,context)

def my_post_view(request):
    if not request.user.is_authenticated:
        return render(request,'login_required.html')
    qs = Post.objects.filter(user=request.user)
    template = 'forum/list.html'
    context = {'object_list' : qs}
    return render(request,template,context)

def detail_post_view(request,slug):
    obj = get_object_or_404(Post,slug=slug)
    comments = obj.comments
    template_name = 'forum/post_detail.html'
    initial_data = {
        "content_type" : obj.get_content_type,
        "object_id" : obj.id ,
    }
    comment_form = CommentForm(request.POST or None,initial=initial_data)
    if comment_form.is_valid():
        # print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return render(request,'login_required.html')
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get('object_id')
        content = comment_form.cleaned_data.get('content')
        parent_obj = None
        # print(object_id)
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()
        # print(parent_id,parent_obj)
        try: 
            Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                content=content,
                parent=parent_obj)
            messages.success(request,'Successfully Commented')
        except:
            messages.error(request,"Try Again")
        comment_form = CommentForm()
        return HttpResponseRedirect(obj.get_absolute_url())
    l=[]
    for c in comments:
        l.append(c.content)
        for i in c.children():
            l.append(i.content)
    sid = SentimentIntensityAnalyzer()
    data=[0,0,0]
    for i in l:
        val = sid.polarity_scores(i).get('compound')
        if val==0:
            data[2]+=1
        elif val>0:
            data[0]+=1
        else:
            data[1]+=1
    if l:
        found=True
    else:
        found=False
    context = { 
        "post_detail" : obj,
        "comments" : comments,
        "comment_form" : comment_form,
        "data":data,
        "found":found
        }
    return render(request,template_name,context)

def edit_post_view(request,slug):
    obj = get_object_or_404(Post,slug=slug)
    form = PostModelForm(request.POST or None,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request,'Successfully Updated')
        return HttpResponseRedirect(obj.get_absolute_url())
    template_name = 'form.html'
    context = {"form" : form}
    return render(request,template_name,context)

def delete_post_view(request,slug):
    # print("###object")second-title-11
    obj = get_object_or_404(Post,slug=slug)
    # print("###object",obj)
    template_name = "delete.html"
    if request.method == "POST":
        obj.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('/forum')
    context = { "object":obj.title}
    return render(request,template_name,context)

def create_post_view(request):
    print(request,request.user,request.user.is_authenticated)
    if not request.user.is_authenticated:
        return render(request,'login_required.html')
    form = PostModelForm(request.POST or None,request.FILES or None)
    context = {"form" : form }
    if form.is_valid():
        obj = form.save(commit=False)
        # print("###object",obj,request.user)
        obj.user = request.user
        # print("###object",obj)
        obj.save()
        messages.success(request,'Successfully Created')
        return redirect('/forum')
    template_name = 'form.html'
    return render(request,template_name,context)