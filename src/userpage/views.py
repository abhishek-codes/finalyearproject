from django.shortcuts import render,get_object_or_404
from .models import User_detail
from comments.models import Comment
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create your views here.
def my_profile(request):
    # if not request.user.is_authenticated:
    #     return render(request,'login_required.html')
    # obj=User_detail.objects.filter(user=request.user)
    # if not obj:
    #     obj = User_detail.objects.create(user=request.user,email=user.email)
    # context = {"object" : obj }
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     email = request.POST.get('email')
    #     experience = request.POST.get('exp')
    #     recommened = request.POST.get('rec')
    #     msg = request.POST.get('message')
    #     messages.success(request,'Successfully Created')
    #     return redirect('/profile/my-profile')
    return render(request,'profile.html')

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