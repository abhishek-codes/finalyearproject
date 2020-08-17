from django.shortcuts import render,get_object_or_404,redirect
from .models import User_detail
from comments.models import Comment
from django.contrib import messages
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .forms import UserPageForm

# Create your views here.
def my_profile(request):
    obj = get_object_or_404(User_detail,user=request.user)
    form = UserPageForm(request.POST or None,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request,'Successfully Updated')
        return redirect(f'/profile/{obj.slug}')
    template_name = 'form.html'
    context = {"form" : form,"title":"EDIT PROFILE"}
    return render(request,template_name,context)

def u_profile(request,slug):
    obj=get_object_or_404(User_detail,slug=slug)
    comments = Comment.objects.filter(user=obj.user)
    l=[]
    for c in comments:
        l.append(c.content)
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
    context = {"object" : obj , "data":data,"found":found}
    return render(request,'profile_view.html',context)