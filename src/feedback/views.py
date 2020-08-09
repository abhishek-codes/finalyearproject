from django.shortcuts import render,redirect
from .models import Feedback
from django.contrib import messages
# Create your views here.
def feedback(request):
    template_name = "feedback.html"
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        experience = request.POST.get('exp')
        recommened = request.POST.get('rec')
        msg = request.POST.get('message')
        # print(name,email,experience,recommened,msg)
        obj=Feedback.objects.create(name=name,email=email,experience=experience,recommened=recommened,msg=msg)
        print(obj)
        messages.success(request,'Successfully Created')
        return redirect('/feedback')
    return render(request,template_name)
